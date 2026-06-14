from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "build_gta_grand_rp_shorts.py"
PROJECT = "gta_v_grand_rp_batch_02"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"
THUMB_DIR = PIPELINE / "thumbnails" / PROJECT

SOURCE_1 = Path(
    r"C:\Users\abhik\Downloads\🔴 LIVE_ GTA V Grand RP - Zero to Millionaire Empire Grind _ Money Making (1).mp4"
)
SOURCE_2 = Path(
    r"C:\Users\abhik\Downloads\🔴 LIVE_ GTA V Grand RP - Zero to Millionaire Empire Grind _ Money Making (2).mp4"
)

BASE_HASHTAGS = (
    "#gta5 #gtav #gtarp #grandrp #gta5rp #gtadriving #gtacars "
    "#hindigaming #indiangaming #pcgaming #gamingclips #gtaonline #shorts"
)
BASE_TAGS = (
    "gta v, gta 5, gta rp, grand rp, gta 5 roleplay, gta v roleplay, "
    "gta grand rp hindi, gta driving, gta cars, gta plane job, gta helicopter, "
    "gta money grind, grand rp money, hindi gaming, indian gaming, pc gameplay india, "
    "gta shorts, gaming shorts, gta funny moments, gta rp moments"
)
DESCRIPTION_SUFFIX = (
    "More GTA V Grand RP Hindi roleplay, driving, flying, and money-grind highlights on "
    "MrLluminati Gaming."
)
THUMBNAIL_TIMESTAMPS = {
    "06_black_car_rp_pullup": 5.5,
    "07_lakeside_rp_standoff": 5.0,
    "10_ocean_chopper_pickup": 8.0,
    "11_night_plane_takeoff": 7.0,
    "12_city_lights_flyover": 5.5,
}


@dataclass(frozen=True)
class BatchShort:
    slug: str
    source_key: str
    start: str
    duration: float
    hook: str
    title: str
    description: str
    tags: str
    pinned_comment: str
    thumbnail_text: str
    upload_order: int


SHORTS = [
    BatchShort(
        slug="01_mail_delivery_run",
        source_key="source_1",
        start="00:28:18.000",
        duration=45.0,
        hook="MAIL DELIVERY\nRUN STARTED",
        title="Mail Delivery Run Started | GTA V Grand RP Hindi #shorts",
        description="A clean Grand RP mail-delivery route begins with the box truck job.",
        tags=f"{BASE_TAGS}, gta mail delivery, grand rp mail job, gta delivery truck, gta job route",
        pinned_comment="Would you grind delivery jobs first or save for a faster vehicle?",
        thumbnail_text="MAIL RUN",
        upload_order=7,
    ),
    BatchShort(
        slug="02_mail_truck_city_lanes",
        source_key="source_1",
        start="00:31:40.000",
        duration=45.0,
        hook="CITY LANES\nIN A TRUCK",
        title="City Lanes In A Delivery Truck | GTA V Grand RP #shorts",
        description="The mail truck run cuts through city traffic during the money grind.",
        tags=f"{BASE_TAGS}, gta truck driving, gta delivery job, grand rp delivery, gta city lanes",
        pinned_comment="Clean delivery driving or too slow for Shorts?",
        thumbnail_text="TRUCK LANES",
        upload_order=10,
    ),
    BatchShort(
        slug="03_airport_checkpoint_takeoff",
        source_key="source_1",
        start="00:40:07.000",
        duration=28.0,
        hook="PLANE JOB\nTAKEOFF",
        title="Plane Job Takeoff | GTA V Grand RP Hindi #shorts",
        description="The Grand RP grind switches from road jobs to a checkpoint plane job.",
        tags=f"{BASE_TAGS}, gta plane job, grand rp pilot job, gta airport takeoff, gta flying",
        pinned_comment="Plane job or road job: which grind looks better?",
        thumbnail_text="PLANE JOB",
        upload_order=5,
    ),
    BatchShort(
        slug="04_mountain_checkpoint_flight",
        source_key="source_1",
        start="00:41:10.000",
        duration=50.0,
        hook="MOUNTAIN CHECKPOINT\nRUN",
        title="Mountain Checkpoint Run | GTA V Grand RP #shorts",
        description="A fast plane checkpoint run across the mountains in Grand RP.",
        tags=f"{BASE_TAGS}, gta mountain flight, gta plane checkpoint, grand rp pilot, gta flying challenge",
        pinned_comment="Would you fly low here or play it safe?",
        thumbnail_text="MOUNTAIN RUN",
        upload_order=3,
    ),
    BatchShort(
        slug="05_runway_checkpoint_landing",
        source_key="source_1",
        start="00:52:28.000",
        duration=48.0,
        hook="RUNWAY CHECKPOINT\nGOT TIGHT",
        title="Runway Checkpoint Got Tight | GTA V Grand RP #shorts",
        description="A runway checkpoint and landing sequence from the Grand RP plane job.",
        tags=f"{BASE_TAGS}, gta runway landing, gta plane landing, grand rp airport, gta pilot job",
        pinned_comment="Clean landing or too close to the marker?",
        thumbnail_text="TIGHT RUNWAY",
        upload_order=4,
    ),
    BatchShort(
        slug="06_black_car_rp_pullup",
        source_key="source_2",
        start="00:29:55.000",
        duration=50.0,
        hook="BLACK CAR\nRP PULLUP",
        title="Black Car RP Pullup | GTA V Grand RP Hindi #shorts",
        description="A nightfall Grand RP drive ends in a lakeside roleplay pullup.",
        tags=f"{BASE_TAGS}, gta black car, gta rp meetup, grand rp roleplay, gta night drive",
        pinned_comment="This car looked clean. What would you call it?",
        thumbnail_text="RP PULLUP",
        upload_order=1,
    ),
    BatchShort(
        slug="07_lakeside_rp_standoff",
        source_key="source_2",
        start="00:37:30.000",
        duration=55.0,
        hook="LAKESIDE RP\nGOT TENSE",
        title="Lakeside RP Got Tense | GTA V Grand RP #shorts",
        description="A crowded lakeside roleplay moment during the GTA V Grand RP stream.",
        tags=f"{BASE_TAGS}, gta rp standoff, grand rp meetup, gta roleplay moment, gta lakeside rp",
        pinned_comment="Would you stay and talk or leave before it gets worse?",
        thumbnail_text="RP STANDOFF",
        upload_order=12,
    ),
    BatchShort(
        slug="08_night_highway_cruise",
        source_key="source_2",
        start="00:54:25.000",
        duration=58.0,
        hook="NIGHT HIGHWAY\nCRUISE",
        title="Night Highway Cruise | GTA V Grand RP Hindi #shorts",
        description="A clean night highway drive from the Grand RP money-grind route.",
        tags=f"{BASE_TAGS}, gta night highway, gta night drive, grand rp driving, gta car cruise",
        pinned_comment="Night drive or sunset drive in GTA RP?",
        thumbnail_text="NIGHT CRUISE",
        upload_order=2,
    ),
    BatchShort(
        slug="09_mountain_road_stop",
        source_key="source_2",
        start="01:00:00.000",
        duration=55.0,
        hook="MOUNTAIN ROAD\nSTOP",
        title="Mountain Road Stop | GTA V Grand RP #shorts",
        description="The night drive moves from highway speed into a mountain-road stop.",
        tags=f"{BASE_TAGS}, gta mountain road, gta night route, grand rp car drive, gta road trip",
        pinned_comment="Good place to stop or bad place to slow down?",
        thumbnail_text="ROAD STOP",
        upload_order=9,
    ),
    BatchShort(
        slug="10_ocean_chopper_pickup",
        source_key="source_2",
        start="01:15:05.000",
        duration=45.0,
        hook="OCEAN CHOPPER\nPICKUP",
        title="Ocean Chopper Pickup | GTA V Grand RP Hindi #shorts",
        description="A night helicopter pickup turns into an ocean flight during the Grand RP stream.",
        tags=f"{BASE_TAGS}, gta helicopter, gta ocean pickup, grand rp helicopter, gta chopper moment",
        pinned_comment="Would you trust this chopper ride at night?",
        thumbnail_text="CHOPPER PICKUP",
        upload_order=6,
    ),
    BatchShort(
        slug="11_night_plane_takeoff",
        source_key="source_2",
        start="03:00:00.000",
        duration=55.0,
        hook="NIGHT PLANE\nRUN",
        title="Night Plane Run | GTA V Grand RP #shorts",
        description="A late-stream plane job starts with a night takeoff and checkpoint route.",
        tags=f"{BASE_TAGS}, gta night flight, gta plane takeoff, grand rp pilot job, gta airport night",
        pinned_comment="Night flying looks better, but is it harder?",
        thumbnail_text="NIGHT TAKEOFF",
        upload_order=11,
    ),
    BatchShort(
        slug="12_city_lights_flyover",
        source_key="source_2",
        start="03:12:30.000",
        duration=55.0,
        hook="CITY LIGHTS\nFLYOVER",
        title="City Lights Flyover | GTA V Grand RP Hindi #shorts",
        description="A night plane route over the city lights during the Grand RP grind.",
        tags=f"{BASE_TAGS}, gta city flyover, gta night city, gta plane route, grand rp flying",
        pinned_comment="Best view in GTA RP: city lights or mountain roads?",
        thumbnail_text="CITY FLYOVER",
        upload_order=8,
    ),
]


def load_base_module():
    spec = importlib.util.spec_from_file_location("gta_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.SHORT_DIR = SHORT_DIR
    module.META_DIR = META_DIR
    module.WORK_DIR = WORK_DIR
    module.REVIEW_DIR = REVIEW_DIR
    module.ASS_DIR = ASS_DIR
    return module


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR, THUMB_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def drawtext_escape(text: str) -> str:
    return (
        text.replace("\\", r"\\")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace("%", r"\%")
    )


def font_path(name: str) -> str:
    return f"C\\:/Windows/Fonts/{name}"


def drawtext(
    text: str,
    x: int,
    y: int,
    size: int,
    color: str,
    font: str = "impact.ttf",
    border: int = 5,
) -> str:
    return (
        f"drawtext=fontfile='{font_path(font)}':"
        f"text='{drawtext_escape(text)}':"
        f"x={x}:y={y}:fontsize={size}:fontcolor={color}:"
        f"borderw={border}:bordercolor=black@0.94"
    )


def thumbnail_lines(text: str) -> tuple[str, str]:
    words = text.split()
    if len(words) <= 1:
        return text, ""
    return " ".join(words[:-1]), words[-1]


def render_thumbnail(ffmpeg: str, video_path: Path, short: BatchShort) -> Path:
    out_path = THUMB_DIR / f"{short.slug}_thumbnail.jpg"
    line1, line2 = thumbnail_lines(short.thumbnail_text)
    stamp = THUMBNAIL_TIMESTAMPS.get(
        short.slug,
        min(max(4.2, short.duration * 0.34), max(1.0, short.duration - 1.0)),
    )
    filters = [
        "scale=1080:1920:force_original_aspect_ratio=increase",
        "crop=1080:1920",
        "setsar=1",
        "eq=contrast=1.16:brightness=0.015:saturation=1.24",
        "unsharp=5:5:0.65",
        "drawbox=x=0:y=0:w=1080:h=1920:color=black@0.10:t=fill",
        "drawbox=x=0:y=1158:w=1080:h=508:color=black@0.62:t=fill",
        "drawbox=x=58:y=100:w=252:h=58:color=0xF4C430@0.98:t=fill",
        drawtext("GTA V RP", 76, 113, 34, "black", "arialbd.ttf", 1),
        "drawbox=x=58:y=170:w=438:h=8:color=white@0.96:t=fill",
        drawtext(line1, 58, 1232, 92, "white", "impact.ttf", 6),
        drawtext(line2, 58, 1352, 108, "0xF4C430", "impact.ttf", 6),
        "drawbox=x=62:y=1568:w=386:h=60:color=0x111111@0.88:t=fill",
        drawtext("HINDI STREAM", 82, 1581, 32, "white", "arialbd.ttf", 2),
        "vignette=PI/5",
        "format=yuvj420p",
    ]
    base_module = load_base_module()
    base_module.run(
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
            "-vf",
            ",".join(filters),
            "-q:v",
            "2",
            str(out_path),
        ]
    )
    return out_path


def render_thumbnails(ffmpeg: str, short_paths: dict[str, Path]) -> dict[str, Path]:
    thumbnail_paths: dict[str, Path] = {}
    for short in SHORTS:
        video_path = short_paths.get(short.slug, SHORT_DIR / f"{short.slug}.mp4")
        if video_path.exists():
            thumbnail_paths[short.slug] = render_thumbnail(ffmpeg, video_path, short)
    return thumbnail_paths


def write_metadata(short_paths: dict[str, Path]) -> None:
    rows = []
    for short in SHORTS:
        thumbnail_path = THUMB_DIR / f"{short.slug}_thumbnail.jpg"
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": short_paths[short.slug].name,
                "thumbnail": thumbnail_path.name if thumbnail_path.exists() else "",
                "source": short.source_key,
                "source_start": short.start,
                "duration_seconds": short.duration,
                "title": short.title,
                "description": f"{short.description} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )

    csv_path = META_DIR / "gta_v_grand_rp_batch_02_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# GTA V Grand RP Batch 02 Shorts", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
                f"- Source: {row['source']}",
                f"- Source start: {row['source_start']}",
                f"- Duration: {row['duration_seconds']}s",
                f"- Thumbnail: {row['thumbnail']}",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                f"- Thumbnail text: {row['thumbnail_text']}",
                "",
            ]
        )
    (META_DIR / "gta_v_grand_rp_batch_02_metadata.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GTA V Grand RP batch 02 Shorts.")
    parser.add_argument("--source-1", default=str(SOURCE_1), help="First local stream MP4")
    parser.add_argument("--source-2", default=str(SOURCE_2), help="Second local stream MP4")
    parser.add_argument("--only", nargs="*", help="Optional slug list to rerender")
    parser.add_argument("--thumbnails-only", action="store_true", help="Only render thumbnails and metadata")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Do not render thumbnail JPGs")
    args = parser.parse_args()

    ensure_dirs()
    sources = {"source_1": Path(args.source_1), "source_2": Path(args.source_2)}
    missing_sources = [str(path) for path in sources.values() if not path.exists()]
    if missing_sources:
        raise SystemExit(f"Missing source file(s): {', '.join(missing_sources)}")

    base = load_base_module()
    ffmpeg = base.imageio_ffmpeg.get_ffmpeg_exe()

    only = set(args.only or [])
    selected = [short for short in SHORTS if not only or short.slug in only]
    if only and len(selected) != len(only):
        known = ", ".join(short.slug for short in SHORTS)
        raise SystemExit(f"Unknown slug in --only. Known slugs: {known}")

    short_paths: dict[str, Path] = {
        short.slug: SHORT_DIR / f"{short.slug}.mp4"
        for short in SHORTS
        if (SHORT_DIR / f"{short.slug}.mp4").exists()
    }
    if not args.thumbnails_only:
        for short in selected:
            print(f"Rendering GTA batch 02 short: {short.slug}")
            out_path = base.render_short(ffmpeg, sources[short.source_key], short)
            short_paths[short.slug] = out_path
            base.review_frames(ffmpeg, out_path, short.slug, short.duration)
            base.review_contact_sheet(ffmpeg, out_path, short.slug, short.duration)

    missing = [short.slug for short in SHORTS if short.slug not in short_paths]
    if missing:
        raise SystemExit(f"Missing rendered shorts: {', '.join(missing)}")

    if not args.skip_thumbnails:
        print("Rendering GTA batch 02 thumbnails")
        render_thumbnails(ffmpeg, short_paths)

    write_metadata(short_paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Thumbnails: {THUMB_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
