# -*- mode: python ; coding: utf-8 -*-
"""Reproducible PyInstaller one-folder (onedir) specification for VoiceForge Studio v1.0.2.

Why one-folder (onedir) instead of --onefile:
1. Faster startup: Avoids unpacking hundreds of megabytes of Qt6, ONNX Runtime, FFmpeg,
   and Piper binaries into %TEMP% on every launch.
2. Subprocess reliability: Piper (`piper.exe`) and FFmpeg (`ffmpeg.exe` / `ffprobe.exe`)
   execute directly from stable paths (`vendor/ffmpeg/`, `bin/ffmpeg/`, `vendor/piper/`, `bin/piper/`)
   without antivirus false positives caused by self-extracting temp executables.
3. Single-EXE end-user experience is provided by `installer/VoiceForgeStudio.nsi`, which
   packages this entire `dist/VoiceForgeStudio/` directory into `VoiceForgeStudio_Setup_v1.0.2_x64.exe`.
"""

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

SPEC_ROOT = Path(SPECPATH).resolve()
SRC_DIR = SPEC_ROOT / "src"

datas = [
    (str(SPEC_ROOT / "README.md"), "."),
    (str(SPEC_ROOT / "LICENSES.md"), "."),
    (str(SPEC_ROOT / "THIRD_PARTY_NOTICES.md"), "."),
    (str(SPEC_ROOT / "SBOM.json"), "."),
    (str(SPEC_ROOT / "CHANGELOG.md"), "."),
]

assets_dir = SPEC_ROOT / "assets"
if assets_dir.exists():
    datas.append((str(assets_dir), "assets"))

# Pre-staged vendor binaries & default voice model (en_US-libritts-high, CC BY 4.0):
# - vendor/ffmpeg/ (ffmpeg.exe, ffprobe.exe, LICENSE.txt, FFMPEG_NOTICE.txt) -> bundled in both vendor/ffmpeg and bin/ffmpeg
# - vendor/piper/  (piper.exe, espeak-ng-data, *.dll, LICENSE.md) -> bundled in both vendor/piper and bin/piper
# - vendor/models/piper/ (en_US-libritts-high.onnx, .onnx.json, MODEL_CARD.txt) -> bundled in bundled_models/piper
vendor_ffmpeg = SPEC_ROOT / "vendor" / "ffmpeg"
if vendor_ffmpeg.exists() and any(vendor_ffmpeg.iterdir()):
    datas.append((str(vendor_ffmpeg), "vendor/ffmpeg"))
    datas.append((str(vendor_ffmpeg), "bin/ffmpeg"))

bin_ffmpeg = SPEC_ROOT / "bin" / "ffmpeg"
if bin_ffmpeg.exists() and any(bin_ffmpeg.iterdir()) and not (vendor_ffmpeg.exists() and any(vendor_ffmpeg.iterdir())):
    datas.append((str(bin_ffmpeg), "vendor/ffmpeg"))
    datas.append((str(bin_ffmpeg), "bin/ffmpeg"))

vendor_piper = SPEC_ROOT / "vendor" / "piper"
if vendor_piper.exists() and any(vendor_piper.iterdir()):
    datas.append((str(vendor_piper), "vendor/piper"))
    datas.append((str(vendor_piper), "bin/piper"))

bin_piper = SPEC_ROOT / "bin" / "piper"
if bin_piper.exists() and any(bin_piper.iterdir()) and not (vendor_piper.exists() and any(vendor_piper.iterdir())):
    datas.append((str(bin_piper), "vendor/piper"))
    datas.append((str(bin_piper), "bin/piper"))

vendor_models = SPEC_ROOT / "vendor" / "models" / "piper"
if vendor_models.exists() and any(vendor_models.iterdir()):
    datas.append((str(vendor_models), "bundled_models/piper"))

bundled_models_local = SPEC_ROOT / "bundled_models" / "piper"
if bundled_models_local.exists() and any(bundled_models_local.iterdir()) and not (
    vendor_models.exists() and any(vendor_models.iterdir())
):
    datas.append((str(bundled_models_local), "bundled_models/piper"))

binaries = []

# Collect python-docx default XML templates
try:
    datas += collect_data_files("docx")
except Exception:
    pass

# Collect ONNX Runtime shared libraries (.dll / .pyd) for 64-bit CPU inference
try:
    binaries += collect_dynamic_libs("onnxruntime")
except Exception:
    pass

# Collect piper-tts / espeak-ng data if installed as a Python package in .venv
try:
    datas += collect_data_files("piper")
    binaries += collect_dynamic_libs("piper")
except Exception:
    pass

hiddenimports = [
    "sqlite3",
    "wave",
    "numpy",
    "onnxruntime",
    "onnxruntime.capi._pybind_state",
    "docx",
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "PySide6.QtMultimedia",
]
hiddenimports += collect_submodules("voiceforge")

try:
    hiddenimports += collect_submodules("piper")
except Exception:
    pass

excludes = [
    "pytest",
    "unittest",
    "tkinter",
    "matplotlib",
    "scipy",
    "pandas",
    "selenium",
    "tests",
]

icon_file = SPEC_ROOT / "assets" / "voiceforge.ico"
version_file = SPEC_ROOT / "installer" / "file_version_info.txt"

a = Analysis(
    [str(SPEC_ROOT / "app.py")],
    pathex=[str(SRC_DIR), str(SPEC_ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VoiceForgeStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to prevent Windows Defender / SmartScreen false-positive heuristics
    console=False,  # GUI subsystem: launches window directly with no console prompt
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="x86_64",
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_file) if icon_file.exists() else None,
    version=str(version_file) if version_file.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="VoiceForgeStudio",
)
