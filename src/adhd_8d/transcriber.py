"""
GPU Kinetic Caption Generator
=============================
Generates high-dopamine, dead-center kinetic captions using speech-to-text GPU acceleration
(via faster-whisper).
Formats text into punchy 2-4 word bursts to eliminate saccadic eye wandering.
"""

import os
import sys
import subprocess
from datetime import timedelta
from typing import List, Tuple, Optional
import numpy as np

# Load PyTorch CUDA DLLs on Windows
try:
    import torch
    torch_lib = os.path.join(os.path.dirname(torch.__file__), "lib")
    if os.path.exists(torch_lib):
        os.add_dll_directory(torch_lib)
except Exception:
    pass

from faster_whisper import WhisperModel
from .config import PRESETS, VideoPreset

def format_srt_time(seconds: float) -> str:
    td = timedelta(seconds=max(0.0, seconds))
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_ass_time(seconds: float) -> str:
    total_seconds = int(max(0.0, seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    centis = int((seconds - int(seconds)) * 100)
    return f"{hours:d}:{minutes:02d}:{secs:02d}.{centis:02d}"

def decode_audio_16k(audio_path: str) -> np.ndarray:
    """Decode audio to 16kHz mono float32 numpy array."""
    cmd = [
        "ffmpeg", "-v", "error",
        "-i", audio_path,
        "-f", "s16le", "-ac", "1", "-ar", "16000", "-"
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768.0

def transcribe_and_format_captions(
    audio_path: str,
    ass_output: str,
    srt_output: Optional[str] = None,
    preset_name: str = "mobile_9_16",
    whisper_model: str = "base",
    device: str = "cuda",
    compute_type: str = "float16",
    max_words_per_burst: int = 4
) -> int:
    """
    Transcribe audio and write ASS captions formatted for ADHD cognitive offloading.
    """
    preset = PRESETS.get(preset_name, PRESETS["mobile_9_16"])

    print(f"[*] Decoding audio for speech recognition: {audio_path}")
    audio_arr = decode_audio_16k(audio_path)
    audio_dur = len(audio_arr) / 16000.0
    print(f"[*] Decoded audio duration: {audio_dur:.1f}s ({audio_dur/60:.1f} min)")

    print(f"[*] Loading faster-whisper ({whisper_model}) on {device.upper()} ({compute_type})...")
    try:
        model = WhisperModel(whisper_model, device=device, compute_type=compute_type)
    except Exception as e:
        print(f"[!] Warning: CUDA initialization failed ({e}). Falling back to CPU...")
        model = WhisperModel(whisper_model, device="cpu", compute_type="int8")

    print("[*] Running word-level timestamp transcription...")
    segments, info = model.transcribe(audio_arr, beam_size=5, word_timestamps=True, language="en")
    print(f"[*] Detected spoken language: {info.language}")

    caption_chunks: List[Tuple[float, float, str]] = []

    for segment in segments:
        words = segment.words if segment.words else []
        if not words:
            caption_chunks.append((segment.start, segment.end, segment.text.strip()))
            continue

        chunk_words = []
        chunk_start = words[0].start
        for w in words:
            w_str = w.word.strip()
            if not w_str:
                continue
            chunk_words.append(w_str)
            if len(chunk_words) >= max_words_per_burst or w_str.endswith(('.', '?', '!', ';', ':')):
                chunk_end = w.end
                text = " ".join(chunk_words)
                if text:
                    caption_chunks.append((chunk_start, chunk_end, text))
                chunk_words = []
                chunk_start = w.end
        if chunk_words:
            caption_chunks.append((chunk_start, words[-1].end, " ".join(chunk_words)))

    # Write ASS with dead-center alignment (Alignment 5)
    ass_header = f"""[Script Info]
Title: ADHD Study Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {preset.width}
PlayResY: {preset.height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ADHD_Captions,Arial Black,{preset.caption_fontsize},&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,7.0,4.0,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_output, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for start, end, text in caption_chunks:
            clean_text = text.replace("{", "\\{").replace("}", "\\}")
            f.write(f"Dialogue: 0,{format_ass_time(start)},{format_ass_time(end)},ADHD_Captions,,0,0,0,,{clean_text}\n")

    if srt_output:
        with open(srt_output, "w", encoding="utf-8") as f:
            for idx, (start, end, text) in enumerate(caption_chunks, start=1):
                f.write(f"{idx}\n{format_srt_time(start)} --> {format_srt_time(end)}\n{text}\n\n")

    print(f"[+] Total kinetic captions created: {len(caption_chunks)}")
    return len(caption_chunks)
