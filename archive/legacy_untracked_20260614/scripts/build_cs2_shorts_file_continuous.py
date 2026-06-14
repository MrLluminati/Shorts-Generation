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


PROJECT = "cs2_shorts_file_continuous_20260613"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE = Path(r"C:\Users\abhik\Videos\Shorts\Shorts.mp4")

BASE_HASHTAGS = (
    "#cs2 #counterstrike2 #cs2clips #cs2shorts #ancient "
    "#fpsgaming #gamingclips #indiangaming #pcgaming #shorts"
)
BASE_TAGS = (
    "cs2, counter strike 2, cs2 shorts, cs2 clips, cs2 ancient, cs2 quick kills, "
    "cs2 reaction, cs2 aim, cs2 spray control, cs2 gameplay india, fps gaming, "
    "indian gaming, pc gameplay india, mrlluminati gaming"
)
DESCRIPTION_SUFFIX = (
    "Fast CS2 clip from MrLluminati Gaming, kept as one continuous fight window with no mixed timestamps."
)


@dataclass(frozen=True)
class ContinuousShort:
    slug: str
    start: str
    duration: float
    hook: str
    beat_one: str
    beat_two: str
    title: str
    description_lead: str
    tags: str
    pinned_comment: str
    thumbnail_text: str
    upload_order: int


SHORTS = (
    ContinuousShort(
        slug="01_first_contact_trim",
        start="00:00:03.200",
        duration=6.8,
        hook="FIRST CONTACT\nHIT FAST",
        beat_one="KEEP FIRING",
        beat_two="RESET",
        title="First Contact Hit Fast | CS2 Ancient #shorts",
        description_lead="A continuous first-contact CS2 Ancient fight window from the trimmed clip.",
        tags=f"{BASE_TAGS}, cs2 first contact, cs2 ancient fight, cs2 quick reaction",
        pinned_comment="Clean first fight or lucky timing?",
        thumbnail_text="FIRST CONTACT",
        upload_order=1,
    ),
    ContinuousShort(
        slug="02_wall_spray_trim",
        start="00:00:34.800",
        duration=7.4,
        hook="WALL SPRAY\nGOT CLEAN",
        beat_one="HOLD ANGLE",
        beat_two="MOVE OUT",
        title="Wall Spray Got Clean | CS2 Ancient #shorts",
        description_lead="A single continuous wall-angle spray fight from the trimmed CS2 clip.",
        tags=f"{BASE_TAGS}, cs2 wall spray, cs2 angle hold, cs2 ancient spray",
        pinned_comment="Would you keep holding this angle?",
        thumbnail_text="WALL SPRAY",
        upload_order=2,
    ),
    ContinuousShort(
        slug="03_low_hp_angle_trim",
        start="00:01:31.300",
        duration=8.8,
        hook="LOW HP\nANGLE HOLD",
        beat_one="NO PANIC",
        beat_two="SURVIVE",
        title="Low HP Angle Hold | CS2 Ancient #shorts",
        description_lead="A continuous low-HP angle-hold fight from the CS2 Ancient clip.",
        tags=f"{BASE_TAGS}, cs2 low hp, cs2 angle hold, cs2 ancient low hp",
        pinned_comment="Would you take this fight on low HP?",
        thumbnail_text="LOW HP HOLD",
        upload_order=3,
    ),
    ContinuousShort(
        slug="04_box_fight_trim",
        start="00:02:23.400",
        duration=8.8,
        hook="BOX FIGHT\nGOT MESSY",
        beat_one="CLOSE RANGE",
        beat_two="RELOAD FAST",
        title="Box Fight Got Messy | CS2 Ancient #shorts",
        description_lead="A continuous box-area close fight from the trimmed CS2 clip.",
        tags=f"{BASE_TAGS}, cs2 box fight, cs2 close range, cs2 ancient close fight",
        pinned_comment="Close range fight or bad position?",
        thumbnail_text="BOX FIGHT",
        upload_order=4,
    ),
    ContinuousShort(
        slug="05_wall_pressure_trim",
        start="00:02:46.100",
        duration=9.8,
        hook="WALL PRESSURE\nWAS REAL",
        beat_one="LOW HP",
        beat_two="STAY ALIVE",
        title="Wall Pressure Was Real | CS2 Ancient #shorts",
        description_lead="A continuous wall-pressure fight from the trimmed CS2 Ancient gameplay.",
        tags=f"{BASE_TAGS}, cs2 wall pressure, cs2 survival, cs2 ancient fight",
        pinned_comment="Would you fall back or fight it?",
        thumbnail_text="WALL PRESSURE",
        upload_order=5,
    ),
    ContinuousShort(
        slug="06_final_fight_trim",
        start="00:03:06.400",
        duration=14.4,
        hook="FINAL FIGHT\nGOT LOUD",
        beat_one="KEEP FIRING",
        beat_two="LAST PICK",
        title="Final Fight Got Loud | CS2 Ancient #shorts",
        description_lead="A continuous late-round CS2 fight from the trimmed Ancient clip.",
        tags=f"{BASE_TAGS}, cs2 final fight, cs2 late round, cs2 ancient final fight",
        pinned_comment="Should I upload more full fight windows like this?",
        thumbnail_text="FINAL FIGHT",
        upload_order=6,
    ),
)


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_ass(short: ContinuousShort) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    duration = short.duration
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
        "Style: Logo,Arial,30,&H00FFFFFF,&H000000FF,&H99000000,&H99000000,-1,0,0,0,100,100,1,0,1,2,0,8,48,48,42,1",
        "Style: Hook,Arial Black,76,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,7,3,8,50,50,160,1",
        "Style: Beat,Arial Black,52,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,6,2,2,70,70,240,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 6,{ass_time(0)},{ass_time(duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.08)},{ass_time(min(2.0, duration - 0.5))},Hook,,0,0,0,,"
            r"{\fad(50,120)\t(0,180,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 8,{ass_time(3.0)},{ass_time(min(4.7, duration - 0.8))},Beat,,0,0,0,,"
            r"{\fad(60,120)}"
            f"{ass_escape(short.beat_one)}"
        ),
        (
            f"Dialogue: 8,{ass_time(max(4.9, duration - 2.7))},{ass_time(duration - 0.45)},Beat,,0,0,0,,"
            r"{\fad(60,150)}"
            f"{ass_escape(short.beat_two)}"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, source: Path, short: ContinuousShort) -> Path:
    ass_path = write_ass(short)
    output = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.20)
    video_filter = (
        "[0:v]fps=30,split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=24:1,eq=brightness=-0.10:saturation=1.08[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=655:w=1080:h=3:color=white@0.14:t=fill,"
        "drawbox=x=0:y=1262:w=1080:h=3:color=white@0.14:t=fill,"
        "eq=contrast=1.06:saturation=1.10:brightness=0.006,"
        "unsharp=5:5:0.42:3:3:0.18,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.04,"
        f"fade=t=out:st={fade_out:.3f}:d=0.20,"
        "format=yuv420p[v]"
    )
    audio_filter = (
        "[0:a]aresample=48000,highpass=f=65,"
        "acompressor=threshold=-18dB:ratio=2.6:attack=8:release=120,"
        "volume=1.10,alimiter=limit=0.95,"
        "afade=t=in:st=0:d=0.04,"
        f"afade=t=out:st={fade_out:.3f}:d=0.20[a]"
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
            "18",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    return output


def make_review_assets(ffmpeg: str, video_path: Path, short: ContinuousShort) -> None:
    frame_dir = REVIEW_DIR / "frames" / short.slug
    frame_dir.mkdir(parents=True, exist_ok=True)
    for label, second in (
        ("hook", 0.6),
        ("middle", min(max(1.0, short.duration * 0.50), short.duration - 0.8)),
        ("ending", max(0.8, short.duration - 0.8)),
    ):
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{second:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                str(frame_dir / f"{label}.jpg"),
            ]
        )
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video_path),
            "-vf",
            "fps=2,scale=216:-1,tile=5x3",
            "-frames:v",
            "1",
            str(REVIEW_DIR / f"{short.slug}_contact.jpg"),
        ]
    )


def write_metadata(paths: dict[str, Path]) -> None:
    rows = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": paths[short.slug].name,
                "source_start": short.start,
                "duration_seconds": short.duration,
                "source_rule": "single continuous A-to-B trim only; no mixed timestamps",
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )

    csv_path = META_DIR / "cs2_shorts_file_continuous_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# CS2 Continuous Trim Shorts",
        "",
        f"- Source: {DEFAULT_SOURCE}",
        "- Rule: every Short uses one continuous A-to-B source window only",
        "- Layout: blurred 1080x1920 background with centered gameplay",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['upload_order']}. {row['file']}",
                f"- Source start: {row['source_start']}",
                f"- Duration: {row['duration_seconds']}s",
                f"- Rule: {row['source_rule']}",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                f"- Thumbnail text: {row['thumbnail_text']}",
                "",
            ]
        )
    (META_DIR / "cs2_shorts_file_continuous_metadata.md").write_text("\n".join(lines), encoding="utf-8")


def verify_outputs(ffmpeg: str, paths: dict[str, Path]) -> None:
    for path in paths.values():
        run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build continuous A-to-B Shorts from Shorts.mp4.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    selected = [short for short in SHORTS if not args.only or short.slug in set(args.only)]
    if args.only and len(selected) != len(set(args.only)):
        known = ", ".join(short.slug for short in SHORTS)
        raise SystemExit(f"Unknown slug in --only. Known slugs: {known}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    paths: dict[str, Path] = {}
    for short in selected:
        print(f"Rendering continuous Short: {short.slug}")
        output = render_short(ffmpeg, source, short)
        paths[short.slug] = output
        make_review_assets(ffmpeg, output, short)

    verify_outputs(ffmpeg, paths)
    write_metadata(paths)
    print(f"Rendered {len(paths)} continuous Shorts to {SHORT_DIR}")
    print(f"Metadata written to {META_DIR}")
    print(f"Review assets written to {REVIEW_DIR}")


if __name__ == "__main__":
    main()
