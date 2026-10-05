"""
CLI Interface for ADHD 8D Study Video Generator
===============================================
Command-line entrypoint allowing users to convert any audio/video lecture, podcast,
or tutorial into a high-retention 8D audio and kinetic visual loop experience.
"""

import os
import sys
import argparse
from .config import PRESETS, DEFAULT_SPEED, DEFAULT_8D_FREQ_HZ, DEFAULT_8D_AMOUNT
from .audio_engine import process_8d_audio
from .transcriber import transcribe_and_format_captions
from .video_engine import render_study_video

from .procedural import get_or_create_default_background
from .document_ingest import extract_document_text, synthesize_text_to_speech

def main():
    parser = argparse.ArgumentParser(
        prog="adhd-8d",
        description="Convert ANY lecture, audio, PDF, or text document into an 8D audio and ADHD kinetic visual loop study experience."
    )
    parser.add_argument("-i", "--input", required=True, help="Input media or document: audio (.m4a, .mp3), video (.mp4), PDF (.pdf), or text (.txt, .md)")
    parser.add_argument("-b", "--background", help="Path to background visual loop (.mp4). If omitted, an open-source procedural motion loop is used.")
    parser.add_argument("--procedural-style", choices=["fractal", "starfield"], default="fractal", help="Built-in procedural background style (default: fractal)")
    parser.add_argument("--voice", default="en-US-ChristopherNeural", help="Voice for PDF/text speech synthesis (default: en-US-ChristopherNeural)")
    parser.add_argument("-o", "--output", help="Output path (.mp4 for full video, or .mp3/.m4a for audio only)")
    parser.add_argument("-t", "--title", default="ADHD High-Retention Study Session", help="Title banner overlay text")
    parser.add_argument("-s", "--speed", type=float, default=DEFAULT_SPEED, help=f"Cognitive acceleration speed multiplier (default: {DEFAULT_SPEED})")
    parser.add_argument("--freq", type=float, default=DEFAULT_8D_FREQ_HZ, help=f"8D oscillation frequency in Hz (default: {DEFAULT_8D_FREQ_HZ} Hz)")
    parser.add_argument("--amount", type=float, default=DEFAULT_8D_AMOUNT, help=f"8D panning depth 0.0-1.0 (default: {DEFAULT_8D_AMOUNT})")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default="mobile_9_16", help="Resolution preset (default: mobile_9_16 [720x1280])")
    parser.add_argument("--whisper-model", default="base", help="Faster-whisper model (tiny, base, small, medium, large-v3) (default: base)")
    parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Compute device for transcription (default: cuda)")
    parser.add_argument("--audio-only", action="store_true", help="Generate only the 8D audio file without video rendering")
    parser.add_argument("--strip-silence", action="store_true", help="Automatically remove dead pauses longer than 0.4s")
    parser.add_argument("--no-hud", action="store_true", help="Disable the glowing progress bar and timer HUD")

    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    if not os.path.exists(input_file):
        print(f"[-] Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    base_dir = os.path.dirname(input_file)
    stem = os.path.splitext(os.path.basename(input_file))[0]
    temp_tts_audio = None

    # Detect PDF or Text document input
    ext = os.path.splitext(input_file)[1].lower()
    if ext in [".pdf", ".txt", ".md"]:
        print(f"[*] Detected document input ({ext}): {input_file}")
        text = extract_document_text(input_file)
        temp_tts_audio = os.path.join(base_dir, f"{stem}_synthesized.mp3")
        synthesize_text_to_speech(text, temp_tts_audio, voice=args.voice)
        input_file = temp_tts_audio

    # Audio-only mode
    if args.audio_only or (args.output and args.output.lower().endswith((".mp3", ".wav", ".m4a"))):
        out_audio = os.path.abspath(args.output) if args.output else os.path.join(base_dir, f"{stem}_8D.mp3")
        process_8d_audio(
            input_path=input_file,
            output_path=out_audio,
            speed=args.speed,
            freq_hz=args.freq,
            amount=args.amount,
            strip_silence=args.strip_silence
        )
        print(f"\n[+] SUCCESS! 8D Audio file ready at: {out_audio}")
        return

    # Full Video Mode: If background not specified, use built-in procedural loop
    if not args.background:
        print("[*] No background video provided. Using built-in open-source procedural motion loop...")
        bg_video = get_or_create_default_background(preset_name=args.preset, style=args.procedural_style)
    else:
        bg_video = os.path.abspath(args.background)
        if not os.path.exists(bg_video):
            print(f"[-] Error: Background video not found: {bg_video}", file=sys.stderr)
            sys.exit(1)

    out_video = os.path.abspath(args.output) if args.output else os.path.join(base_dir, f"{stem}_8D_ADHD.mp4")
    temp_8d_audio = os.path.join(base_dir, f"{stem}_temp_8d.m4a")
    ass_captions = os.path.join(base_dir, f"{stem}_captions.ass")
    srt_captions = os.path.join(base_dir, f"{stem}_captions.srt")

    try:
        # Step 1: 8D Audio
        duration = process_8d_audio(
            input_path=input_file,
            output_path=temp_8d_audio,
            speed=args.speed,
            freq_hz=args.freq,
            amount=args.amount,
            strip_silence=args.strip_silence
        )

        # Step 2: GPU Captions
        transcribe_and_format_captions(
            audio_path=temp_8d_audio,
            ass_output=ass_captions,
            srt_output=srt_captions,
            preset_name=args.preset,
            whisper_model=args.whisper_model,
            device=args.device
        )

        # Step 3: Render Video
        render_study_video(
            background_video=bg_video,
            audio_path=temp_8d_audio,
            ass_subtitles=ass_captions,
            output_video=out_video,
            duration=duration,
            title=args.title,
            preset_name=args.preset,
            add_hud=not args.no_hud
        )

        print(f"\n[+] SUCCESS! ADHD 8D Study Video generated at: {out_video}")

    finally:
        # Clean temporary intermediate audio if needed
        if os.path.exists(temp_8d_audio):
            try:
                os.remove(temp_8d_audio)
            except Exception:
                pass
        if temp_tts_audio and os.path.exists(temp_tts_audio):
            try:
                os.remove(temp_tts_audio)
            except Exception:
                pass

if __name__ == "__main__":
    main()
