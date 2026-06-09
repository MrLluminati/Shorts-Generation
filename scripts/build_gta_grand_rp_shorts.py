from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


PROJECT = "gta_v_grand_rp_money_grind"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE = Path(
    r"C:\Users\abhik\Downloads\🔴 LIVE_ GTA V Grand RP - Zero to Millionaire Empire Grind _ Money Making.mp4"
)

BASE_HASHTAGS = (
    "#gta5 #gtav #gtarp #grandrp #gta5rp #hindigaming #indiangaming "
    "#pcgaming #gamingclips #moneygrind #shorts"
)
BASE_TAGS = (
    "gta v, gta 5, grand rp, gta rp, gta 5 roleplay, gta v roleplay, "
    "gta grand rp hindi, hindi gaming, indian gaming, pc gameplay india, "
    "money grind, millionaire grind, gta rp money, gta shorts, gaming shorts"
)
DESCRIPTION_SUFFIX = "Watch more GTA V Grand RP Hindi gameplay and money-grind highlights on MrLluminati Gaming."


@dataclass(frozen=True)
class ShortSpec:
    slug: str
    start: str
    duration: float
    hook: str
    title: str
    description: str
    tags: str
    pinned_comment: str
    upload_order: int


SHORTS = [
    ShortSpec(
        slug="01_helicopter_job_started",
        start="00:28:18.000",
        duration=27.0,
        hook="HELICOPTER JOB\nSTARTED",
        title="Helicopter Job Started | GTA V Grand RP #shorts",
        description="The money grind starts with a helicopter pickup in GTA V Grand RP.",
        tags=f"{BASE_TAGS}, gta helicopter, grand rp job, gta rp job, gta money making",
        pinned_comment="Would you take the helicopter job or grind another way?",
        upload_order=1,
    ),
    ShortSpec(
        slug="02_mountain_money_run",
        start="00:28:55.000",
        duration=29.0,
        hook="MOUNTAIN MONEY\nRUN",
        title="Mountain Money Run In GTA RP | Grand RP #shorts",
        description="A helicopter money-run across the mountains during the Grand RP stream.",
        tags=f"{BASE_TAGS}, gta mountain flight, gta helicopter job, grand rp money run",
        pinned_comment="This looked risky. Easy money or bad idea?",
        upload_order=2,
    ),
    ShortSpec(
        slug="03_rooftop_landing",
        start="00:41:38.000",
        duration=28.0,
        hook="ROOFTOP LANDING\nGOT TIGHT",
        title="Rooftop Landing Got Tight | GTA V Grand RP #shorts",
        description="A tight helicopter landing during the GTA V Grand RP millionaire grind.",
        tags=f"{BASE_TAGS}, gta helicopter landing, gta rooftop landing, grand rp helicopter",
        pinned_comment="Clean landing or too close?",
        upload_order=3,
    ),
    ShortSpec(
        slug="04_supercar_price_check",
        start="00:43:16.000",
        duration=30.0,
        hook="SUPERCAR PRICES\nARE CRAZY",
        title="Checking Supercar Prices In GTA RP | Grand RP #shorts",
        description="The millionaire grind hits the car market, and the prices are not friendly.",
        tags=f"{BASE_TAGS}, gta car market, gta supercar, grand rp car prices, gta millionaire grind",
        pinned_comment="Which car would you buy first in Grand RP?",
        upload_order=4,
    ),
    ShortSpec(
        slug="05_money_exchange_decision",
        start="01:21:18.000",
        duration=25.0,
        hook="MONEY EXCHANGE\nDECISION",
        title="Money Exchange Decision | GTA V Grand RP #shorts",
        description="The grind pauses for a money exchange decision in GTA V Grand RP.",
        tags=f"{BASE_TAGS}, gta money exchange, grand rp exchange, gta rp economy, gta money grind",
        pinned_comment="Spend it now or save for the bigger play?",
        upload_order=5,
    ),
    ShortSpec(
        slug="06_air_taxi_takeoff",
        start="01:22:18.000",
        duration=31.0,
        hook="AIR TAXI\nTAKEOFF",
        title="Air Taxi Takeoff In Grand RP | GTA V #shorts",
        description="Back to the helicopter for another city run during the Grand RP money grind.",
        tags=f"{BASE_TAGS}, gta air taxi, gta helicopter, grand rp city flight, gta rp transport",
        pinned_comment="Would you pay for air taxi travel in GTA RP?",
        upload_order=6,
    ),
    ShortSpec(
        slug="07_trading_market_meetup",
        start="02:50:28.000",
        duration=33.0,
        hook="TRADING MARKET\nMEETUP",
        title="Trading Market Meetup | GTA V Grand RP #shorts",
        description="A Grand RP trading market stop during the zero-to-millionaire grind.",
        tags=f"{BASE_TAGS}, gta trading market, grand rp trading, gta rp marketplace, gta roleplay",
        pinned_comment="Trading market grind: smart money or slow money?",
        upload_order=7,
    ),
    ShortSpec(
        slug="08_cold_beer_shop_deal",
        start="03:16:02.000",
        duration=28.0,
        hook="SHOP DEAL\nSTARTED",
        title="Shop Deal Started In GTA RP | Grand RP #shorts",
        description="A late-stream shop interaction from the GTA V Grand RP money-making run.",
        tags=f"{BASE_TAGS}, gta shop deal, grand rp shop, gta rp business, gta business grind",
        pinned_comment="Would you invest in a shop first or a vehicle first?",
        upload_order=8,
    ),
]


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_short_ass(short: ShortSpec) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        (
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
            "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
        ),
        "Style: Logo,Arial,28,&H00FFFFFF,&H000000FF,&HAA000000,&HAA000000,-1,0,0,0,100,100,2,0,1,2,0,8,40,40,34,1",
        "Style: Hook,Arial Black,68,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,54,54,180,1",
        "Style: Lower,Arial Black,36,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,1,2,70,70,196,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 8,{ass_time(0)},{ass_time(short.duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.25)},{ass_time(3.8)},Hook,,0,0,0,,"
            r"{\fad(80,220)\t(0,320,\fscx108\fscy108)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 7,{ass_time(max(0, short.duration - 5.8))},{ass_time(max(0, short.duration - 0.7))},Lower,,0,0,0,,"
            r"{\fad(120,220)}GTA V GRAND RP HINDI"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, source: Path, short: ShortSpec) -> Path:
    ass_path = write_short_ass(short)
    out_path = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.45)
    video_filter = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.06:saturation=0.88[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "setsar=1,"
        "drawbox=x=0:y=650:w=1080:h=3:color=white@0.12:t=fill,"
        "drawbox=x=0:y=1267:w=1080:h=3:color=white@0.12:t=fill,"
        "vignette=PI/5,noise=alls=3:allf=t+u,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.16,"
        f"fade=t=out:st={fade_out:.3f}:d=0.45,"
        "format=yuv420p[v]"
    )
    audio_filter = (
        "[0:a]aresample=48000,highpass=f=70,volume=1.08,alimiter=limit=0.95,"
        f"afade=t=in:st=0:d=0.12,afade=t=out:st={fade_out:.3f}:d=0.45[a]"
    )
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            short.start,
            "-t",
            f"{short.duration:.3f}",
            "-i",
            str(source),
            "-filter_complex",
            f"{video_filter};{audio_filter}",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-r",
            "30",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            str(out_path),
        ]
    )
    return out_path


def review_frames(ffmpeg: str, video_path: Path, slug: str, duration: float) -> None:
    for label, stamp in {"hook": 1.0, "middle": duration * 0.5, "end": max(1.0, duration - 1.5)}.items():
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{stamp:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(REVIEW_DIR / f"{slug}_{label}.jpg"),
            ]
        )


def review_contact_sheet(ffmpeg: str, video_path: Path, slug: str, duration: float) -> None:
    frames_dir = REVIEW_DIR / f"{slug}_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    stamps = [0.8, duration * 0.33, duration * 0.66, max(1.0, duration - 1.0)]
    for index, stamp in enumerate(stamps):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{stamp:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(frame),
            ]
        )
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
            str(frames_dir / "frame_%03d.jpg"),
            "-vf",
            "tile=2x2",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(REVIEW_DIR / f"{slug}_contact.jpg"),
        ]
    )


def write_metadata(short_paths: dict[str, Path]) -> None:
    rows = []
    for short in SHORTS:
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": short_paths[short.slug].name,
                "source_start": short.start,
                "duration_seconds": short.duration,
                "title": short.title,
                "description": f"{short.description} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
            }
        )
    csv_path = META_DIR / "gta_v_grand_rp_shorts_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# GTA V Grand RP Shorts Pack", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
                f"- Source start: {row['source_start']}",
                f"- Duration: {row['duration_seconds']}s",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                "",
            ]
        )
    (META_DIR / "gta_v_grand_rp_shorts_metadata.md").write_text("\n".join(md_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GTA V Grand RP Shorts.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local stream MP4")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    short_paths: dict[str, Path] = {}
    for short in SHORTS:
        print(f"Rendering short: {short.slug}")
        out_path = render_short(ffmpeg, source, short)
        short_paths[short.slug] = out_path
        review_frames(ffmpeg, out_path, short.slug, short.duration)
        review_contact_sheet(ffmpeg, out_path, short.slug, short.duration)

    write_metadata(short_paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
