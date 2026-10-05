#!/usr/bin/env python3
"""
Example: Programmatic usage of the adhd-8d engine.
"""

from adhd_8d.audio_engine import process_8d_audio
from adhd_8d.transcriber import transcribe_and_format_captions
from adhd_8d.video_engine import render_study_video

def main():
    audio_input = "lecture.m4a"
    background_video = "motion_loop.mp4"
    output_video = "lecture_adhd_study_session.mp4"
    ass_captions = "lecture_captions.ass"

    # Step 1: Create 8D Audio track
    duration = process_8d_audio(
        input_path=audio_input,
        output_path="lecture_8D.mp3",
        speed=1.20,
        freq_hz=0.18,
        amount=0.85
    )

    # Step 2: GPU Transcription & Centered Kinetic Captions
    transcribe_and_format_captions(
        audio_path="lecture_8D.mp3",
        ass_output=ass_captions,
        preset_name="mobile_9_16"
    )

    # Step 3: Render Final Video with Background Loop & Live HUD
    render_study_video(
        background_video=background_video,
        audio_path="lecture_8D.mp3",
        ass_subtitles=ass_captions,
        output_video=output_video,
        duration=duration,
        title="High-Retention Study Session",
        preset_name="mobile_9_16"
    )

if __name__ == "__main__":
    main()
