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


PROJECT = "007_first_light_2026_06_09"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
THUMB_DIR = PIPELINE / "thumbnails" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE = Path(r"C:\Users\abhik\Videos\2026-06-09_14-17-59.mp4")

BASE_HASHTAGS = (
    "#007firstlight #jamesbond #bondgame #iointeractive #firstlight "
    "#storygame #gamingclips #hindigaming #indiangaming #pcgaming #shorts"
)
BASE_TAGS = (
    "007 first light, first light game, james bond game, bond game, io interactive, "
    "007 first light gameplay, 007 first light hindi, james bond gameplay, story game, "
    "cinematic gameplay, pc gameplay india, hindi gaming, indian gaming, gaming shorts"
)
DESCRIPTION_SUFFIX = (
    "More 007 First Light Hindi gameplay highlights, story moments, and cinematic Shorts "
    "on MrLluminati Gaming."
)


@dataclass(frozen=True)
class FirstLightShort:
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
    thumbnail_timestamp: float


SHORTS = [
    FirstLightShort(
        slug="01_mission_starts_in_fire",
        start="00:01:35.000",
        duration=52.0,
        hook="THE MISSION\nSTARTS IN FIRE",
        title="The Mission Starts In Fire | 007 First Light Hindi #shorts",
        description="The opening mission throws young Bond straight into a burning disaster.",
        tags=f"{BASE_TAGS}, 007 first light opening, bond opening scene, first light fire scene",
        pinned_comment="Strong opening or too cinematic for a gameplay Short?",
        thumbnail_text="MISSION FIRE",
        upload_order=2,
        thumbnail_timestamp=25.0,
    ),
    FirstLightShort(
        slug="02_dark_opening_cinematic",
        start="00:02:36.000",
        duration=48.0,
        hook="THE OPENING\nGETS DARK",
        title="The Opening Gets Dark | 007 First Light #shorts",
        description="The cinematic opening slows down into a darker, more mysterious moment.",
        tags=f"{BASE_TAGS}, 007 first light cinematic, james bond cinematic, first light opening",
        pinned_comment="This opening felt more thriller than action. Good choice?",
        thumbnail_text="DARK OPENING",
        upload_order=8,
        thumbnail_timestamp=23.0,
    ),
    FirstLightShort(
        slug="03_warzone_shore",
        start="00:04:08.000",
        duration=58.0,
        hook="BOND WAKES UP\nIN A WARZONE",
        title="Bond Wakes Up In A Warzone | 007 First Light Hindi #shorts",
        description="The first playable stretch opens on a burning shore after the crash.",
        tags=f"{BASE_TAGS}, 007 first light crash, bond warzone, first light gameplay, burning shore",
        pinned_comment="Would you explore first or run straight toward the objective?",
        thumbnail_text="WARZONE SHORE",
        upload_order=1,
        thumbnail_timestamp=18.0,
    ),
    FirstLightShort(
        slug="04_survivor_in_the_cave",
        start="00:08:02.000",
        duration=54.0,
        hook="HE FINDS\nA SURVIVOR",
        title="He Finds A Survivor | 007 First Light #shorts",
        description="Bond searches the wreckage and finds someone still alive in the cave.",
        tags=f"{BASE_TAGS}, 007 first light survivor, first light cave, james bond rescue scene",
        pinned_comment="Was this the first real story hook of the mission?",
        thumbnail_text="SURVIVOR FOUND",
        upload_order=4,
        thumbnail_timestamp=10.0,
    ),
    FirstLightShort(
        slug="05_mi6_briefcase_found",
        start="00:15:18.000",
        duration=58.0,
        hook="THE MI6 BRIEFCASE\nWAS FOUND",
        title="The MI6 Briefcase Was Found | 007 First Light Hindi #shorts",
        description="A key MI6 briefcase turns the wreckage search into a mission clue.",
        tags=f"{BASE_TAGS}, mi6 briefcase, 007 first light mi6, james bond mission clue",
        pinned_comment="Would you check the briefcase first or help the survivor?",
        thumbnail_text="MI6 BRIEFCASE",
        upload_order=5,
        thumbnail_timestamp=57.0,
    ),
    FirstLightShort(
        slug="06_hidden_room_discovery",
        start="00:23:28.000",
        duration=58.0,
        hook="THE ROOM\nWAS NOT EMPTY",
        title="The Room Was Not Empty | 007 First Light #shorts",
        description="A quiet room search turns tense when the scene reveals more than expected.",
        tags=f"{BASE_TAGS}, 007 first light hidden room, bond stealth, first light room discovery",
        pinned_comment="Did this feel like stealth, horror, or both?",
        thumbnail_text="NOT EMPTY",
        upload_order=6,
        thumbnail_timestamp=26.0,
    ),
    FirstLightShort(
        slug="07_bond_spots_the_base",
        start="00:26:10.000",
        duration=58.0,
        hook="BOND SPOTS\nTHE BASE",
        title="Bond Spots The Base | 007 First Light Hindi #shorts",
        description="The cave path opens into a larger enemy base and the mission scale changes.",
        tags=f"{BASE_TAGS}, 007 first light base, bond infiltration, first light stealth gameplay",
        pinned_comment="This is where the mission starts feeling bigger.",
        thumbnail_text="THE BASE",
        upload_order=3,
        thumbnail_timestamp=33.0,
    ),
    FirstLightShort(
        slug="08_crew_was_trapped",
        start="00:29:42.000",
        duration=55.0,
        hook="THE CREW\nWAS TRAPPED",
        title="The Crew Was Trapped | 007 First Light #shorts",
        description="Bond reaches the crew area and the mission shifts into a rescue problem.",
        tags=f"{BASE_TAGS}, 007 first light crew, bond rescue, first light story gameplay",
        pinned_comment="Would you call this a rescue mission or a setup?",
        thumbnail_text="CREW TRAPPED",
        upload_order=7,
        thumbnail_timestamp=16.0,
    ),
    FirstLightShort(
        slug="09_ambush_hit_fast",
        start="00:34:28.000",
        duration=58.0,
        hook="THE AMBUSH\nHIT FAST",
        title="The Ambush Hit Fast | 007 First Light Hindi #shorts",
        description="A calm story moment breaks into an ambush with sparks, smoke, and panic.",
        tags=f"{BASE_TAGS}, 007 first light ambush, bond action scene, first light action gameplay",
        pinned_comment="Best action moment of the recording?",
        thumbnail_text="AMBUSH HIT",
        upload_order=9,
        thumbnail_timestamp=24.0,
    ),
    FirstLightShort(
        slug="10_flare_title_sequence",
        start="00:36:28.000",
        duration=58.0,
        hook="THE FLARE\nBECAME THE TITLE",
        title="The Flare Became The Title | 007 First Light #shorts",
        description="The finale moves from the flare moment into the 007 First Light title beat.",
        tags=f"{BASE_TAGS}, 007 first light title, bond title sequence, first light finale",
        pinned_comment="That title transition was clean. Did it land?",
        thumbnail_text="TITLE FLARE",
        upload_order=10,
        thumbnail_timestamp=48.0,
    ),
]


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, THUMB_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_short_ass(short: FirstLightShort) -> Path:
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
        "Style: Logo,Arial,27,&H00FFFFFF,&H000000FF,&HAA000000,&HAA000000,-1,0,0,0,100,100,2,0,1,2,0,8,40,40,34,1",
        "Style: Hook,Arial Black,64,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,54,54,180,1",
        "Style: Lower,Arial Black,35,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,1,2,70,70,196,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 8,{ass_time(0)},{ass_time(short.duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.20)},{ass_time(3.8)},Hook,,0,0,0,,"
            r"{\fad(80,220)\t(0,320,\fscx108\fscy108)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 7,{ass_time(max(0, short.duration - 5.4))},{ass_time(max(0, short.duration - 0.7))},Lower,,0,0,0,,"
            r"{\fad(120,220)}007 FIRST LIGHT HINDI"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, source: Path, short: FirstLightShort) -> Path:
    ass_path = write_short_ass(short)
    out_path = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.45)
    video_filter = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.045:saturation=0.90[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "setsar=1,"
        "drawbox=x=0:y=650:w=1080:h=3:color=white@0.12:t=fill,"
        "drawbox=x=0:y=1267:w=1080:h=3:color=white@0.12:t=fill,"
        "eq=contrast=1.05:saturation=1.06,"
        "vignette=PI/5,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.16,"
        f"fade=t=out:st={fade_out:.3f}:d=0.45,"
        "format=yuv420p[v]"
    )
    audio_filter = (
        "[0:a]aresample=48000,highpass=f=70,volume=1.05,alimiter=limit=0.96,"
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
            "18",
            "-r",
            "60",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
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
                str(frames_dir / f"frame_{index:03d}.jpg"),
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


def render_thumbnail(ffmpeg: str, video_path: Path, short: FirstLightShort) -> Path:
    out_path = THUMB_DIR / f"{short.slug}_thumbnail.jpg"
    line1, line2 = thumbnail_lines(short.thumbnail_text)
    filters = [
        "scale=1080:1920:force_original_aspect_ratio=increase",
        "crop=1080:1920",
        "setsar=1",
        "eq=gamma=1.18:contrast=1.12:brightness=0.055:saturation=1.26",
        "unsharp=5:5:0.68",
        "drawbox=x=0:y=0:w=1080:h=360:color=0xF4C430@0.055:t=fill",
        "drawbox=x=0:y=0:w=1080:h=1920:color=black@0.04:t=fill",
        "drawbox=x=0:y=1156:w=1080:h=512:color=black@0.64:t=fill",
        "drawbox=x=58:y=100:w=316:h=58:color=0xF4C430@0.98:t=fill",
        drawtext("007 FIRST LIGHT", 76, 113, 29, "black", "arialbd.ttf", 1),
        "drawbox=x=58:y=170:w=438:h=8:color=white@0.96:t=fill",
        drawtext(line1, 58, 1232, 90, "white", "impact.ttf", 6),
        drawtext(line2, 58, 1352, 108, "0xF4C430", "impact.ttf", 6),
        "drawbox=x=62:y=1568:w=386:h=60:color=0x111111@0.88:t=fill",
        drawtext("HINDI GAMEPLAY", 82, 1581, 31, "white", "arialbd.ttf", 2),
        "vignette=PI/5",
        "format=yuvj420p",
    ]
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{short.thumbnail_timestamp:.3f}",
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


def render_thumbnails(ffmpeg: str, short_paths: dict[str, Path]) -> None:
    for short in SHORTS:
        video_path = short_paths.get(short.slug, SHORT_DIR / f"{short.slug}.mp4")
        if video_path.exists():
            render_thumbnail(ffmpeg, video_path, short)


def write_metadata(short_paths: dict[str, Path]) -> None:
    rows = []
    for short in SHORTS:
        thumbnail_path = THUMB_DIR / f"{short.slug}_thumbnail.jpg"
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": short_paths[short.slug].name,
                "thumbnail": thumbnail_path.name if thumbnail_path.exists() else "",
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

    csv_path = META_DIR / "007_first_light_2026_06_09_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# 007 First Light Shorts Pack", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
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
    (META_DIR / "007_first_light_2026_06_09_metadata.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 007 First Light Shorts from the June 9 recording.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local gameplay recording")
    parser.add_argument("--only", nargs="*", help="Optional slug list to rerender")
    parser.add_argument("--thumbnails-only", action="store_true", help="Only render thumbnails and metadata")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Do not render thumbnail JPGs")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Missing source file: {source}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
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
            print(f"Rendering 007 First Light short: {short.slug}")
            out_path = render_short(ffmpeg, source, short)
            short_paths[short.slug] = out_path
            review_frames(ffmpeg, out_path, short.slug, short.duration)
            review_contact_sheet(ffmpeg, out_path, short.slug, short.duration)

    missing = [short.slug for short in SHORTS if short.slug not in short_paths]
    if missing:
        raise SystemExit(f"Missing rendered shorts: {', '.join(missing)}")

    if not args.skip_thumbnails:
        print("Rendering 007 First Light thumbnails")
        render_thumbnails(ffmpeg, short_paths)

    write_metadata(short_paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Thumbnails: {THUMB_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
