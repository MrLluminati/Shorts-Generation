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
LONG_DIR = PIPELINE / "long_form" / PROJECT
SHORT_DIR = PIPELINE / "short_form" / PROJECT
THUMB_DIR = PIPELINE / "thumbnails" / PROJECT
ART_DIR = THUMB_DIR / "custom_art"
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT / "pro_longform"
REVIEW_DIR = PIPELINE / "review" / PROJECT / "pro_longform"

DEFAULT_SOURCE = Path(r"C:\Users\abhik\Videos\2026-06-09_14-17-59.mp4")
LONG_ART_BASE = ART_DIR / "007_first_light_longform_art_base.png"
SHORT_ART_BASE = ART_DIR / "007_first_light_shorts_art_base.png"

LONG_FILENAME = "007_first_light_hindi_part_01_first_mission_story_cut.mp4"
LONG_THUMBNAIL = "007_first_light_hindi_part_01_custom_thumbnail.jpg"

LONG_HASHTAGS = (
    "#007firstlight #jamesbond #bondgame #iointeractive #hindigaming "
    "#indiangaming #pcgaming #storygame #gamingvideo"
)
LONG_TAGS = (
    "007 first light, 007 first light gameplay, 007 first light hindi, james bond game, "
    "james bond gameplay, io interactive, bond game, first light game, hindi gameplay, "
    "indian gaming, pc gameplay india, story gameplay, cinematic gameplay, mrlluminati gaming"
)


@dataclass(frozen=True)
class LongClip:
    label: str
    start: str
    end: str
    card: bool = True

    @property
    def duration(self) -> float:
        return parse_timecode(self.end) - parse_timecode(self.start)


@dataclass(frozen=True)
class ShortThumb:
    slug: str
    text: tuple[str, str]


LONG_CLIPS = (
    LongClip("Crash Site Cold Open", "00:01:35.000", "00:03:35.000"),
    LongClip("Burning Shore", "00:04:08.000", "00:10:24.000"),
    LongClip("Survivor And Briefcase", "00:11:42.000", "00:18:32.000"),
    LongClip("Inside The Wreckage", "00:21:35.000", "00:24:42.000"),
    LongClip("The Base Reveal", "00:25:10.000", "00:30:42.000"),
    LongClip("Ambush And Flare", "00:31:45.000", "00:37:55.000"),
    LongClip("Title Sequence", "00:38:03.000", "00:41:18.000"),
)

SHORT_THUMBS = (
    ShortThumb("01_mission_starts_in_fire", ("MISSION", "FIRE")),
    ShortThumb("02_dark_opening_cinematic", ("DARK", "OPENING")),
    ShortThumb("03_warzone_shore", ("WARZONE", "SHORE")),
    ShortThumb("04_survivor_in_the_cave", ("SURVIVOR", "FOUND")),
    ShortThumb("05_mi6_briefcase_found", ("MI6", "BRIEFCASE")),
    ShortThumb("06_hidden_room_discovery", ("NOT", "EMPTY")),
    ShortThumb("07_bond_spots_the_base", ("THE", "BASE")),
    ShortThumb("08_crew_was_trapped", ("CREW", "TRAPPED")),
    ShortThumb("09_ambush_hit_fast", ("AMBUSH", "HIT")),
    ShortThumb("10_flare_title_sequence", ("TITLE", "FLARE")),
)


def ensure_dirs() -> None:
    for directory in (LONG_DIR, THUMB_DIR, ART_DIR, META_DIR, WORK_DIR, REVIEW_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def parse_timecode(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def fmt_time(seconds: float) -> str:
    total = int(round(seconds))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def total_long_duration() -> float:
    card_total = len(LONG_CLIPS) * 1.25
    return 2.4 + card_total + sum(clip.duration for clip in LONG_CLIPS) + 2.0


def chapters() -> list[str]:
    elapsed = 2.4
    result = ["00:00 Intro"]
    for clip in LONG_CLIPS:
        result.append(f"{fmt_time(elapsed)} {clip.label}")
        elapsed += 1.25 + clip.duration
    return result


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
    x: str | int,
    y: str | int,
    size: int,
    color: str,
    font: str = "impact.ttf",
    border: int = 4,
    enable: str | None = None,
) -> str:
    value = (
        f"drawtext=fontfile='{font_path(font)}':"
        f"text='{drawtext_escape(text)}':x={x}:y={y}:fontsize={size}:"
        f"fontcolor={color}:borderw={border}:bordercolor=black@0.92"
    )
    if enable:
        value += f":enable='{enable}'"
    return value


def make_card(ffmpeg: str, title: str, subtitle: str, out_path: Path, duration: float) -> None:
    filters = [
        "drawbox=x=0:y=0:w=1920:h=1080:color=0x030507@1:t=fill",
        "drawbox=x=0:y=0:w=1920:h=1080:color=0x0E2535@0.35:t=fill",
        "drawbox=x=0:y=0:w=1920:h=126:color=black@0.55:t=fill",
        "drawbox=x=132:y=244:w=14:h=334:color=0xF4C430@0.96:t=fill",
        "drawbox=x=132:y=608:w=680:h=7:color=0xC91414@0.96:t=fill",
        drawtext("MRLLUMINATI GAMING", 144, 48, 32, "white", "arialbd.ttf", 2),
        drawtext(title.upper(), 166, 294, 82, "white", "impact.ttf", 5),
        drawtext(subtitle.upper(), 170, 416, 38, "0xF4C430", "arialbd.ttf", 3),
        drawtext("007 FIRST LIGHT HINDI", 144, 930, 34, "white", "arialbd.ttf", 2),
        "format=yuv420p",
    ]
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c=0x030507:s=1920x1080:r=60:d={duration:.3f}",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=channel_layout=stereo:sample_rate=48000:d={duration:.3f}",
            "-vf",
            ",".join(filters),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "60",
            "-video_track_timescale",
            "60000",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_path),
        ]
    )


def render_long_clip(ffmpeg: str, source: Path, clip: LongClip, out_path: Path) -> None:
    duration = clip.duration
    fade = min(0.20, max(0.08, duration / 8))
    fade_out = max(0.0, duration - fade)
    label_enable = r"between(t\,0.35\,5.20)"
    filters = [
        "scale=1920:1080:flags=lanczos",
        "setsar=1",
        "fps=60",
        "eq=contrast=1.055:brightness=0.004:saturation=1.08",
        "unsharp=5:5:0.42",
        f"fade=t=in:st=0:d={fade:.3f}",
        f"fade=t=out:st={fade_out:.3f}:d={fade:.3f}",
        "drawbox=x=0:y=0:w=1920:h=74:color=black@0.18:t=fill",
        drawtext("MRLLUMINATI GAMING", "w-tw-42", 26, 24, "white", "arialbd.ttf", 1),
        "drawbox=x=54:y=826:w=560:h=98:color=black@0.58:t=fill:enable='between(t\\,0.35\\,5.20)'",
        "drawbox=x=54:y=826:w=10:h=98:color=0xF4C430@0.96:t=fill:enable='between(t\\,0.35\\,5.20)'",
        drawtext(clip.label.upper(), 82, 850, 39, "white", "arialbd.ttf", 2, label_enable),
        "format=yuv420p",
    ]
    audio_filter = (
        "aresample=48000,volume=1.04,alimiter=limit=0.97,"
        f"afade=t=in:st=0:d={fade:.3f},"
        f"afade=t=out:st={fade_out:.3f}:d={fade:.3f}"
    )
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            clip.start,
            "-t",
            f"{duration:.3f}",
            "-i",
            str(source),
            "-vf",
            ",".join(filters),
            "-af",
            audio_filter,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "60",
            "-video_track_timescale",
            "60000",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(out_path),
        ]
    )


def render_longform(ffmpeg: str, source: Path) -> Path:
    render_items: list[Path] = []
    intro = WORK_DIR / "00_intro.mp4"
    make_card(ffmpeg, "007 First Light", "First Mission Story Cut", intro, 2.4)
    render_items.append(intro)

    for index, clip in enumerate(LONG_CLIPS, start=1):
        card = WORK_DIR / f"{index:02d}_card.mp4"
        make_card(ffmpeg, clip.label, "Story-first Hindi gameplay", card, 1.25)
        render_items.append(card)

        clip_path = WORK_DIR / f"{index:02d}_{clip.label.lower().replace(' ', '_')}.mp4"
        render_long_clip(ffmpeg, source, clip, clip_path)
        render_items.append(clip_path)

    outro = WORK_DIR / "99_outro.mp4"
    make_card(ffmpeg, "More Story Cuts", "Subscribe for the next gameplay episode", outro, 2.0)
    render_items.append(outro)

    concat_path = WORK_DIR / "concat_longform.txt"
    concat_path.write_text(
        "\n".join(f"file '{item.as_posix()}'" for item in render_items) + "\n",
        encoding="utf-8",
    )

    out_path = LONG_DIR / LONG_FILENAME
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(out_path),
        ]
    )
    return out_path


def render_long_thumbnail(ffmpeg: str) -> Path:
    out_path = THUMB_DIR / LONG_THUMBNAIL
    if not LONG_ART_BASE.exists():
        raise FileNotFoundError(f"Missing custom art base: {LONG_ART_BASE}")
    filters = [
        "scale=1280:720:force_original_aspect_ratio=increase",
        "crop=1280:720",
        "setsar=1",
        "eq=contrast=1.12:brightness=0.012:saturation=1.14",
        "unsharp=5:5:0.55",
        "drawbox=x=674:y=0:w=606:h=720:color=black@0.42:t=fill",
        "drawbox=x=0:y=0:w=1280:h=720:color=black@0.05:t=fill",
        "drawbox=x=710:y=72:w=278:h=55:color=0xF4C430@0.96:t=fill",
        drawtext("HINDI GAMEPLAY", 730, 85, 28, "black", "arialbd.ttf", 1),
        drawtext("007 FIRST", 706, 178, 72, "white", "impact.ttf", 5),
        drawtext("LIGHT", 706, 266, 104, "0xF4C430", "impact.ttf", 6),
        drawtext("FIRST MISSION", 708, 406, 54, "white", "impact.ttf", 5),
        drawtext("STORY CUT", 710, 476, 62, "0xD71920", "impact.ttf", 5),
        "drawbox=x=710:y=574:w=420:h=54:color=black@0.78:t=fill",
        drawtext("PART 1", 732, 584, 34, "white", "arialbd.ttf", 2),
        "format=yuvj420p",
    ]
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(LONG_ART_BASE),
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


def render_short_custom_thumbnails(ffmpeg: str) -> list[Path]:
    if not SHORT_ART_BASE.exists():
        raise FileNotFoundError(f"Missing custom art base: {SHORT_ART_BASE}")
    outputs = []
    for item in SHORT_THUMBS:
        line1, line2 = item.text
        out_path = THUMB_DIR / f"{item.slug}_thumbnail.jpg"
        filters = [
            "scale=1080:1920:force_original_aspect_ratio=increase",
            "crop=1080:1920",
            "setsar=1",
            "eq=contrast=1.10:brightness=0.018:saturation=1.12",
            "unsharp=5:5:0.58",
            "drawbox=x=0:y=1240:w=1080:h=512:color=black@0.58:t=fill",
            "drawbox=x=58:y=100:w=318:h=58:color=0xF4C430@0.98:t=fill",
            drawtext("007 FIRST LIGHT", 76, 113, 29, "black", "arialbd.ttf", 1),
            "drawbox=x=58:y=170:w=438:h=8:color=white@0.96:t=fill",
            drawtext(line1, 58, 1286, 100, "white", "impact.ttf", 6),
            drawtext(line2, 58, 1410, 118, "0xF4C430", "impact.ttf", 6),
            "drawbox=x=62:y=1632:w=386:h=60:color=0x111111@0.86:t=fill",
            drawtext("HINDI GAMEPLAY", 82, 1645, 31, "white", "arialbd.ttf", 2),
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
                "-i",
                str(SHORT_ART_BASE),
                "-frames:v",
                "1",
                "-vf",
                ",".join(filters),
                "-q:v",
                "2",
                str(out_path),
            ]
        )
        outputs.append(out_path)
    return outputs


def review_frames(ffmpeg: str, video_path: Path, duration: float) -> None:
    points = [
        ("hook", 2.8),
        ("early", min(duration * 0.18, duration - 1.0)),
        ("middle", min(duration * 0.52, duration - 1.0)),
        ("finale", min(duration * 0.82, duration - 1.0)),
        ("ending", max(0.0, duration - 2.0)),
    ]
    for label, seconds in points:
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
                str(video_path),
                "-frames:v",
                "1",
                "-vf",
                "scale=480:270",
                "-q:v",
                "3",
                str(REVIEW_DIR / f"longform_{label}.jpg"),
            ]
        )


def review_contact_sheet(ffmpeg: str, video_path: Path, duration: float) -> None:
    frames_dir = REVIEW_DIR / "longform_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    timestamps = [0.0]
    step = 150
    current = float(step)
    while current < duration - 4:
        timestamps.append(current)
        current += step
    timestamps.append(max(0.0, duration - 3.0))

    for index, seconds in enumerate(timestamps):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        label = fmt_time(seconds).replace(":", r"\:")
        vf = (
            "scale=320:180,"
            "drawbox=x=0:y=0:w=320:h=24:color=black@0.74:t=fill,"
            f"drawtext=text='{label}':x=8:y=4:fontsize=18:fontcolor=white"
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
                str(video_path),
                "-frames:v",
                "1",
                "-vf",
                vf,
                "-q:v",
                "3",
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
            "tile=4x4",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(REVIEW_DIR / "longform_contact_sheet.jpg"),
        ]
    )


def thumbnail_contact_sheet(ffmpeg: str) -> None:
    frames_dir = REVIEW_DIR / "custom_thumb_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    items = [THUMB_DIR / LONG_THUMBNAIL] + [THUMB_DIR / f"{item.slug}_thumbnail.jpg" for item in SHORT_THUMBS]
    for index, item in enumerate(items):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(item),
                "-frames:v",
                "1",
                "-vf",
                "scale=320:568:force_original_aspect_ratio=decrease,pad=320:568:(ow-iw)/2:(oh-ih)/2:black",
                "-q:v",
                "3",
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
            "tile=6x2",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(REVIEW_DIR / "custom_thumbnails_contact.jpg"),
        ]
    )


def write_metadata(long_path: Path, long_thumb: Path) -> None:
    title = "007 First Light Hindi Gameplay - First Mission Story Cut"
    description = (
        "A tighter story-first cut from my 007 First Light Hindi gameplay recording. "
        "This edit keeps the crash site, survivor moment, MI6 briefcase, base reveal, ambush, "
        "and title sequence in a clean episode format without menu dead time.\n\n"
        "Chapters:\n"
        + "\n".join(chapters())
    )
    rows = [
        {
            "output_type": "long",
            "upload_order": 1,
            "file": long_path.name,
            "title": title,
            "description": description,
            "hashtags": LONG_HASHTAGS,
            "tags": LONG_TAGS,
            "pinned_comment": "Should I turn the next recording into a full story episode like this?",
            "thumbnail": long_thumb.name,
            "chapters": " | ".join(chapters()),
        }
    ]
    for index, thumb in enumerate(SHORT_THUMBS, start=2):
        rows.append(
            {
                "output_type": "short_thumbnail",
                "upload_order": index,
                "file": f"{thumb.slug}.mp4",
                "title": "",
                "description": "",
                "hashtags": "",
                "tags": "",
                "pinned_comment": "",
                "thumbnail": f"{thumb.slug}_thumbnail.jpg",
                "chapters": "",
            }
        )

    csv_path = META_DIR / "007_first_light_2026_06_09_pro_pack_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# 007 First Light Pro Pack",
        "",
        f"## Long Form",
        f"- File: {long_path.name}",
        f"- Title: {title}",
        f"- Thumbnail: {long_thumb.name}",
        f"- Hashtags: {LONG_HASHTAGS}",
        f"- Tags: {LONG_TAGS}",
        f"- Pinned comment: {rows[0]['pinned_comment']}",
        "",
        "## Description",
        description,
        "",
        "## Custom Short Thumbnails",
    ]
    for thumb in SHORT_THUMBS:
        md_lines.append(f"- {thumb.slug}_thumbnail.jpg")
    (META_DIR / "007_first_light_2026_06_09_pro_pack_metadata.md").write_text(
        "\n".join(md_lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the professional 007 First Light long-form pack.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local gameplay MP4 source")
    parser.add_argument("--skip-long", action="store_true", help="Only render custom thumbnails and metadata")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Only render long-form video")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise FileNotFoundError(source)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    long_path = LONG_DIR / LONG_FILENAME
    if not args.skip_long:
        print("Rendering 007 First Light long-form story cut")
        long_path = render_longform(ffmpeg, source)
        duration = total_long_duration()
        review_frames(ffmpeg, long_path, duration)
        review_contact_sheet(ffmpeg, long_path, duration)

    long_thumb = THUMB_DIR / LONG_THUMBNAIL
    if not args.skip_thumbnails:
        print("Rendering custom generated-art thumbnails")
        long_thumb = render_long_thumbnail(ffmpeg)
        render_short_custom_thumbnails(ffmpeg)
        thumbnail_contact_sheet(ffmpeg)

    write_metadata(long_path, long_thumb)
    print(f"Long form: {LONG_DIR}")
    print(f"Thumbnails: {THUMB_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
