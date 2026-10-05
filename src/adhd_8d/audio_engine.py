"""
8D Audio Processing Engine
==========================
Transforms standard mono or flat stereo recordings into high-focus 8D spatial audio.
Uses continuous sinusoidal interaural level and phase differences to engage
both cerebral hemispheres and stimulate the brainstem's superior olivary complex.
"""

import os
import subprocess
from typing import Optional
from .config import DEFAULT_8D_FREQ_HZ, DEFAULT_8D_AMOUNT, DEFAULT_SPEED, DEFAULT_LOUDNORM

def get_audio_duration(file_path: str) -> float:
    """Return exact audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def process_8d_audio(
    input_path: str,
    output_path: str,
    speed: float = DEFAULT_SPEED,
    freq_hz: float = DEFAULT_8D_FREQ_HZ,
    amount: float = DEFAULT_8D_AMOUNT,
    loudnorm: str = DEFAULT_LOUDNORM,
    strip_silence: bool = False
) -> float:
    """
    Process any input audio/video into an 8D spatialized audio track.

    Args:
        input_path: Path to input audio or video file
        output_path: Destination path (.mp3, .m4a, or .wav)
        speed: Playback speed multiplier (default 1.20)
        freq_hz: Panning oscillation frequency in Hz (default 0.18 Hz ~ 5.5s cycle)
        amount: Panning depth between 0.0 and 1.0 (default 0.85)
        loudnorm: FFmpeg loudnorm filter specification
        strip_silence: Whether to remove dead pauses longer than 0.4s

    Returns:
        float: Duration of generated audio in seconds
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input media not found: {input_path}")

    filter_chains = []

    if strip_silence:
        filter_chains.append("silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-42dB")

    if abs(speed - 1.0) > 0.01:
        filter_chains.append(f"atempo={speed}")

    # 8D bilateral sinusoidal sweep
    filter_chains.append(f"apulsator=mode=sine:hz={freq_hz}:amount={amount}:offset_l=0:offset_r=0.5")

    # Speech loudness normalization
    if loudnorm:
        filter_chains.append(f"loudnorm={loudnorm}")

    af_filter = ",".join(filter_chains)

    # Determine encoder by extension
    ext = os.path.splitext(output_path)[1].lower()
    if ext == ".mp3":
        codec_args = ["-c:a", "libmp3lame", "-b:a", "192k"]
    elif ext in [".m4a", ".aac"]:
        codec_args = ["-c:a", "aac", "-b:a", "192k"]
    elif ext == ".wav":
        codec_args = ["-c:a", "pcm_s16le"]
    else:
        codec_args = ["-c:a", "aac", "-b:a", "192k"]

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-af", af_filter,
        *codec_args,
        output_path
    ]

    print(f"[*] Running 8D Audio Engine on: {input_path}")
    print(f"[*] Settings: Speed={speed}x | Frequency={freq_hz}Hz | Modulation={amount*100}%")
    subprocess.run(cmd, check=True)

    duration = get_audio_duration(output_path)
    print(f"[+] 8D Audio complete: {output_path} ({duration:.1f}s)")
    return duration
