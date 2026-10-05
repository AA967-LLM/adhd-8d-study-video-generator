"""
Open-Source Procedural Motion Background Generator
==================================================
Generates 100% copyright-free, mathematically computed kinetic visual loops
using pure open-source algorithms (fractal zooms, 3D starfields, audio-reactive spectra).
Eliminates any reliance on proprietary or third-party gameplay footage.
"""

import os
import sys
import subprocess
import numpy as np
from pathlib import Path
from typing import Optional
from .config import PRESETS, VideoPreset

def get_cache_dir() -> str:
    """Return user cache directory for storing reusable procedural loops."""
    home = Path.home()
    cache_dir = home / ".cache" / "adhd_8d"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return str(cache_dir)

def generate_fractal_loop(
    output_path: str,
    width: int = 720,
    height: int = 1280,
    duration: int = 45,
    fps: int = 30
) -> str:
    """
    Generate an infinite hypnotic Mandelbrot fractal zoom loop using pure math.
    Zero external video assets required. 100% open-source procedural graphics.
    """
    total_pts = duration * fps
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"mandelbrot=s={width}x{height}:r={fps}:end_scale=0.00001:end_pts={total_pts}:outer=normalized_iteration_count",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    print(f"[*] Generating open-source procedural fractal loop ({width}x{height}, {duration}s)...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Procedural background ready: {output_path}")
    return output_path

def generate_starfield_loop(
    output_path: str,
    width: int = 720,
    height: int = 1280,
    duration: int = 30,
    fps: int = 30,
    num_stars: int = 800
) -> str:
    """
    Generate a 3D forward-warp starfield loop in pure NumPy matrix mathematics.
    Fast, lightweight, zero copyright liabilities.
    """
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    print(f"[*] Generating open-source 3D starfield warp loop ({width}x{height}, {duration}s)...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    stars = np.random.uniform(-1.0, 1.0, (num_stars, 3))
    stars[:, 2] = np.random.uniform(0.05, 1.0, num_stars)

    cx, cy = width // 2, height // 2

    for _ in range(duration * fps):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        stars[:, 2] -= 0.02
        reset = stars[:, 2] <= 0.04
        stars[reset, 2] = 1.0
        stars[reset, 0] = np.random.uniform(-1.0, 1.0, np.sum(reset))
        stars[reset, 1] = np.random.uniform(-1.0, 1.0, np.sum(reset))

        sx = ((stars[:, 0] / stars[:, 2]) * cx + cx).astype(int)
        sy = ((stars[:, 1] / stars[:, 2]) * cy + cy).astype(int)
        valid = (sx >= 0) & (sx < width) & (sy >= 0) & (sy < height)

        bright = ((1.0 - stars[valid, 2]) * 255).astype(np.uint8)
        frame[sy[valid], sx[valid], 0] = bright // 3
        frame[sy[valid], sx[valid], 1] = bright
        frame[sy[valid], sx[valid], 2] = bright

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"[+] Procedural starfield ready: {output_path}")
    return output_path

def get_or_create_default_background(
    preset_name: str = "mobile_9_16",
    style: str = "fractal"
) -> str:
    """
    Retrieve or automatically generate a cached open-source procedural motion loop.
    Ensures zero external video assets or third-party files are required to run the pipeline.
    """
    preset = PRESETS.get(preset_name, PRESETS["mobile_9_16"])
    cache_dir = get_cache_dir()
    cached_file = os.path.join(cache_dir, f"procedural_{style}_{preset.width}x{preset.height}.mp4")

    if os.path.exists(cached_file) and os.path.getsize(cached_file) > 1024:
        return cached_file

    if style == "starfield":
        return generate_starfield_loop(cached_file, width=preset.width, height=preset.height)
    else:
        return generate_fractal_loop(cached_file, width=preset.width, height=preset.height)
