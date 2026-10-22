# VoiceForge Studio v1.0.2 — Third-Party Legal Notices, Licenses & Source Offer

This installer and application bundle (`VoiceForge Studio v1.0.2`) incorporates distinct software components, runtime libraries, and optional voice model checkpoints that are governed by separate licenses.

**IMPORTANT NOTICE:** The complete installer bundle is **not** covered by a single MIT license. Each component listed below retains its own license and copyright terms.

## 1. VoiceForge Studio Application Code
- **Component:** `src/voiceforge/`, `app.py`, `installer/`, `scripts/`
- **Copyright:** Copyright (c) 2026 VoiceForge Engineering
- **License:** MIT License

## 2. Piper TTS Engine (`GPL-3.0-or-later` / `MIT`)
- **Active Upstream Repository:** https://github.com/OHF-Voice/piper1-gpl (PyPI: `piper-tts`)
- **Original Archive Repository:** https://github.com/rhasspy/piper
- **License:** `GPL-3.0-or-later` (for `OHF-Voice/piper1-gpl` >= 1.3.0 and `espeak-ng` phonemizer integration) / `MIT License` (for `rhasspy/piper` <= 1.2.0).
- **Bundling & Corresponding Source Code Offer (GPLv3 Section 6):**
  Piper is executed by VoiceForge Studio as a separate command-line process (`vendor\piper\piper.exe`, `bin\piper\piper.exe`, or `--piper-cli-worker`). When `VoiceForgeStudio_Setup_v1.0.2_x64.exe` is distributed with `piper` / `espeak-ng` binaries, the complete corresponding machine-readable source code and build scripts are available from:
  - https://github.com/OHF-Voice/piper1-gpl
  - https://github.com/rhasspy/piper
  - https://github.com/espeak-ng/espeak-ng
  A copy of the GNU General Public License v3.0 is included in the installation folder and release bundle.

## 3. PySide6 / Qt for Python (`LGPL-3.0-only`)
- **Upstream:** https://pypi.org/project/PySide6/ (The Qt Company Ltd.)
- **License:** GNU Lesser General Public License v3.0 (`LGPL-3.0-only`)
- **Dynamic Linking Notice:** VoiceForge Studio dynamically loads unmodified PySide6 / Qt6 shared libraries (`.dll` / `.pyd` files inside `_internal\PySide6\`). Users may replace or relink these shared libraries in accordance with LGPL-3.0 terms.

## 4. FFmpeg & FFprobe Media Tools (`GPL v3` / `LGPL v2.1+`)
- **Upstream Project:** https://ffmpeg.org/legal.html
- **Windows x64 Build Source:** https://github.com/BtbN/FFmpeg-Builds (`ffmpeg-master-latest-win64-gpl.zip`)
- **License:** GNU General Public License v3 (`GPL v3`) when compiled with `--enable-gpl --enable-version3 --enable-libmp3lame` (required for `libmp3lame` MP3 encoding).
- **Process Separation & Source Availability:** VoiceForge Studio invokes `ffmpeg.exe` and `ffprobe.exe` strictly as standalone external command-line executables (`vendor\ffmpeg\ffmpeg.exe` / `bin\ffmpeg\ffmpeg.exe`). FFmpeg is not linked into the VoiceForge Studio binary. Complete FFmpeg source code and build scripts are available at https://git.ffmpeg.org/ffmpeg.git and https://github.com/BtbN/FFmpeg-Builds, and build metadata is included in `vendor\ffmpeg\FFMPEG_NOTICE.txt`.

## 5. ONNX Runtime (`MIT License`), NumPy (`BSD-3-Clause`), python-docx (`MIT License`)
- **ONNX Runtime:** Copyright (c) Microsoft Corporation — MIT License (https://github.com/microsoft/onnxruntime)
- **NumPy:** Copyright (c) NumPy Developers — BSD 3-Clause License (https://numpy.org/doc/stable/license.html)
- **python-docx:** Copyright (c) Steve Canny — MIT License (https://github.com/python-openxml/python-docx)

## 6. Default Bundled / Recommended Neural Voice Model Attribution (`CC BY 4.0`)
When bundled with or downloaded via VoiceForge Studio, the default English voice model is:
- **Model Identifier:** `en_US-libritts-high`
- **Model Card URL:** https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts/high/MODEL_CARD
- **Training Dataset & Provenance:** LibriTTS `train-clean-360` (http://www.openslr.org/60/; Zen et al., 2019, derived from Public Domain LibriSpeech/LibriVox audiobooks). Upstream `MODEL_CARD` explicitly states: *"Trained from scratch on train-clean-360."*
- **Dataset & Model License:** Creative Commons Attribution 4.0 International (`CC BY 4.0`, https://creativecommons.org/licenses/by/4.0/)
- **Required Attribution:**
  *"Voice model `en_US-libritts-high` trained from scratch by Michael Hansen (Rhasspy / Piper project) on the LibriTTS `train-clean-360` dataset (Zen et al., Google Research, http://www.openslr.org/60/, CC BY 4.0)."*

## 7. Notice on Other Downloadable Voice Models (Including `en_US-libritts_r-medium`)
Not all models in `rhasspy/piper-voices` have verified standalone commercial rights:
- **`en_US-libritts_r-medium` (`License Review Required`):** Although the LibriTTS-R dataset is `CC BY 4.0`, its upstream `MODEL_CARD` states that the checkpoint was **fine-tuned from English Lessac (medium)**. Because the Lessac base checkpoint was trained on the Blizzard Challenge 2013 non-commercial research dataset, `en_US-libritts_r-medium` is marked **License Review Required** and is not bundled as the default commercial voice.
- **`en_US-lessac-medium` & `en_US-hfc_female-medium` (`Restricted`):** Restricted to **non-commercial** use (Blizzard Challenge 2013 research license and `CC BY-NC-SA 4.0`, respectively).
- **Models fine-tuned from `lessac` (`en_US-amy-medium`, `en_US-ryan-medium`) or with dataset terms requiring verification (`en_GB-cori-medium`, `ur_PK-fasih-medium`, `ur_PK-aegis_female-medium`):** Marked **License Review Required**.
