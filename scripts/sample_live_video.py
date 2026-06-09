from __future__ import annotations

import argparse
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


def hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create timestamped visual contact sheets for a long live video.")
    parser.add_argument("--source", required=True, help="Local video file")
    parser.add_argument("--out-dir", required=True, help="Output review directory")
    parser.add_argument("--duration", type=float, required=True, help="Video duration in seconds")
    parser.add_argument("--interval", type=int, default=120, help="Sample interval in seconds")
    parser.add_argument("--start", type=int, default=0, help="Start sampling at this timestamp in seconds")
    parser.add_argument("--end", type=int, default=0, help="Stop sampling at this timestamp in seconds; defaults to duration")
    parser.add_argument("--cols", type=int, default=5)
    parser.add_argument("--rows", type=int, default=5)
    args = parser.parse_args()

    source = Path(args.source)
    out_dir = Path(args.out_dir)
    frames_dir = out_dir / f"frames_{args.interval}s"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    end = args.end if args.end > 0 else int(args.duration)
    end = min(end, int(args.duration))
    timestamps = list(range(args.start, end, args.interval))
    if not timestamps:
        timestamps = [args.start]
    if timestamps[-1] < end - 5:
        timestamps.append(max(args.start, end - 5))

    for index, seconds in enumerate(timestamps):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        label = hms(seconds).replace(":", r"\:")
        drawtext = (
            "scale=320:180,"
            "drawbox=x=0:y=0:w=128:h=30:color=black@0.72:t=fill,"
            f"drawtext=text='{label}':x=8:y=6:fontsize=18:fontcolor=white"
        )
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{seconds:.3f}",
                "-i",
                str(source),
                "-frames:v",
                "1",
                "-vf",
                drawtext,
                "-q:v",
                "3",
                str(frame),
            ]
        )

    page_size = args.cols * args.rows
    pages = math.ceil(len(timestamps) / page_size)
    for page in range(pages):
        start = page * page_size
        count = min(page_size, len(timestamps) - start)
        page_dir = frames_dir / f"page_{page + 1:02d}"
        page_dir.mkdir(parents=True, exist_ok=True)
        for offset in range(count):
            src = frames_dir / f"frame_{start + offset:03d}.jpg"
            dst = page_dir / f"frame_{offset:03d}.jpg"
            if dst.exists():
                dst.unlink()
            dst.write_bytes(src.read_bytes())
        sheet = out_dir / f"overview_{args.interval}s_page_{page + 1:02d}.jpg"
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-framerate",
                "1",
                "-i",
                str(page_dir / "frame_%03d.jpg"),
                "-vf",
                f"tile={args.cols}x{args.rows}",
                "-frames:v",
                "1",
                "-q:v",
                "3",
                str(sheet),
            ]
        )

    print(f"Wrote {len(timestamps)} frames and {pages} contact sheet(s) to {out_dir}")


if __name__ == "__main__":
    main()
