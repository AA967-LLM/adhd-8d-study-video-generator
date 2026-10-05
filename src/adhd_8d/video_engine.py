"""
Video Engine & ADHD Sensory Compositor
======================================
Pairs 8D audio with continuous background video loops (gameplay motion, kinetic loops),
burns dead-center kinetic captions, and injects a real-time dopamine HUD
(progress bar and elapsed/remaining time countdown).
"""

import os
import subprocess
from typing import Optional
from .config import PRESETS, VideoPreset

FONT_PATH_WINDOWS = "C\\:/Windows/Fonts/segoeuib.ttf"

def check_nvenc() -> bool:
    """Return True if hardware NVENC encoder is supported."""
    try:
        res = subprocess.run(["ffmpeg", "-encoders"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "h264_nvenc" in res.stdout
    except Exception:
        return False

def format_time_str(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}\\:{m:02d}\\:{s:02d}"
    return f"{m:02d}\\:{s:02d}"

def render_study_video(
    background_video: str,
    audio_path: str,
    ass_subtitles: str,
    output_video: str,
    duration: float,
    title: str = "ADHD High-Retention Study Session",
    preset_name: str = "mobile_9_16",
    font_path: str = FONT_PATH_WINDOWS,
    add_hud: bool = True
):
    """
    Renders high-dopamine ADHD study video using hardware GPU acceleration.
    """
    preset = PRESETS.get(preset_name, PRESETS["mobile_9_16"])
    use_nvenc = check_nvenc()

    total_time_fmt = format_time_str(duration)
    clean_title = title.replace(":", "\\:").replace("'", "\\'")

    # Use relative filename or escaped forward slashes for libass
    ass_rel = os.path.basename(ass_subtitles)
    # Check if ass is in current working directory; if not, use properly escaped path
    if os.path.exists(ass_rel) and os.path.abspath(ass_rel) == os.path.abspath(ass_subtitles):
        ass_arg = f"ass=filename='{ass_rel}'"
    else:
        escaped_ass = ass_subtitles.replace("\\", "/").replace(":", "\\:")
        ass_arg = f"ass='{escaped_ass}'"

    vf_filters = [
        f"scale={preset.width}:{preset.height}:force_original_aspect_ratio=increase,crop={preset.width}:{preset.height}",
        ass_arg
    ]

    if add_hud:
        # Progress bar background
        vf_filters.append(f"drawbox=x=0:y=ih-{preset.progress_bar_height}:w=iw:h={preset.progress_bar_height}:color=black@0.75:t=fill")
        # Glowing cyan progress bar
        vf_filters.append(f"drawbox=x=0:y=ih-{preset.progress_bar_height}:w='iw*(t/{duration:.2f})':h={preset.progress_bar_height}:color=#00E5FF:t=fill")
        # Top title banner
        vf_filters.append(f"drawtext=fontfile='{font_path}':text='{clean_title}':x=24:y=24:fontsize={preset.title_fontsize}:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=10")
        # Top right live countdown timer
        vf_filters.append(f"drawtext=fontfile='{font_path}':text='%{{pts\\:gmtime\\:0\\:%M\\\\\\:%S}} / {total_time_fmt}':x=w-tw-24:y=24:fontsize={preset.hud_fontsize}:fontcolor=#00E5FF:box=1:boxcolor=black@0.7:boxborderw=10")

    vf_chain = ",".join(vf_filters)

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", background_video,
        "-i", audio_path,
        "-t", f"{duration:.2f}",
        "-vf", vf_chain,
        "-c:v", "h264_nvenc" if use_nvenc else "libx264",
        "-preset", "p4" if use_nvenc else "veryfast",
        "-cq", "24" if use_nvenc else "22",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_video
    ]

    print(f"[*] Rendering study video ({preset.width}x{preset.height}) with {'Hardware NVENC' if use_nvenc else 'CPU'}...")
    subprocess.run(cmd, check=True)

    size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"[+] SUCCESS: ADHD study video generated at {output_video} ({size_mb:.2f} MB)")
