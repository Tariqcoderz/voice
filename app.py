#!/usr/bin/env python3
"""Entrypoint for VoiceForge Studio — Simple Local-First AI Voiceover Generator.

Supports:
- Standard graphical desktop launch (`VoiceForgeStudio.exe` or `python app.py`)
- Startup verification (`--check-startup`)
- Strict end-to-end packaged build smoke-test (`--smoke-test [--smoke-test-report <file>]`)
- Frozen PyInstaller Piper CLI subprocess worker (`--piper-cli-worker ...`)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def _run_piper_cli_worker(worker_args: list[str]) -> int:
    """Execute the `piper` Python module CLI when invoked as `VoiceForgeStudio.exe --piper-cli-worker`."""
    sys.argv = ["piper", *worker_args]
    try:
        from piper.__main__ import main as piper_main

        piper_main()
        return 0
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 0
    except Exception as exc:
        sys.stderr.write(f"Piper worker error: {exc}\n")
        return 1


def run_packaged_smoke_test(
    window: object,
    report_path: Optional[Path] = None,
    expected_voice_id: str = "en_US-libritts-high",
    require_bundled_binaries: bool = False,
) -> int:
    """Run a strict end-to-end packaged-build acceptance smoke test.

    Required acceptance criteria (fails if any criterion is unmet):
    1. Actual PySide6 desktop application (not HeadlessQtFallback).
    2. Working bundled FFmpeg and FFprobe with libmp3lame MP3 encoder.
    3. Actual Piper neural engine and intended bundled/installed voice model (default: en_US-libritts-high).
       Never substitutes Flite or system TTS when reporting Piper neural synthesis.
    4. Generation of real speech from a test script via Piper.
    5. Valid final WAV export.
    6. Valid final MP3 export.
    7. Application startup from an installed/data path containing spaces.
    """
    from voiceforge import __app_name__, __version__
    from voiceforge.core.audio_processing import AudioProcessor
    from voiceforge.core.diagnostics import collect_environment_diagnostics
    from voiceforge.core.runtime_paths import (
        find_bundled_only_executable,
        get_app_install_dir,
        is_frozen_build,
        is_path_within_app_bundle,
    )
    from voiceforge.ui.main_window import VoiceForgeMainWindow
    from voiceforge.ui.qt_compat import QT_BACKEND, USING_PYSIDE6

    assert isinstance(window, VoiceForgeMainWindow)
    enforce_bundle = bool(is_frozen_build() or require_bundled_binaries)
    install_dir = get_app_install_dir()
    data_dir = window.config_manager.dirs.root_dir

    report: dict[str, object] = {
        "app_name": __app_name__,
        "version": __version__,
        "test_type": "end_to_end_packaged_smoke_test",
        "ui_mode": "single_screen_elevenlabs_style",
        "qt_backend": QT_BACKEND,
        "using_pyside6": USING_PYSIDE6,
        "pyside6_desktop_verified": False,
        "is_frozen_build": is_frozen_build(),
        "enforce_bundled_binaries": enforce_bundle,
        "install_dir": str(install_dir),
        "data_dir": str(data_dir),
        "space_in_path_startup_verified": False,
        "ffmpeg_executable": "",
        "ffprobe_executable": "",
        "ffmpeg_bundled_in_package": False,
        "ffprobe_bundled_in_package": False,
        "ffmpeg_and_ffprobe_working": False,
        "libmp3lame_encoder_verified": False,
        "piper_engine_available": False,
        "piper_executable_or_module": "",
        "target_neural_voice_id": expected_voice_id,
        "target_neural_voice_installed": False,
        "piper_neural_synthesis_verified": False,
        "synthesized_engine": "",
        "synthesized_voice_id": "",
        "master_audio_duration_sec": 0.0,
        "wav_exported": False,
        "mp3_exported": False,
        "status": "FAIL",
        "errors": [],
    }
    errors: list[str] = []

    try:
        diags = collect_environment_diagnostics(window.config_manager)
        report["diagnostics"] = diags

        # 1. Verify actual PySide6 desktop GUI (never pass on HeadlessQtFallback)
        if USING_PYSIDE6 and QT_BACKEND == "PySide6":
            report["pyside6_desktop_verified"] = True
        else:
            errors.append(
                f"Actual PySide6 desktop application is required for packaged smoke test, "
                f"but active backend is '{QT_BACKEND}' (USING_PYSIDE6={USING_PYSIDE6})."
            )

        # 2. Verify application startup from a path containing spaces
        if " " in str(install_dir) and " " in str(data_dir):
            report["space_in_path_startup_verified"] = True
        else:
            space_test_root = Path(tempfile.mkdtemp(prefix="VoiceForge Space Path Check "))
            try:
                space_data_dir = space_test_root / "Installed User Data With Spaces"
                space_window = VoiceForgeMainWindow(data_root=space_data_dir)
                space_window.show()
                if space_window.isVisible() and space_window.config_manager.dirs.settings_path.exists():
                    report["space_in_path_startup_verified"] = True
                else:
                    errors.append("Application startup verification on a path containing spaces failed.")
                space_window.shutdown_cleanly()
                space_window.close()
            except Exception as space_exc:
                errors.append(f"Startup from path containing spaces raised error: {space_exc}")
            finally:
                shutil.rmtree(space_test_root, ignore_errors=True)

        if enforce_bundle and " " not in str(install_dir):
            errors.append(
                f"Packaged smoke test requires launching from an installation path containing spaces, "
                f"but install_dir is '{install_dir}'."
            )
            report["space_in_path_startup_verified"] = False

        # 3. Verify working bundled FFmpeg and FFprobe with libmp3lame
        ffmpeg_ok, ffmpeg_msg, mp3_ok = AudioProcessor.check_ffmpeg_availability(
            window.config_manager.settings.ffmpeg_executable_path,
            window.config_manager.settings.ffprobe_executable_path,
        )
        resolved_ffmpeg = AudioProcessor.resolve_ffmpeg(window.config_manager.settings.ffmpeg_executable_path)
        resolved_ffprobe = AudioProcessor.resolve_ffprobe(window.config_manager.settings.ffprobe_executable_path)
        bundled_ffmpeg = find_bundled_only_executable("ffmpeg")
        bundled_ffprobe = find_bundled_only_executable("ffprobe")

        report["ffmpeg_executable"] = resolved_ffmpeg
        report["ffprobe_executable"] = resolved_ffprobe
        report["ffmpeg_bundled_in_package"] = bool(
            bundled_ffmpeg is not None and is_path_within_app_bundle(bundled_ffmpeg)
        )
        report["ffprobe_bundled_in_package"] = bool(
            bundled_ffprobe is not None and is_path_within_app_bundle(bundled_ffprobe)
        )
        report["ffmpeg_and_ffprobe_working"] = bool(ffmpeg_ok)
        report["libmp3lame_encoder_verified"] = bool(mp3_ok)

        if not ffmpeg_ok:
            errors.append(f"FFmpeg and FFprobe verification failed: {ffmpeg_msg}")
        if not mp3_ok:
            errors.append("FFmpeg is missing required 'libmp3lame' MP3 encoder.")
        if enforce_bundle:
            if not report["ffmpeg_bundled_in_package"]:
                errors.append(
                    "Bundled ffmpeg executable was not found inside the application package (vendor/ffmpeg or bin/ffmpeg)."
                )
            if not report["ffprobe_bundled_in_package"]:
                errors.append(
                    "Bundled ffprobe executable was not found inside the application package (vendor/ffmpeg or bin/ffmpeg)."
                )

        # 4. Verify actual Piper neural engine & intended bundled/installed voice model
        piper_diag = window.piper_engine.check_installation()
        report["piper_engine_available"] = bool(piper_diag.available)
        report["piper_executable_or_module"] = piper_diag.executable_or_module
        if not piper_diag.available:
            errors.append(f"Piper neural TTS engine is not available: {piper_diag.message}")

        installed_voices = window.voice_catalog.get_installed_voices()
        report["installed_voices_count"] = len(installed_voices)
        report["installed_voice_ids"] = [v.voice_id for v in installed_voices]

        target_voice = window.voice_catalog.get_voice_by_id(expected_voice_id)
        if (
            target_voice is not None
            and target_voice.engine == "piper"
            and target_voice.is_neural
            and target_voice.is_available_for_synthesis
        ):
            report["target_neural_voice_installed"] = True
        else:
            errors.append(
                f"Required Piper neural voice '{expected_voice_id}' is not installed/verified "
                f"(installed voices: {[v.voice_id for v in installed_voices]}). "
                f"Refusing to substitute Flite or system TTS for Piper neural synthesis."
            )

        # 5. Generate real speech via Piper neural engine and verify WAV + MP3 exports
        if report["piper_engine_available"] and report["target_neural_voice_installed"]:
            window.populate_installed_voices()
            combo_idx = window.voice_combo.findData(expected_voice_id)
            if combo_idx < 0:
                errors.append(f"Voice '{expected_voice_id}' was not selectable in the narration dropdown.")
            else:
                window.voice_combo.setCurrentIndex(combo_idx)
                selected_voice = window.get_selected_voice_profile()
                if selected_voice is None or selected_voice.engine != "piper":
                    errors.append(
                        f"Selected voice '{ getattr(selected_voice, 'voice_id', None) }' is not using the Piper neural engine."
                    )
                else:
                    script_text = (
                        "Welcome to VoiceForge Studio. Paste your script, choose a voice, and click Generate Voiceover.\n\n"
                        "This packaged smoke test verifies real local Piper neural speech synthesis, WAV export, and MP3 encoding."
                    )
                    window.script_editor.setPlainText(script_text)
                    started = window.start_simple_generation(force_regenerate=True)
                    if not started:
                        errors.append("Failed to start single-screen Piper voiceover generation.")
                    else:
                        window.task_manager.wait_all(timeout=90.0)
                        if (
                            window.current_master_wav
                            and window.current_master_wav.exists()
                            and window.output_panel.isVisible()
                        ):
                            master_info = AudioProcessor.inspect_audio_file(window.current_master_wav)
                            peaks = AudioProcessor.compute_waveform_peaks(window.current_master_wav, 32)
                            max_peak = max(peaks) if peaks else 0.0
                            if (
                                master_info.valid
                                and master_info.duration_seconds > 1.0
                                and max_peak > 0.01
                            ):
                                report["piper_neural_synthesis_verified"] = True
                                report["synthesized_engine"] = selected_voice.engine
                                report["synthesized_voice_id"] = selected_voice.voice_id
                                report["master_audio_duration_sec"] = round(master_info.duration_seconds, 3)

                                with tempfile.TemporaryDirectory(dir=window.config_manager.dirs.temp_dir) as tmp_exp:
                                    out_dir = Path(tmp_exp)
                                    # 5a. Required WAV export
                                    wav_file = window.export_master_to_destination(
                                        out_dir / "smoke_test.wav", fmt="wav"
                                    )
                                    if wav_file and wav_file.exists():
                                        wav_info = AudioProcessor.inspect_audio_file(wav_file)
                                        if wav_info.valid and wav_info.duration_seconds > 1.0 and wav_info.size_bytes > 10000:
                                            report["wav_exported"] = True
                                        else:
                                            errors.append(
                                                f"Exported WAV validation failed: {wav_info.error_message or 'invalid duration/size'}"
                                            )
                                    else:
                                        errors.append("Required WAV download/export failed during smoke test.")

                                    # 5b. Required MP3 export (never skip silently!)
                                    mp3_file = window.export_master_to_destination(
                                        out_dir / "smoke_test.mp3", fmt="mp3"
                                    )
                                    if mp3_file and mp3_file.exists():
                                        mp3_info = AudioProcessor.inspect_audio_file(mp3_file)
                                        if mp3_info.valid and mp3_info.duration_seconds > 1.0 and mp3_info.size_bytes > 4000:
                                            report["mp3_exported"] = True
                                        else:
                                            errors.append(
                                                f"Exported MP3 validation failed: {mp3_info.error_message or 'invalid duration/size'}"
                                            )
                                    else:
                                        errors.append("Required MP3 download/export failed during smoke test.")
                            else:
                                errors.append(
                                    f"Generated master WAV did not pass speech verification "
                                    f"(valid={master_info.valid}, duration={master_info.duration_seconds}s, "
                                    f"max_peak={max_peak:.4f})."
                                )
                        else:
                            errors.append(
                                f"Master audio not ready after Piper generation (status='{window.lbl_status_message.text()}')."
                            )
    except Exception as exc:
        errors.append(str(exc))

    all_required_passed = bool(
        not errors
        and report["pyside6_desktop_verified"]
        and report["space_in_path_startup_verified"]
        and report["ffmpeg_and_ffprobe_working"]
        and report["libmp3lame_encoder_verified"]
        and report["piper_engine_available"]
        and report["target_neural_voice_installed"]
        and report["piper_neural_synthesis_verified"]
        and report["wav_exported"]
        and report["mp3_exported"]
    )
    if enforce_bundle:
        all_required_passed = bool(
            all_required_passed
            and report["ffmpeg_bundled_in_package"]
            and report["ffprobe_bundled_in_package"]
        )

    report["errors"] = errors
    report["status"] = "PASS" if all_required_passed else "FAIL"

    if report_path is not None:
        report_path = Path(report_path).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    try:
        print(json.dumps(report, indent=2))
    except Exception:
        pass

    return 0 if all_required_passed else 1


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if raw_argv and raw_argv[0] == "--piper-cli-worker":
        return _run_piper_cli_worker(raw_argv[1:])

    from voiceforge import __app_id__, __app_name__, __version__
    from voiceforge.ui.main_window import VoiceForgeMainWindow
    from voiceforge.ui.qt_compat import QT_BACKEND, USING_PYSIDE6, QApplication

    parser = argparse.ArgumentParser(
        description=f"{__app_name__} v{__version__} — Local-First AI Voiceover Generator"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="",
        help="Optional custom application data directory path.",
    )
    parser.add_argument(
        "--check-startup",
        action="store_true",
        help="Initialize main window, run startup verification, and exit cleanly.",
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run strict end-to-end packaged application smoke test and exit.",
    )
    parser.add_argument(
        "--smoke-test-report",
        type=str,
        default="",
        help="Optional JSON file path to write the --smoke-test report.",
    )
    parser.add_argument(
        "--expected-voice-id",
        type=str,
        default="en_US-libritts-high",
        help="Expected Piper neural voice ID for --smoke-test (default: en_US-libritts-high).",
    )
    parser.add_argument(
        "--require-bundled-binaries",
        action="store_true",
        help="Require ffmpeg/ffprobe to reside inside the application package bundle.",
    )
    args = parser.parse_args(raw_argv)

    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(__app_id__)
        except Exception:
            pass

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setOrganizationName("VoiceForge")

    data_root = Path(args.data_dir).expanduser().resolve() if args.data_dir else None
    window = VoiceForgeMainWindow(data_root=data_root)
    window.show()

    if args.check_startup:
        try:
            print(
                f"[OK] {__app_name__} v{__version__} initialized (UI backend={QT_BACKEND}, "
                f"installed_voices={len(window.voice_catalog.get_installed_voices())})"
            )
        except Exception:
            pass
        window.shutdown_cleanly()
        window.close()
        return 0

    if args.smoke_test:
        rep_path = Path(args.smoke_test_report) if args.smoke_test_report else None
        code = run_packaged_smoke_test(
            window,
            report_path=rep_path,
            expected_voice_id=args.expected_voice_id,
            require_bundled_binaries=args.require_bundled_binaries,
        )
        window.shutdown_cleanly()
        window.close()
        return code

    if not USING_PYSIDE6:
        try:
            print(
                f"[NOTICE] PySide6 is not installed in this Python environment. "
                f"{__app_name__} v{__version__} initialized in headless mode ({QT_BACKEND}).\n"
                f"On Windows 10/11, install via VoiceForgeStudio_Setup_v1.0.2_x64.exe or run scripts\\setup_windows.bat."
            )
        except Exception:
            pass
        window.shutdown_cleanly()
        return 0

    exit_code = app.exec()
    window.shutdown_cleanly()
    return int(exit_code)


if __name__ == "__main__":
    sys.exit(main())
