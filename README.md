# VoiceForge Studio v1.0.2 — Simple Local AI Voiceover Generator

**VoiceForge Studio** is a clean, beginner-friendly Windows 10/11 (64-bit) desktop application that turns written scripts into complete voiceover narration on your computer—with **no cloud subscriptions, no API keys, and no technical setup**.

## How to Use VoiceForge Studio

1. **Open VoiceForge Studio** from your Desktop or Start Menu shortcut.
2. **Paste your script** into the text box (supports short clips up to 10,000+ word documentaries in English, Urdu, and other languages where a voice is installed).
3. **Select a narration voice** from the dropdown (and click **Preview Voice** if you want to hear a sample).
4. **Click "Generate Voiceover"** and wait for the progress bar (`Preparing script...` → `Generating voiceover...` → `Finalizing audio...` → `Voiceover ready.`).
5. **Play your finished voiceover** right inside the app.
6. **Click "Download WAV" or "Download MP3"** to save the final audio file anywhere on your computer.

All long-script splitting, silence pacing, audio normalization, and file merging happen automatically behind the scenes.

## Bundled Default Neural Voice & Evidence-Based Licensing

- **Default Bundled Neural Voice (`en_US-libritts-high`):** Trained **from scratch** on the LibriTTS `train-clean-360` dataset ([OpenSLR SLR60](http://www.openslr.org/60/)) and licensed under **Creative Commons Attribution 4.0 (`CC BY 4.0`)** per its upstream [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts/high/MODEL_CARD).
- **Why `en_US-libritts_r-medium` Is Marked `License Review Required`:** Although the LibriTTS-R dataset is `CC BY 4.0`, the upstream `en_US-libritts_r-medium` model card states it was fine-tuned from English Lessac (medium), whose base dataset (Blizzard Challenge 2013) is non-commercial. Accordingly, VoiceForge Studio marks `en_US-libritts_r-medium` as **License Review Required** and bundles `en_US-libritts-high` as the verified `CC BY 4.0` default instead.
- **Bundled FFmpeg & FFprobe (`vendor/ffmpeg/`):** Includes Windows x64 `ffmpeg.exe` and `ffprobe.exe` from [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds) verified for `libmp3lame` MP3 encoding, invoked as standalone external CLI processes (`see vendor/ffmpeg/FFMPEG_NOTICE.txt` and `THIRD_PARTY_NOTICES.md`).

## End-User Windows Installation (`VoiceForgeStudio_Setup_v1.0.2_x64.exe`)

Ordinary Windows 10/11 (64-bit) users do **not** need to install Python, `pip`, `PySide6`, or FFmpeg separately:

1. **Download & Double-Click**: Run `VoiceForgeStudio_Setup_v1.0.2_x64.exe`.
   - *Code-Signing Note:* This release is not signed with a commercial Authenticode certificate. Do not disable Windows Defender or antivirus protection; verify the SHA-256 checksum against `VoiceForgeStudio_Setup_v1.0.2_x64.exe.sha256` if prompted.
2. **Follow the Setup Wizard**:
   - Default per-user installation path (`%LOCALAPPDATA%\Programs\VoiceForge Studio\`) requires no Administrator privileges.
   - Keep **Create Desktop Shortcut** checked (enabled by default).
3. **Finish & Launch**: Click **Finish** to launch **VoiceForge Studio** immediately or open it anytime from your Desktop icon.
4. **Uninstalling**: Open **Windows Settings > Apps > Installed apps**, select **VoiceForge Studio**, and click **Uninstall**. Your saved voiceovers, projects, and downloaded voice models in `%LOCALAPPDATA%\VoiceForge Studio\` are preserved unless you explicitly choose to delete them.

## Building `VoiceForgeStudio_Setup_v1.0.2_x64.exe` via GitHub Actions or Windows 10/11

Upload this bundle to a GitHub repository to run `.github/workflows/build_windows_installer.yml` on `windows-latest` (which installs NSIS via Chocolatey, downloads and verifies FFmpeg with `libmp3lame`, downloads `en_US-libritts-high`, builds and smoke-tests the PyInstaller package from a path with spaces, compiles `release/VoiceForgeStudio_Setup_v1.0.2_x64.exe`, and uploads the installer + SHA-256 checksum).

On a local Windows 10/11 x64 build machine:

```bat
scripts\build_windows_installer.bat
scripts\test_installed_build.bat
```

## Running Unit vs. Packaged End-to-End Smoke Tests

```bat
REM Unit and component test suite (runs in any Python 3.11+ environment):
python -m unittest discover -s tests -v

REM Strict packaged end-to-end smoke test (requires real PySide6, Piper, en_US-libritts-high, and bundled FFmpeg/FFprobe):
dist\VoiceForgeStudio\VoiceForgeStudio.exe --smoke-test --require-bundled-binaries --expected-voice-id en_US-libritts-high
```
