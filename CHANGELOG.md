# Changelog

## [1.0.2] - 2026-10-20
### Added & Improved
- **Simple Single-Screen Redesign**: Streamlined the main interface into one clean, beginner-friendly screen (`Header` → `Script Input` → `Narration Voice Selector` → `Generate Voiceover` → `Final Audio Player & WAV/MP3 Download`) while keeping the output player hidden until valid audio is ready.
- **10,000-Word Hidden Pipeline (`SimpleVoiceoverPipeline`)**: Automatic paragraph/sentence/word chunking, SHA-256 chunk caching for instant retry/resume, sequential CPU-friendly background synthesis, and low-RAM disk-streamed WAV merging (`AudioProcessor.combine_clips`).
- **GitHub Actions Windows x64 Installer Workflow Fixes (`.github/workflows/build_windows_installer.yml`)**:
  - Added explicit NSIS installation via Chocolatey (`choco install nsis --yes --no-progress`) and `makensis.exe` path/version verification.
  - Added explicit download, extraction, execution verification, and `libmp3lame` encoder check for Windows x64 `ffmpeg.exe` and `ffprobe.exe` in `vendor/ffmpeg/` (`BtbN/FFmpeg-Builds`), plus `vendor/ffmpeg/FFMPEG_NOTICE.txt`.
  - Switched the bundled default voice to `en_US-libritts-high` (trained from scratch on LibriTTS `train-clean-360`, `CC BY 4.0`) and reclassified `en_US-libritts_r-medium` as `License Review Required` because its upstream model card notes fine-tuning from English Lessac medium.
  - Strengthened `app.py --smoke-test` to require native `PySide6` (not `HeadlessQtFallback`), real Piper neural speech generation with `en_US-libritts-high` (never substituting Flite/system TTS), valid WAV and MP3 exports, working bundled `ffmpeg`/`ffprobe` with `libmp3lame`, and startup from an installed path containing spaces.

## [1.0.1] - 2026-10-20
- Initial Windows desktop release with multi-tab interface, Piper ONNX + System TTS adapters, and SQLite project persistence.
