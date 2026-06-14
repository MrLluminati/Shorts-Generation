from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "build_gta_grand_rp_shorts.py"
PROJECT = "gta_v_grand_rp_driving_batch"
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
    "#gta5 #gtav #gtarp #grandrp #gta5rp #gtadriving #gtacars "
    "#hindigaming #indiangaming #pcgaming #gamingclips #shorts"
)
BASE_TAGS = (
    "gta v, gta 5, grand rp, gta rp, gta 5 roleplay, gta v roleplay, "
    "gta grand rp hindi, gta driving, gta car drive, gta cars, gta highway, "
    "gta city driving, hindi gaming, indian gaming, pc gameplay india, gta shorts, gaming shorts"
)
DESCRIPTION_SUFFIX = (
    "More GTA V Grand RP Hindi driving, roleplay, and money-grind highlights on MrLluminati Gaming."
)


@dataclass(frozen=True)
class DrivingShort:
    slug: str
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
    DrivingShort(
        slug="01_coastal_highway_pull",
        start="00:03:30.000",
        duration=48.0,
        hook="COASTAL HIGHWAY\nPULL",
        title="Coastal Highway Pull | GTA V Grand RP Hindi #shorts",
        description="A clean sunset highway pull from the opening Grand RP money-grind route.",
        tags=f"{BASE_TAGS}, gta coastal highway, gta sunset drive, gta highway pull, grand rp drive",
        pinned_comment="Clean highway run or risky speed?",
        thumbnail_text="HIGHWAY PULL",
        upload_order=1,
    ),
    DrivingShort(
        slug="02_tunnel_speed_run",
        start="00:05:30.000",
        duration=45.0,
        hook="TUNNEL SPEED\nRUN",
        title="Tunnel Speed Run Went Wild | GTA V Grand RP #shorts",
        description="The route turns into a fast tunnel-to-highway run before the road gets messy.",
        tags=f"{BASE_TAGS}, gta tunnel drive, gta speed run, gta highway driving, grand rp route",
        pinned_comment="Would you slow down here or keep pushing?",
        thumbnail_text="TUNNEL RUN",
        upload_order=2,
    ),
    DrivingShort(
        slug="03_mountain_road_entry",
        start="00:07:00.000",
        duration=43.0,
        hook="MOUNTAIN ROAD\nENTRY",
        title="Mountain Road Entry | GTA V Grand RP Hindi #shorts",
        description="A clean mountain-road stretch from the GTA V Grand RP driving route.",
        tags=f"{BASE_TAGS}, gta mountain road, gta mountain drive, grand rp car route, gta scenic drive",
        pinned_comment="Best GTA roads: city streets or mountain roads?",
        thumbnail_text="MOUNTAIN ROAD",
        upload_order=3,
    ),
    DrivingShort(
        slug="04_lumber_job_arrival",
        start="00:07:38.000",
        duration=39.0,
        hook="FOREST ROAD\nARRIVAL",
        title="Forest Road Arrival | GTA V Grand RP #shorts",
        description="The drive leaves the highway and cuts into the forest job area.",
        tags=f"{BASE_TAGS}, gta forest drive, grand rp lumberjack, gta job route, gta offroad entry",
        pinned_comment="This job route looked peaceful until the grind started.",
        thumbnail_text="FOREST ROUTE",
        upload_order=4,
    ),
    DrivingShort(
        slug="05_hospital_city_run",
        start="00:51:40.000",
        duration=55.0,
        hook="CITY RUN TO\nHOSPITAL",
        title="City Run To Hospital | GTA V Grand RP Hindi #shorts",
        description="A sunset city drive into the hospital area during the Grand RP stream.",
        tags=f"{BASE_TAGS}, gta hospital drive, gta city route, grand rp city drive, gta sunset city",
        pinned_comment="That city route was clean. Would you take the same road?",
        thumbnail_text="CITY RUN",
        upload_order=5,
    ),
    DrivingShort(
        slug="06_downtown_sunset_drive",
        start="00:55:05.000",
        duration=44.0,
        hook="DOWNTOWN SUNSET\nDRIVE",
        title="Downtown Sunset Drive | GTA V Grand RP #shorts",
        description="A short downtown driving stretch with the sunset hitting the streets.",
        tags=f"{BASE_TAGS}, gta downtown drive, gta sunset drive, gta city driving, grand rp cars",
        pinned_comment="GTA sunset driving always hits different.",
        thumbnail_text="SUNSET DRIVE",
        upload_order=6,
    ),
    DrivingShort(
        slug="07_city_lane_cut",
        start="00:58:05.000",
        duration=55.0,
        hook="CITY LANES\nGOT TIGHT",
        title="City Lanes Got Tight | GTA V Grand RP Hindi #shorts",
        description="A tighter city-lane drive before the damaged car stop.",
        tags=f"{BASE_TAGS}, gta tight lanes, gta damaged car, gta city drive, grand rp route",
        pinned_comment="Clean control or too close to traffic?",
        thumbnail_text="TIGHT LANES",
        upload_order=7,
    ),
    DrivingShort(
        slug="08_night_city_cruise",
        start="02:16:00.000",
        duration=43.0,
        hook="NIGHT CITY\nCRUISE",
        title="Night City Cruise | GTA V Grand RP #shorts",
        description="A night-time Grand RP city cruise with clean road movement from the later stream.",
        tags=f"{BASE_TAGS}, gta night drive, gta city cruise, gta night city, grand rp night drive",
        pinned_comment="Night driving or sunset driving in GTA?",
        thumbnail_text="NIGHT CRUISE",
        upload_order=8,
    ),
    DrivingShort(
        slug="09_rural_road_flip",
        start="01:44:10.000",
        duration=25.0,
        hook="RURAL ROAD\nALMOST FLIPPED",
        title="Rural Road Almost Flipped | GTA V Grand RP #shorts",
        description="A short rural-road moment where the car nearly flips during the Grand RP route.",
        tags=f"{BASE_TAGS}, gta near flip, gta rural road, gta driving fail, grand rp driving",
        pinned_comment="Saved it or pure luck?",
        thumbnail_text="ALMOST FLIPPED",
        upload_order=9,
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
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


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
                "thumbnail_text": short.thumbnail_text,
            }
        )

    csv_path = META_DIR / "gta_v_grand_rp_driving_shorts_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# GTA V Grand RP Driving Shorts Pack", ""]
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
                f"- Thumbnail text: {row['thumbnail_text']}",
                "",
            ]
        )
    (META_DIR / "gta_v_grand_rp_driving_shorts_metadata.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GTA V Grand RP driving Shorts.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local stream MP4")
    parser.add_argument("--only", nargs="*", help="Optional slug list to rerender")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    base = load_base_module()
    ffmpeg = base.imageio_ffmpeg.get_ffmpeg_exe()

    selected = [short for short in SHORTS if not args.only or short.slug in set(args.only)]
    if args.only and len(selected) != len(set(args.only)):
        known = ", ".join(short.slug for short in SHORTS)
        raise SystemExit(f"Unknown slug in --only. Known slugs: {known}")

    short_paths: dict[str, Path] = {
        short.slug: SHORT_DIR / f"{short.slug}.mp4" for short in SHORTS if (SHORT_DIR / f"{short.slug}.mp4").exists()
    }
    for short in selected:
        print(f"Rendering driving short: {short.slug}")
        out_path = base.render_short(ffmpeg, source, short)
        short_paths[short.slug] = out_path
        base.review_frames(ffmpeg, out_path, short.slug, short.duration)
        base.review_contact_sheet(ffmpeg, out_path, short.slug, short.duration)

    missing = [short.slug for short in SHORTS if short.slug not in short_paths]
    if missing:
        raise SystemExit(f"Missing rendered shorts: {', '.join(missing)}")

    write_metadata(short_paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
