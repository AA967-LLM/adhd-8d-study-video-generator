"""
Bilateral Dual-Speaker 8D Dialogue Engine
=========================================
Implements alternating bilateral auditory stimulation for ADHD focus.
- Speaker 1 (e.g. Alex / Questioner): Left Ear dominant (85% Left / 15% Right), Voice: en-US-AriaNeural
- Speaker 2 (e.g. Marcus / Explainer): Right Ear dominant (15% Left / 85% Right), Voice: en-GB-RyanNeural
- Combined with a 0.20 Hz continuous 8D spatial acoustic sweep.
Forces bilateral cerebral engagement and eliminates mental wandering.
"""

import os
import sys
import tempfile
import asyncio
import subprocess
from typing import List, Tuple
import edge_tts

DEFAULT_SPEAKER1_VOICE = "en-US-AriaNeural"   # Left Ear (curious, sharp)
DEFAULT_SPEAKER2_VOICE = "en-GB-RyanNeural"   # Right Ear (witty, authoritative)


def parse_dialogue(text: str) -> List[Tuple[str, str]]:
    """
    Parse a dialogue text into structured [(speaker_id, text_snippet)] turns.
    Recognizes prefixes like 'Alex:', 'Marcus:', 'Speaker 1:', 'Speaker 2:', 'Q:', 'A:'.
    If no speaker tags exist, splits by paragraphs into alternating turns.
    """
    lines = text.strip().splitlines()
    dialogue: List[Tuple[str, str]] = []
    current_speaker = "speaker1"
    current_buffer: List[str] = []

    for line in lines:
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue

        lower = raw.lower()
        if lower.startswith(("alex:", "speaker 1:", "s1:", "q:", "question:")):
            if current_buffer:
                dialogue.append((current_speaker, " ".join(current_buffer)))
                current_buffer = []
            current_speaker = "speaker1"
            parts = raw.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                current_buffer.append(parts[1].strip())
        elif lower.startswith(("marcus:", "speaker 2:", "s2:", "a:", "answer:", "explanation:")):
            if current_buffer:
                dialogue.append((current_speaker, " ".join(current_buffer)))
                current_buffer = []
            current_speaker = "speaker2"
            parts = raw.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                current_buffer.append(parts[1].strip())
        else:
            current_buffer.append(raw)

    if current_buffer:
        dialogue.append((current_speaker, " ".join(current_buffer)))

    # Fallback: if all text ended up as one speaker, alternate by sentences
    if len(dialogue) <= 1 and dialogue:
        single_text = dialogue[0][1]
        sentences = [s.strip() for s in single_text.replace("! ", ". ").replace("? ", ". ").split(". ") if s.strip()]
        new_dialogue = []
        for i, s in enumerate(sentences):
            spk = "speaker1" if i % 2 == 0 else "speaker2"
            new_dialogue.append((spk, s + "."))
        return new_dialogue

    return dialogue


async def synthesize_clip_async(text: str, voice: str, out_file: str):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(out_file)


def synthesize_bilateral_dialogue(
    script_text: str,
    output_path: str,
    speed: float = 1.20,
    speaker1_voice: str = DEFAULT_SPEAKER1_VOICE,
    speaker2_voice: str = DEFAULT_SPEAKER2_VOICE,
    freq_hz: float = 0.20,
    amount: float = 0.95
) -> float:
    """
    Generate an alternating bilateral dual-speaker 8D audio master.
    """
    turns = parse_dialogue(script_text)
    if not turns:
        raise ValueError("No dialogue content found to synthesize.")

    temp_dir = tempfile.mkdtemp(prefix="bilateral_")
    clip_files: List[str] = []

    print(f"[*] Synthesizing {len(turns)} bilateral dialogue turns...")
    print(f"    - Left Ear  (85/15 pan): {speaker1_voice}")
    print(f"    - Right Ear (15/85 pan): {speaker2_voice}")

    try:
        for idx, (spk, snippet) in enumerate(turns):
            raw_tts = os.path.join(temp_dir, f"raw_{idx}.mp3")
            panned_clip = os.path.join(temp_dir, f"clip_{idx}.m4a")

            voice = speaker1_voice if spk == "speaker1" else speaker2_voice
            asyncio.run(synthesize_clip_async(snippet, voice, raw_tts))

            # Apply hard bilateral ear panning
            if spk == "speaker1":
                # Left Ear dominant
                pan_filter = "pan=stereo|c0=0.85*c0|c1=0.15*c0"
            else:
                # Right Ear dominant
                pan_filter = "pan=stereo|c0=0.15*c0|c1=0.85*c0"

            cmd_pan = [
                "ffmpeg", "-y", "-i", raw_tts,
                "-af", pan_filter,
                "-c:a", "aac", "-b:a", "192k",
                panned_clip
            ]
            subprocess.run(cmd_pan, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            clip_files.append(panned_clip)

        # Build concat list file
        concat_list = os.path.join(temp_dir, "concat.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for cfile in clip_files:
                f.write(f"file '{cfile.replace(os.sep, '/')}'\n")

        # Concat all turns together
        merged_raw = os.path.join(temp_dir, "merged.m4a")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            merged_raw
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Layer the master 8D sweep and tempo pacing
        filter_chains = []
        if abs(speed - 1.0) > 0.01:
            filter_chains.append(f"atempo={speed}")
        filter_chains.append(f"apulsator=mode=sine:hz={freq_hz}:amount={amount}:offset_l=0:offset_r=0.5")
        filter_chains.append("loudnorm=I=-16:TP=-1.5:LRA=11")
        master_af = ",".join(filter_chains)

        cmd_master = [
            "ffmpeg", "-y",
            "-i", merged_raw,
            "-af", master_af,
            "-c:a", "aac", "-b:a", "192k",
            output_path
        ]
        subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Get duration
        cmd_dur = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            output_path
        ]
        dur_res = subprocess.run(cmd_dur, stdout=subprocess.PIPE, text=True, check=True)
        dur = float(dur_res.stdout.strip())
        print(f"[+] Bilateral 8D Dialogue audio created: {output_path} ({dur:.1f}s)")
        return dur

    finally:
        # Cleanup temp clips
        try:
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)
        except Exception:
            pass
