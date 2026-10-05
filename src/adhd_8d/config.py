"""
Configuration and Presets for ADHD 8D Video Generation
======================================================
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class VideoPreset:
    name: str
    width: int
    height: int
    caption_fontsize: int
    title_fontsize: int
    hud_fontsize: int
    progress_bar_height: int

PRESETS = {
    "mobile_9_16": VideoPreset(
        name="mobile_9_16",
        width=720,
        height=1280,
        caption_fontsize=58,
        title_fontsize=22,
        hud_fontsize=20,
        progress_bar_height=16
    ),
    "desktop_16_9": VideoPreset(
        name="desktop_16_9",
        width=1280,
        height=720,
        caption_fontsize=64,
        title_fontsize=26,
        hud_fontsize=22,
        progress_bar_height=14
    ),
    "vertical_full_hd": VideoPreset(
        name="vertical_full_hd",
        width=1080,
        height=1920,
        caption_fontsize=84,
        title_fontsize=32,
        hud_fontsize=28,
        progress_bar_height=24
    )
}

# Default ADHD Audio Parameters
DEFAULT_8D_FREQ_HZ = 0.18        # Gentle 5.5-second rotation period
DEFAULT_8D_AMOUNT = 0.85         # 85% modulation depth (avoids complete single-ear muting)
DEFAULT_SPEED = 1.20             # Optimal cognitive stimulation speed
DEFAULT_LOUDNORM = "I=-16:TP=-1.5:LRA=11" # Broadcast standard speech loudness
