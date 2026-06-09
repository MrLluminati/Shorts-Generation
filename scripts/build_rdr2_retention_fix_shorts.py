from __future__ import annotations

import csv
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "build_rdr2_live_outputs.py"
PROJECT = "rdr2_hindi_story_free_roam_retention_fix"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

SOURCE = Path(
    r"C:\Users\abhik\Downloads\Red Dead Redemption 2 (Hindi) LIVE _ Story Mode + Free Roam _ Indian PC Gameplay 🔴.mp4"
)

BASE_HASHTAGS = (
    "#rdr2 #reddeadredemption2 #rdr2hindi #hindigaming #indiangaming "
    "#pcgaming #storymode #gaminghighlights #gamingclips #shorts"
)
BASE_TAGS = (
    "red dead redemption 2, rdr2, rdr2 hindi, red dead redemption 2 hindi, "
    "indian pc gameplay, hindi gaming, mrlluminati gaming, rdr2 story mode, "
    "arthur morgan, rdr2 shorts, rdr2 gameplay, gaming shorts india"
)


@dataclass(frozen=True)
class FixedShort:
    slug: str
    start: str
    duration: float
    hook: str
    title: str
    description: str
    tags: str
    pinned_comment: str
    upload_order: int
    replaces: str


FIXED_SHORTS = [
    FixedShort(
        slug="01_snow_camp_ambush_v2",
        start="00:53:56.000",
        duration=22.0,
        hook="SNOW CAMP\nAMBUSH",
        title="Snow Camp Ambush Got Brutal | RDR2 Hindi #shorts",
        description="A tighter RDR2 Hindi snow camp ambush cut with the action starting immediately.",
        tags=f"{BASE_TAGS}, rdr2 snow camp, rdr2 ambush, rdr2 shootout, odriscoll camp",
        pinned_comment="Should this mission be played stealthy or full chaos?",
        upload_order=1,
        replaces="01_first_snow_shootout.mp4",
    ),
    FixedShort(
        slug="02_odriscoll_camp_push_v2",
        start="00:54:54.000",
        duration=21.0,
        hook="ARTHUR PUSHED\nTHE CAMP",
        title="Arthur Pushed The Camp Fight | RDR2 Hindi #shorts",
        description="The snow camp fight trimmed into a fast action beat from the RDR2 Hindi stream.",
        tags=f"{BASE_TAGS}, arthur morgan fight, rdr2 camp fight, rdr2 odriscoll, rdr2 gunfight",
        pinned_comment="Would you rush the camp like this or stay behind cover?",
        upload_order=2,
        replaces="02_looted_everyone_after_fight.mp4",
    ),
    FixedShort(
        slug="03_train_jump_v2",
        start="01:38:42.000",
        duration=21.0,
        hook="JUMP ON\nTHE TRAIN",
        title="Arthur Jumped Onto The Train | RDR2 Hindi #shorts",
        description="The train robbery starts with the clean train jump moment, not a slow lead-in.",
        tags=f"{BASE_TAGS}, rdr2 train robbery, arthur train jump, rdr2 train mission, rdr2 hindi live",
        pinned_comment="This train jump is still cinematic. Clean mission start?",
        upload_order=3,
        replaces="03_train_robbery_started_bad.mp4",
    ),
    FixedShort(
        slug="04_train_fight_v2",
        start="01:41:08.000",
        duration=24.0,
        hook="TRAIN SHOOTOUT\nSTARTED",
        title="The Train Shootout Started Fast | RDR2 Hindi #shorts",
        description="A tighter RDR2 train shootout cut that starts on the readable gunfight instead of the slow setup.",
        tags=f"{BASE_TAGS}, rdr2 train fight, rdr2 train robbery, rdr2 gunfight, arthur morgan",
        pinned_comment="Best RDR2 mission type: train robbery or camp shootout?",
        upload_order=4,
        replaces="03_train_robbery_started_bad.mp4",
    ),
]


def load_base_module():
    spec = importlib.util.spec_from_file_location("rdr2_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def make_contact_sheet(module, ffmpeg: str, video_path: Path, slug: str, duration: float) -> None:
    frames_dir = REVIEW_DIR / f"{slug}_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    stamps = [0.8, duration * 0.33, duration * 0.66, max(1.0, duration - 1.0)]
    for index, stamp in enumerate(stamps):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        module.run(
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
    module.run(
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


def write_metadata(paths: dict[str, Path]) -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in FIXED_SHORTS:
        rows.append(
            {
                "upload_order": item.upload_order,
                "file": paths[item.slug].name,
                "replaces": item.replaces,
                "source_start": item.start,
                "duration_seconds": item.duration,
                "title": item.title,
                "description": f"{item.description} Watch more Hindi gameplay highlights on MrLluminati Gaming.",
                "hashtags": BASE_HASHTAGS,
                "tags": item.tags,
                "pinned_comment": item.pinned_comment,
            }
        )

    csv_path = META_DIR / "rdr2_retention_fix_shorts_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# RDR2 Retention Fix Shorts", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Replaces: {row['replaces']}",
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
    (META_DIR / "rdr2_retention_fix_shorts_metadata.md").write_text("\n".join(md_lines), encoding="utf-8")


def main() -> None:
    module = load_base_module()
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    module.SHORT_DIR = SHORT_DIR
    module.META_DIR = META_DIR
    module.WORK_DIR = WORK_DIR
    module.REVIEW_DIR = REVIEW_DIR
    module.ASS_DIR = ASS_DIR

    ffmpeg = module.imageio_ffmpeg.get_ffmpeg_exe()
    output_paths: dict[str, Path] = {}
    for item in FIXED_SHORTS:
        short = module.ShortSpec(
            slug=item.slug,
            start=item.start,
            duration=item.duration,
            hook=item.hook,
            beats=(),
            title=item.title,
            description=item.description,
            tags=item.tags,
            pinned_comment=item.pinned_comment,
            upload_order=item.upload_order,
        )
        print(f"Rendering fixed short: {item.slug}")
        output_paths[item.slug] = module.render_short(ffmpeg, SOURCE, short)
        module.review_frames(ffmpeg, output_paths[item.slug], item.slug, item.duration)
        make_contact_sheet(module, ffmpeg, output_paths[item.slug], item.slug, item.duration)

    write_metadata(output_paths)
    print(f"Fixed shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
