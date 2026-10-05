# 🧠 ADHD 8D Study Video Generator (`adhd-8d`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)
[![GPU Acceleration](https://img.shields.io/badge/Hardware-GPU%20Accelerated-76B900.svg)](https://github.com/AA967-LLM/adhd-8d-study-video-generator)
[![Open Source](https://img.shields.io/badge/Open%20Source-Heart-red.svg)](https://github.com/AA967-LLM/adhd-8d-study-video-generator)

> **Convert ANY lecture, audiobook, tutorial, or podcast into a high-retention 8D audio and kinetic visual loop study experience.**  
> Built for neurodivergent minds, ADHD learners, and anyone struggling with mid-sentence mental drifting and academic fatigue.

---

## 🔬 Cognitive Neuroscience Foundation

Traditional monologues and dry lectures trigger rapid cognitive fatigue. In ADHD brains, low tonic dopamine in the prefrontal cortex allows the **Default Mode Network (DMN)**—the brain's internal daydreaming circuit—to overpower the **Task Positive Network (TPN)** every 8 to 12 seconds.

This project implements evidence-based cognitive psychology principles (**Optimal Stimulation Theory** by Zentall, 1975; Sweller's Cognitive Load Theory) through 5 sensory pillars:

```
                  ┌──────────────────────────────────────────────┐
                  │          Raw Audio / Video Lecture           │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
                 ▼                                               ▼
    [Auditory Stimulation]                           [Visual Anchoring]
   - 0.18 Hz 8D Bilateral Sweep                    - Silent Continuous Motion Loop
   - Speech Tempo Pacing (1.20x)                     (Kinetic / Spatial Motion Flow)
   - EBU R128 Loudness Normalization               - Dead-Center XXL Captions (2-4 words)
                 │                                 - Glowing Cyan Dynamic Progress Bar
                 │                                 - Real-Time Elapsed / Total HUD
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │    High-Retention ADHD Study Video Loop      │
                  │        (Hardware-Accelerated 50x)            │
                  └──────────────────────────────────────────────┘
```

1. **8D Bilateral Relocalization:** Acoustic energy oscillates across headphones in a gentle 0.18 Hz sine wave (~5.5-second rotation). The brainstem's superior olivary complex must constantly recalculate interaural time differences (ITD), preventing the auditory cortex from tuning out.
2. **Sensory Dual-Channel Pairing:** A silent, predictable background motion loop occupies the visual channel so the auditory channel can absorb dense information without visual distractions.
3. **Time-Blindness Cure (Dynamic HUD):** A glowing `#00E5FF` cyan progress bar (0% to 100%) and live countdown timer provide continuous dopamine micro-feedback.
4. **Cognitive Text Offloading (XXL Kinetic Captions):** Word-timed, 2-to-4 word bursts rendered in 58–64pt Arial Black directly at the screen's dead center eliminate eye fatigue from paragraph scanning.
5. **Speech Pacing (1.15x–1.35x):** Eliminates conversational pauses, hesitations, and vocal drag to match active neurodivergent processing speeds.

---

## ⚡ Quick Start

### 1. Prerequisites
- **FFmpeg** on system `PATH` (with `libass` and optional hardware video encoder support):
  ```bash
  # Windows (via winget)
  winget install Gyan.FFmpeg
  
  # Ubuntu / Debian
  sudo apt update && sudo apt install ffmpeg libass-dev
  ```
- **Python 3.9+** (with optional GPU acceleration).

### 2. Installation
```bash
git clone https://github.com/AA967-LLM/adhd-8d-study-video-generator.git
cd adhd-8d-study-video-generator
pip install -e .
```

---

## 🚀 CLI Usage

### A. Convert Audio Only to 8D Spatial MP3
Turn any lecture or podcast into an 8D headphone experience:
```bash
adhd-8d -i lecture.m4a -o lecture_8D.mp3 --speed 1.20
```

### B. Generate Full ADHD Study Video (Zero External Files Needed)
Automatically uses the built-in **100% open-source procedural motion loop** (infinite Mandelbrot fractal zoom or 3D starfield warp) with zero external video dependencies:
```bash
adhd-8d \
  -i lecture.m4a \
  -o study_session.mp4 \
  --title "Distributed Systems: Architectural Deep Dive" \
  --procedural-style fractal
```

### C. Use a Custom Background Motion Loop
You can also supply your own custom background video loop:
```bash
adhd-8d \
  -i lecture.m4a \
  -b my_motion_loop.mp4 \
  -o study_session.mp4 \
  --title "Advanced Algorithms Deep Dive" \
  --speed 1.20 \
  --preset mobile_9_16
```

### D. Convert PDFs or Written Tutorials into 8D Study Videos
Extract structured text, parse tables into spoken narratives, synthesize spoken neural narration, and output complete 8D audio and video loops:
```bash
# Convert a PDF article or book chapter (auto-extracts headings, paragraphs, and tables)
adhd-8d -i document.pdf -o study_session.mp4 --title "Distributed Systems Deep Dive"

# Convert a markdown or text tutorial with a custom neural voice
adhd-8d -i tutorial.md -o tutorial_8D.mp4 --voice en-US-ChristopherNeural

# Ingest complex multi-column documents or invoices (runs 100% locally and offline)
adhd-8d -i invoice_with_tables.pdf -o financial_breakdown.mp4
```

### E. Available Options
| Argument | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | *Required* | Path to input audio (`.mp3`, `.m4a`), video (`.mp4`), PDF (`.pdf`), or text (`.md`, `.txt`) |
| `--background` | `-b` | Built-in | Path to custom background video (`.mp4`). If omitted, uses built-in open-source procedural loop |
| `--procedural-style` | | `fractal` | Built-in procedural background (`fractal` or `starfield`) |
| `--voice` | | `en-US-ChristopherNeural` | Neural voice model for PDF/text speech synthesis |
| `--output` | `-o` | Auto | Destination path (`.mp4`, `.mp3`, `.m4a`) |
| `--title` | `-t` | "Study Session" | Title overlay banner text |
| `--speed` | `-s` | `1.20` | Audio pacing multiplier (1.0x to 1.5x) |
| `--freq` | | `0.18` | 8D rotation frequency in Hz (0.18 Hz = 5.5s) |
| `--amount` | | `0.85` | 8D spatial modulation depth (0.0 to 1.0) |
| `--preset` | | `mobile_9_16` | Resolution preset (`mobile_9_16`, `desktop_16_9`, `vertical_full_hd`) |
| `--whisper-model`| | `base` | Model size (`tiny`, `base`, `small`, `medium`, `large-v3`) |
| `--device` | | `cuda` | Transcription device (`cuda` or `cpu`) |
| `--strip-silence`| | False | Strip dead air longer than 0.4s |
| `--audio-only` | | False | Export only the 8D audio track |
| `--no-hud` | | False | Disable bottom progress bar and timer HUD |

---

## 💻 Python API Usage

```python
from adhd_8d.audio_engine import process_8d_audio
from adhd_8d.transcriber import transcribe_and_format_captions
from adhd_8d.video_engine import render_study_video

# 1. Transform audio to 8D with pacing
duration = process_8d_audio(
    input_path="lecture.m4a",
    output_path="lecture_8D.mp3",
    speed=1.20,
    freq_hz=0.18,
    amount=0.85
)

# 2. Transcribe on GPU and format kinetic captions
transcribe_and_format_captions(
    audio_path="lecture_8D.mp3",
    ass_output="captions.ass",
    preset_name="mobile_9_16"
)

# 3. Render GPU study video loop with HUD
render_study_video(
    background_video="motion_loop.mp4",
    audio_path="lecture_8D.mp3",
    ass_subtitles="captions.ass",
    output_video="study_video.mp4",
    duration=duration,
    title="Systems Architecture Breakdown",
    preset_name="mobile_9_16"
)
```

---

## ⚖️ Legal Compliance, Trademark Notice & Liability Shield

- **License:** Open-sourced under the permissive [MIT License](LICENSE).
- **Absolute Limitation of Liability:** THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY. Read the full [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md).
- **Not Medical Advice:** This software is an experimental assistive study tool and does not constitute medical, psychiatric, or clinical advice or treatment for ADHD or neurological conditions.
- **Copyright & Content Rights:** Users are solely responsible for ensuring they possess all necessary copyrights, licenses, or fair-use rights for any audio, video, or font files processed by this tool. The authors do not host or distribute proprietary courseware or copyrighted gameplay footage.
- **Blanket Trademark Notice:** All product names, logos, trademarks, and registered trademarks mentioned or referenced in this software or documentation are property of their respective owners. No affiliation, endorsement, or sponsorship is implied.

---

## 🤝 Contributing

Contributions, bug reports, and pull requests are warmly welcome!
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👤 Author
**Adeel Ahmad**  
GitHub: [@AA967-LLM](https://github.com/AA967-LLM)  
Email: [adeelahmad967@gmail.com](mailto:adeelahmad967@gmail.com)
