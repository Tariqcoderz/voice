# Third-Party Software & Voice Model Licensing Notice (`LICENSES.md`)

VoiceForge Studio strictly separates **application software licensing**, **TTS engine software licensing**, and **per-voice dataset/model weights licensing**.

> **CRITICAL COMMERCIAL USE RULE:**
> Never infer commercial or monetized YouTube usage rights for generated audio from a software license alone, from a dataset license when a model was fine-tuned from a restricted base checkpoint, or from the fact that a voice model is freely downloadable. Always inspect the specific voice model card, base checkpoint lineage, and underlying training dataset license.

## 1. TTS Engine & Media Software Licenses

| Component | Upstream Repository / Source | Software License | Notes |
| :--- | :--- | :--- | :--- |
| **Piper TTS (Active Fork)** | [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl) / [piper-tts on PyPI](https://pypi.org/project/piper-tts/) | `GPL-3.0-or-later` | Active maintenance successor to `rhasspy/piper`. Executed as a standalone subprocess or CLI module. |
| **Piper TTS (Original Archive)** | [rhasspy/piper](https://github.com/rhasspy/piper) | `MIT License` | Archived in October 2025 (releases up to `v1.2.0`). |
| **ONNX Runtime** | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) / [onnxruntime on PyPI](https://pypi.org/project/onnxruntime/) | `MIT License` | Local CPU neural inference engine. |
| **PySide6 (Qt for Python)** | [PySide6 on PyPI](https://pypi.org/project/PySide6/) | `LGPL-3.0-only` | Dynamically linked desktop UI framework. |
| **FFmpeg & FFprobe** | [FFmpeg.org](https://ffmpeg.org/legal.html) / [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds) | `GPL v3` (when compiled with `--enable-gpl --enable-version3 --enable-libmp3lame`) / `LGPL v2.1+` | Invoked strictly as an external CLI binary (`vendor\ffmpeg\ffmpeg.exe` / `ffprobe.exe`). |
| **Windows System SAPI5** | [Microsoft Speech API](https://learn.microsoft.com/en-us/windows/win32/sapi/microsoft-speech-api-sapi-5-3) | [Microsoft Windows Retail License Terms](https://www.microsoft.com/en-us/Useterms/Retail/Windows/10/UseTerms_Retail_Windows_10_English.htm) | Built into Windows 10/11; commercial redistribution of SAPI output requires user review of Microsoft license terms. |
| **CMU Flite (Fallback)** | [festvox/flite](https://github.com/festvox/flite/blob/master/COPYING) | Permissive BSD-style License | Non-neural fallback synthesizer. |

## 2. Piper Voice Models (`rhasspy/piper-voices`) Per-Model Licensing

Voice models hosted in [rhasspy/piper-voices on Hugging Face](https://huggingface.co/rhasspy/piper-voices) do **not** all share the same license. Although the Hugging Face repository wrapper lists MIT for scripts/metadata, each `.onnx` checkpoint is governed by its training dataset and base checkpoint lineage:

| Voice ID | Language | Dataset & Training Lineage | Upstream License | VoiceForge Commercial Status | Model Card Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `en_US-libritts-high` | English (US) | LibriTTS `train-clean-360` (**Trained from scratch**, OpenSLR SLR60) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | **Verified** (Default Bundled Voice; Attribution required) | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts/high/MODEL_CARD) |
| `en_US-libritts_r-medium` | English (US) | LibriTTS-R (**Fine-tuned from English Lessac medium**) | CC BY 4.0 Dataset / Lessac Base Checkpoint | **License Review Required** (Base Lessac model is non-commercial Blizzard 2013) | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/en/en_US/libritts_r/medium/MODEL_CARD) |
| `en_US-lessac-medium` | English (US) | Lessac Blizzard Challenge 2013 | [Blizzard 2013 Non-Commercial Research License](https://www.synsig.org/index.php/Blizzard_Challenge_2013) | **Restricted** (Non-Commercial Only) | [Model Directory](https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/medium) |
| `en_US-hfc_female-medium` | English (US) | Hi-Fi CAPTAIN (NICT), finetuned from `lessac` | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en) | **Restricted** (Non-Commercial Only) | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/en/en_US/hfc_female/medium/MODEL_CARD) |
| `en_US-amy-medium` | English (US) | Mycroft Mimic3, finetuned from `lessac` | See [MycroftAI/mimic3-voices](https://github.com/MycroftAI/mimic3-voices) | **License Review Required** | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/en/en_US/amy/medium/MODEL_CARD) |
| `en_US-ryan-medium` | English (US) | RyanSpeech, finetuned from `lessac` | Dataset + `lessac` base checkpoint terms | **License Review Required** | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/en/en_US/ryan/medium/MODEL_CARD) |
| `en_GB-cori-medium` | English (UK) | Cori (`en_GB`) | Dataset terms in Model Card | **License Review Required** | [Commit / Model Card](https://huggingface.co/rhasspy/piper-voices/commit/5fc01c2e94761ab2a335bd9384037bdd6e17baed) |
| `ur_PK-fasih-medium` | Urdu (Pakistan) | Urdu Male Voice (Fasih) | MIT declared in Model Card frontmatter | **License Review Required** (Verify dataset provenance) | [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/main/ur/ur_PK/fasih/medium/MODEL_CARD) |
| `ur_PK-aegis_female-medium` | Urdu (Pakistan) | Urdu Female Voice (Aegis) | MIT declared in Model Card frontmatter | **License Review Required** (Verify dataset provenance) | [Commit / Model Card](https://huggingface.co/rhasspy/piper-voices/commit/57f060450c13802c4c1475f5a9807e516796c015) |

## 3. Excluded Non-Commercial Engines

- **Coqui XTTS-v2** is intentionally excluded as a default engine because the Coqui Public Model License (CPML) restricts use to non-commercial purposes unless a separate commercial license is obtained.
