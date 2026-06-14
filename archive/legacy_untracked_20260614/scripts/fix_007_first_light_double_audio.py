from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


PROJECT = "007_first_light_20260612"
PIPELINE = ROOT / "live_video_pipeline"
LONG_DIR = PIPELINE / "long_form" / PROJECT
SHORT_DIR = PIPELINE / "short_form" / PROJECT

# OBS baked two near-identical inputs into one stereo track. The secondary peak
# measured consistently around 38 ms, so this subtracts a delayed copy to reduce
# the doubled/echo sound while keeping the original video stream untouched.
AUDIO_FIX = (
    "[0:a]aresample=48000,asplit=2[dry][del];"
    "[del]adelay=38|38,volume=-0.45[neg];"
    "[dry][neg]amix=inputs=2:normalize=0,volume=1.12,alimiter=limit=0.95[a]"
)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def targets(include_shorts: bool) -> list[Path]:
    paths = sorted(LONG_DIR.glob("007_first_light_hindi_part_*.mp4"))
    if include_shorts:
        paths.extend(sorted(SHORT_DIR.glob("*.mp4")))
    return paths


def fix_file(ffmpeg: str, path: Path) -> None:
    tmp = path.with_name(f"{path.stem}.audiofix.tmp{path.suffix}")
    if tmp.exists():
        tmp.unlink()
    print(f"Fixing audio: {path.name}", flush=True)
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-filter_complex",
            AUDIO_FIX,
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            str(tmp),
        ]
    )
    run([ffmpeg, "-v", "error", "-i", str(tmp), "-f", "null", "-"])
    path.unlink()
    tmp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Reduce baked-in 38 ms OBS double-audio echo for 007 outputs.")
    parser.add_argument("--include-shorts", action="store_true", help="Also fix rendered Shorts.")
    parser.add_argument("--dry-run", action="store_true", help="Print target files without changing them.")
    args = parser.parse_args()

    paths = targets(args.include_shorts)
    if not paths:
        raise SystemExit("No target MP4 files found.")
    if args.dry_run:
        for path in paths:
            print(path)
        return

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    for path in paths:
        fix_file(ffmpeg, path)
    print("Audio fix complete.", flush=True)


if __name__ == "__main__":
    main()
