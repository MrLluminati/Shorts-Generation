from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


PROJECT = "rdr2_hindi_story_free_roam"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
LONG_DIR = PIPELINE / "long_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
THUMB_DIR = PIPELINE / "thumbnails" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"
LONG_WORK_DIR = WORK_DIR / "long_form_parts"

BASE_HASHTAGS = (
    "#rdr2 #reddeadredemption2 #rdr2hindi #hindigaming #indiangaming "
    "#pcgaming #storymode #gaminghighlights #gamingclips #shorts"
)
BASE_TAGS = (
    "red dead redemption 2, rdr2, rdr2 hindi, red dead redemption 2 hindi, "
    "indian pc gameplay, hindi gaming, mrlluminati gaming, rdr2 story mode, "
    "rdr2 live highlights, gaming shorts, pc gaming india"
)


@dataclass(frozen=True)
class ShortSpec:
    slug: str
    start: str
    duration: float
    hook: str
    beats: tuple[str, ...]
    title: str
    description: str
    tags: str
    pinned_comment: str
    upload_order: int


@dataclass(frozen=True)
class LongClip:
    label: str
    start: str
    end: str
    clip_type: str
    card: bool = False

    @property
    def duration(self) -> float:
        return parse_timecode(self.end) - parse_timecode(self.start)


@dataclass(frozen=True)
class LongPart:
    slug: str
    filename: str
    title: str
    description: str
    tags: str
    pinned_comment: str
    thumbnail_text: tuple[str, str]
    thumbnail_timestamp: str
    upload_order: int
    clips: tuple[LongClip, ...]


SHORTS = [
    ShortSpec(
        slug="01_first_snow_shootout",
        start="00:53:30.000",
        duration=58.0,
        hook="SNOW CAMP\nSHOOTOUT",
        beats=(),
        title="Snow Camp Shootout | RDR2 Hindi #shorts",
        description=(
            "A snowy camp shootout from my Red Dead Redemption 2 Hindi live stream."
        ),
        tags=f"{BASE_TAGS}, rdr2 shootout, rdr2 snow mission, rdr2 odriscoll camp",
        pinned_comment="Should I play this mission stealthy next time or full chaos?",
        upload_order=1,
    ),
    ShortSpec(
        slug="02_looted_everyone_after_fight",
        start="00:57:00.000",
        duration=55.0,
        hook="AFTER THE FIGHT...\nLOOT TIME",
        beats=(),
        title="I Looted Everyone After The Fight | RDR2 Hindi #shorts",
        description=(
            "After the first shootout, the real Red Dead Redemption 2 habit kicked in."
        ),
        tags=f"{BASE_TAGS}, rdr2 loot, rdr2 looting, rdr2 shootout, rdr2 funny gaming moment",
        pinned_comment="Be honest: do you loot everyone too?",
        upload_order=2,
    ),
    ShortSpec(
        slug="03_train_robbery_started_bad",
        start="01:40:05.000",
        duration=58.0,
        hook="TRAIN ROBBERY\nFIGHT",
        beats=(),
        title="Train Robbery Fight | RDR2 Hindi #shorts",
        description=(
            "A train robbery fight from my Red Dead Redemption 2 Hindi live stream."
        ),
        tags=f"{BASE_TAGS}, rdr2 train robbery, rdr2 train mission, rdr2 gunfight, rdr2 hindi live",
        pinned_comment="Best RDR2 mission type: train robbery or camp shootout?",
        upload_order=3,
    ),
]

LONG_HASHTAGS = "#rdr2 #reddeadredemption2 #rdr2hindi #hindigaming #indiangaming #pcgaming #storymode"
LONG_CARD_DURATION = 1.45
LEGACY_LONG_FILES = ("rdr2_hindi_story_free_roam_highlights.mp4",)
LEGACY_REVIEW_PREFIXES = ("long_form_highlights",)

LONG_PARTS = [
    LongPart(
        slug="rdr2_hindi_story_part_01_adler_ranch_rescue",
        filename="rdr2_hindi_story_part_01_adler_ranch_rescue.mp4",
        title="RDR2 Hindi: Adler Ranch Rescue Sets The Story Up | Part 1",
        description=(
            "The RDR2 Hindi story starts in the snow: Colter, the first ride, "
            "the Adler ranch search, and the rescue that sets the gang's Chapter 1 story in motion. "
            "This version keeps the full dialogue flow intact instead of cutting through story scenes."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 chapter 1, "
            "rdr2 snow mission, rdr2 adler ranch, rdr2 sadie adler, rdr2 cutscenes"
        ),
        pinned_comment="Did the Adler ranch scene set the tone for the whole story?",
        thumbnail_text=("ADLER RANCH", "RESCUE"),
        thumbnail_timestamp="00:18:00.000",
        upload_order=4,
        clips=(
            LongClip("COLTER AND ADLER RANCH", "00:05:55.000", "00:28:45.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="rdr2_hindi_story_part_02_john_rescue_snow",
        filename="rdr2_hindi_story_part_02_john_rescue_snow.mp4",
        title="RDR2 Hindi: John Rescue In The Snow | Part 2",
        description=(
            "The gang heads into the storm to find John. This story-first Hindi cut keeps the snowy ride, "
            "rescue dialogue, return to camp, and mission tension together so the scene plays properly."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 john rescue, "
            "rdr2 snow rescue, rdr2 chapter 1, rdr2 cutscenes, rdr2 mission dialogue"
        ),
        pinned_comment="Was this rescue one of the strongest Chapter 1 moments?",
        thumbnail_text=("JOHN RESCUE", "IN SNOW"),
        thumbnail_timestamp="00:10:00.000",
        upload_order=5,
        clips=(
            LongClip("JOHN RESCUE IN THE SNOW", "00:28:35.000", "00:51:15.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="rdr2_hindi_story_part_03_odriscoll_camp_hunt_setup",
        filename="rdr2_hindi_story_part_03_odriscoll_camp_hunt_setup.mp4",
        title="RDR2 Hindi: O'Driscoll Camp Fight To Hunt Setup | Part 3",
        description=(
            "The O'Driscoll camp mission plays with its setup and mission dialogue intact, then skips only "
            "the dead-time body looting before the cabin search and Charles hunting setup."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 odriscoll camp, "
            "rdr2 camp fight, rdr2 cabin search, rdr2 charles hunting, rdr2 mission dialogue"
        ),
        pinned_comment="Should O'Driscoll fights stay full story style or be shortened more?",
        thumbnail_text=("ODRISCOLL", "CAMP FIGHT"),
        thumbnail_timestamp="00:03:30.000",
        upload_order=6,
        clips=(
            LongClip("O'DRISCOLL CAMP MISSION", "00:51:15.000", "00:57:10.000", "dialogue", True),
            LongClip("CABIN SEARCH AND HUNT SETUP", "00:59:20.000", "01:10:50.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="rdr2_hindi_story_part_04_charles_deer_hunt",
        filename="rdr2_hindi_story_part_04_charles_deer_hunt.mp4",
        title="RDR2 Hindi: Charles Deer Hunt Full Story | Part 4",
        description=(
            "Charles teaches Arthur the survival rhythm of RDR2: tracking, deer hunting, and the long ride back. "
            "This cut keeps the conversation flow because this mission is all about character and atmosphere."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 deer hunt, "
            "rdr2 charles hunting, rdr2 survival mission, rdr2 chapter 1, rdr2 dialogue"
        ),
        pinned_comment="Do you prefer these quiet hunting missions or the big action missions?",
        thumbnail_text=("CHARLES", "DEER HUNT"),
        thumbnail_timestamp="00:07:30.000",
        upload_order=7,
        clips=(
            LongClip("CHARLES DEER HUNT", "01:10:00.000", "01:31:45.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="rdr2_hindi_story_part_05_train_robbery",
        filename="rdr2_hindi_story_part_05_train_robbery.mp4",
        title="RDR2 Hindi: Train Robbery Full Mission | Part 5",
        description=(
            "The train robbery gets its full story build-up, fight, search, and payoff. "
            "No chopped dialogue here, just the complete mission flow from the Hindi live stream."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 train robbery, "
            "rdr2 train fight, rdr2 train search, rdr2 chapter 1, rdr2 mission"
        ),
        pinned_comment="Was this train robbery worth the trouble?",
        thumbnail_text=("TRAIN ROBBERY", "FULL MISSION"),
        thumbnail_timestamp="00:05:00.000",
        upload_order=8,
        clips=(
            LongClip("TRAIN ROBBERY", "01:31:45.000", "01:47:58.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="rdr2_hindi_story_part_06_horseshoe_overlook",
        filename="rdr2_hindi_story_part_06_horseshoe_overlook.mp4",
        title="RDR2 Hindi: Finally Reaching Horseshoe Overlook | Part 6",
        description=(
            "After the snow and the train job, the gang finally moves toward Horseshoe Overlook. "
            "This closing story cut keeps the wagon dialogue and camp arrival scene together."
        ),
        tags=(
            f"{BASE_TAGS}, rdr2 hindi gameplay, rdr2 story mode hindi, rdr2 horseshoe overlook, "
            "rdr2 new camp, rdr2 wagon dialogue, rdr2 chapter 2, rdr2 cutscene"
        ),
        pinned_comment="Does Horseshoe Overlook feel like the real beginning of RDR2?",
        thumbnail_text=("NEW CAMP", "ARRIVAL"),
        thumbnail_timestamp="00:09:30.000",
        upload_order=9,
        clips=(
            LongClip("HORSESHOE OVERLOOK ARRIVAL", "01:47:58.000", "02:02:50.000", "dialogue", True),
        ),
    ),
]


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, LONG_DIR, META_DIR, THUMB_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR, LONG_WORK_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def parse_timecode(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def fmt_chapter_time(seconds: float) -> str:
    total = int(round(seconds))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def long_part_duration(part: LongPart) -> float:
    card_time = sum(LONG_CARD_DURATION for clip in part.clips if clip.card)
    return card_time + sum(clip.duration for clip in part.clips)


def long_part_chapters(part: LongPart) -> list[str]:
    chapters: list[str] = []
    elapsed = 0.0
    last_label = ""
    for clip in part.clips:
        if clip.card and clip.label != last_label:
            chapters.append(f"{fmt_chapter_time(elapsed)} {clip.label.title()}")
            last_label = clip.label
        if clip.card:
            elapsed += LONG_CARD_DURATION
        elapsed += clip.duration
    return chapters


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


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
        "Style: Hook,Arial Black,70,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,54,54,180,1",
        "Style: Beat,Arial Black,45,&H00FFFFFF,&H000000FF,&H00111111,&H88000000,-1,0,0,0,100,100,0,0,1,4,1,5,76,76,0,1",
        "Style: Lower,Arial Black,37,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,1,2,70,70,196,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 8,{ass_time(0)},{ass_time(short.duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.25)},{ass_time(3.9)},Hook,,0,0,0,,"
            r"{\fad(80,220)\t(0,320,\fscx108\fscy108)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 7,{ass_time(short.duration - 6.2)},{ass_time(short.duration - 0.7)},Lower,,0,0,0,,"
            r"{\fad(120,220)}RDR2 HINDI LIVE HIGHLIGHT"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def render_short(ffmpeg: str, source: Path, short: ShortSpec) -> Path:
    ass_path = write_short_ass(short)
    out_path = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.45)
    video_filter = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.06:saturation=0.85[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "setsar=1,"
        "drawbox=x=0:y=650:w=1080:h=3:color=white@0.12:t=fill,"
        "drawbox=x=0:y=1267:w=1080:h=3:color=white@0.12:t=fill,"
        "vignette=PI/5,noise=alls=3:allf=t+u,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.18,"
        f"fade=t=out:st={fade_out:.3f}:d=0.45,"
        "format=yuv420p[v]"
    )
    audio_filter = (
        "[0:a]aresample=48000,highpass=f=70,volume=1.10,alimiter=limit=0.95,"
        f"afade=t=in:st=0:d=0.15,afade=t=out:st={fade_out:.3f}:d=0.45[a]"
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


def make_title_card(ffmpeg: str, label: str, out_path: Path, duration: float = 1.6) -> None:
    text = label.replace(":", " - ").replace("'", "")
    draw = (
        "drawbox=x=0:y=0:w=1280:h=720:color=0x070909@1:t=fill,"
        "drawgrid=w=80:h=80:t=1:c=0xffffff@0.035,"
        "drawtext=text='MRLLUMINATI GAMING':x=(w-text_w)/2:y=245:fontsize=28:fontcolor=white,"
        f"drawtext=text='{text}':x=(w-text_w)/2:y=320:fontsize=58:fontcolor=white,"
        "drawtext=text='RDR2 HINDI HIGHLIGHTS':x=(w-text_w)/2:y=405:fontsize=30:fontcolor=0xdddddd"
    )
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
            f"color=c=0x070909:s=1280x720:r=30:d={duration:.2f}",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=channel_layout=stereo:sample_rate=48000:d={duration:.2f}",
            "-vf",
            f"{draw},fps=30,setsar=1,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
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
    fade = 0.14 if clip.clip_type == "combat_montage" else 0.18
    fade = min(fade, max(0.04, duration / 4))
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
            "scale=1280:720:flags=lanczos,setsar=1,fps=30,"
            f"fade=t=in:st=0:d={fade:.3f},"
            f"fade=t=out:st={max(0, duration - fade):.3f}:d={fade:.3f},"
            "format=yuv420p",
            "-af",
            "aresample=48000,volume=1.04,alimiter=limit=0.97,"
            f"afade=t=in:st=0:d={fade:.3f},"
            f"afade=t=out:st={max(0, duration - fade):.3f}:d={fade:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "17",
            "-r",
            "30",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(out_path),
        ]
    )


def render_long_part(ffmpeg: str, source: Path, part: LongPart) -> Path:
    part_work_dir = LONG_WORK_DIR / part.slug
    part_work_dir.mkdir(parents=True, exist_ok=True)
    render_items: list[Path] = []
    for index, clip in enumerate(part.clips, start=1):
        if clip.card:
            card_path = part_work_dir / f"{index:02d}_card.mp4"
            make_title_card(ffmpeg, clip.label, card_path, LONG_CARD_DURATION)
            render_items.append(card_path)
        clip_path = part_work_dir / f"{index:02d}_{clip.clip_type}.mp4"
        render_long_clip(ffmpeg, source, clip, clip_path)
        render_items.append(clip_path)

    concat_path = part_work_dir / "concat.txt"
    concat_path.write_text(
        "\n".join(f"file '{item.as_posix()}'" for item in render_items) + "\n",
        encoding="utf-8",
    )
    out_path = LONG_DIR / part.filename
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


def clean_legacy_long_outputs() -> None:
    desired_files = {part.filename for part in LONG_PARTS}
    desired_thumbnails = {f"{part.slug}_thumbnail.jpg" for part in LONG_PARTS}
    for filename in LEGACY_LONG_FILES:
        path = LONG_DIR / filename
        if path.exists():
            path.unlink()
    for path in LONG_DIR.glob("rdr2_hindi_story_part_*.mp4"):
        if path.name not in desired_files:
            path.unlink()
    for path in THUMB_DIR.glob("rdr2_hindi_story_part_*_thumbnail.jpg"):
        if path.name not in desired_thumbnails:
            path.unlink()
    for prefix in LEGACY_REVIEW_PREFIXES:
        for path in REVIEW_DIR.glob(f"{prefix}_*.jpg"):
            path.unlink()
    desired_slugs = {part.slug for part in LONG_PARTS}
    for path in REVIEW_DIR.glob("rdr2_hindi_story_part_*"):
        matching_slug = next((slug for slug in desired_slugs if path.name.startswith(slug)), None)
        if matching_slug is None:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


def render_long_form(ffmpeg: str, source: Path) -> list[Path]:
    clean_legacy_long_outputs()
    return [render_long_part(ffmpeg, source, part) for part in LONG_PARTS]


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
    border: int = 4,
) -> str:
    return (
        f"drawtext=fontfile='{font_path(font)}':"
        f"text='{drawtext_escape(text)}':"
        f"x={x}:y={y}:fontsize={size}:fontcolor={color}:"
        f"borderw={border}:bordercolor=black@0.92"
    )


def render_thumbnail(ffmpeg: str, video_path: Path, part: LongPart) -> Path:
    out_path = THUMB_DIR / f"{part.slug}_thumbnail.jpg"
    line1, line2 = part.thumbnail_text
    part_number = str(part.upload_order - 3)
    filters = [
        "scale=1280:720:force_original_aspect_ratio=increase",
        "crop=1280:720",
        "setsar=1",
        "eq=contrast=1.12:brightness=-0.025:saturation=1.22",
        "unsharp=5:5:0.72",
        "drawbox=x=0:y=0:w=1280:h=720:color=black@0.12:t=fill",
        "drawbox=x=0:y=0:w=572:h=720:color=black@0.64:t=fill",
        "drawbox=x=0:y=0:w=1280:h=86:color=black@0.28:t=fill",
        "drawbox=x=42:y=38:w=238:h=56:color=0xC91414@0.98:t=fill",
        "drawbox=x=42:y=111:w=468:h=8:color=0xF4C430@0.98:t=fill",
        drawtext("RDR2 HINDI", 62, 49, 34, "white", "arialbd.ttf", 2),
        "drawbox=x=1082:y=42:w=152:h=58:color=black@0.68:t=fill",
        drawtext(f"PART {part_number}", 1100, 54, 34, "0xF4C430", "arialbd.ttf", 2),
        drawtext(line1, 48, 225, 76, "white", "impact.ttf", 5),
        drawtext(line2, 48, 330, 96, "0xF4C430", "impact.ttf", 5),
        "drawbox=x=46:y=478:w=420:h=62:color=0xC91414@0.94:t=fill",
        drawtext("HINDI STORY CUT", 66, 491, 34, "white", "arialbd.ttf", 2),
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
            part.thumbnail_timestamp,
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


def render_thumbnails(ffmpeg: str, long_paths: list[Path]) -> dict[str, Path]:
    thumbnail_paths: dict[str, Path] = {}
    paths_by_name = {path.name: path for path in long_paths}
    for part in LONG_PARTS:
        long_path = paths_by_name.get(part.filename, LONG_DIR / part.filename)
        if long_path.exists():
            thumbnail_paths[part.filename] = render_thumbnail(ffmpeg, long_path, part)
    return thumbnail_paths


def review_frames(ffmpeg: str, video_path: Path, slug: str, duration: float) -> None:
    for label, timestamp in {"hook": 1.0, "middle": duration * 0.5, "end": max(1.0, duration - 1.5)}.items():
        run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-update",
                "1",
                "-q:v",
                "2",
                str(REVIEW_DIR / f"{slug}_{label}.jpg"),
            ]
        )


def review_contact_sheet(ffmpeg: str, video_path: Path, slug: str, duration: float, interval: int = 120) -> None:
    frames_dir = REVIEW_DIR / f"{slug}_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    timestamps = [float(value) for value in range(0, max(1, int(duration)), interval)]
    end_stamp = max(1.0, duration - 1.5)
    if not timestamps or end_stamp - timestamps[-1] > 30:
        timestamps.append(end_stamp)

    for index, seconds in enumerate(timestamps):
        frame = frames_dir / f"frame_{index:03d}.jpg"
        label = fmt_chapter_time(seconds).replace(":", r"\:")
        drawtext = (
            "scale=320:180,"
            "drawbox=x=0:y=0:w=320:h=24:color=black@0.72:t=fill,"
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
                drawtext,
                "-q:v",
                "3",
                str(frame),
            ]
        )

    cols = 4
    rows = 4
    page_size = cols * rows
    pages = (len(timestamps) + page_size - 1) // page_size
    for page in range(pages):
        start = page * page_size
        count = min(page_size, len(timestamps) - start)
        page_dir = frames_dir / f"page_{page + 1:02d}"
        page_dir.mkdir(parents=True, exist_ok=True)
        for old_frame in page_dir.glob("frame_*.jpg"):
            old_frame.unlink()
        for offset in range(count):
            src = frames_dir / f"frame_{start + offset:03d}.jpg"
            dst = page_dir / f"frame_{offset:03d}.jpg"
            dst.write_bytes(src.read_bytes())
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
                f"tile={cols}x{rows}",
                "-frames:v",
                "1",
                "-q:v",
                "3",
                str(REVIEW_DIR / f"{slug}_contact_page_{page + 1:02d}.jpg"),
            ]
        )


def write_metadata(short_paths: dict[str, Path], long_paths: list[Path]) -> None:
    rows = []
    for short in SHORTS:
        rows.append(
            {
                "output_type": "short",
                "upload_order": short.upload_order,
                "file": short_paths[short.slug].name,
                "title": short.title,
                "description": f"{short.description} Watch more Hindi gameplay highlights on MrLluminati Gaming.",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail": "",
                "chapters": "",
            }
        )
    long_paths_by_name = {path.name: path for path in long_paths}
    for part in LONG_PARTS:
        thumbnail_name = f"{part.slug}_thumbnail.jpg"
        rows.append(
            {
                "output_type": "long",
                "upload_order": part.upload_order,
                "file": long_paths_by_name.get(part.filename, LONG_DIR / part.filename).name,
                "title": part.title,
                "description": part.description,
                "hashtags": LONG_HASHTAGS,
                "tags": part.tags,
                "pinned_comment": part.pinned_comment,
                "thumbnail": thumbnail_name,
                "chapters": " | ".join(long_part_chapters(part)),
            }
        )
    csv_path = META_DIR / "rdr2_hindi_story_free_roam_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# RDR2 Hindi Story + Free Roam Upload Pack",
        "",
        "## Outputs",
    ]
    for row in rows:
        md_lines.extend(
            [
                f"### {row['file']}",
                f"- Type: {row['output_type']}",
                f"- Upload order: {row['upload_order']}",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                f"- Thumbnail: {row['thumbnail']}",
                f"- Chapters: {row['chapters']}",
                "",
            ]
        )
    (META_DIR / "rdr2_hindi_story_free_roam_metadata.md").write_text("\n".join(md_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RDR2 Hindi live Short Form and Long Form outputs.")
    parser.add_argument("--source", required=True, help="Local stream MP4")
    parser.add_argument("--skip-long", action="store_true", help="Only render Shorts")
    parser.add_argument("--only-long", action="store_true", help="Only render the long-form edit")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Do not render long-form thumbnails")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    short_paths: dict[str, Path] = {short.slug: SHORT_DIR / f"{short.slug}.mp4" for short in SHORTS}
    if not args.only_long:
        for short in SHORTS:
            print(f"Rendering short: {short.slug}")
            short_paths[short.slug] = render_short(ffmpeg, source, short)
            review_frames(ffmpeg, short_paths[short.slug], short.slug, short.duration)

    long_paths = [LONG_DIR / part.filename for part in LONG_PARTS]
    if not args.skip_long:
        print("Rendering long-form story parts")
        long_paths = render_long_form(ffmpeg, source)
        for part, long_path in zip(LONG_PARTS, long_paths):
            duration = long_part_duration(part)
            review_frames(ffmpeg, long_path, part.slug, duration)
            review_contact_sheet(ffmpeg, long_path, part.slug, duration)

    if not args.skip_thumbnails:
        print("Rendering long-form thumbnails")
        render_thumbnails(ffmpeg, long_paths)

    write_metadata(short_paths, long_paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Long form: {LONG_DIR}")
    print(f"Thumbnails: {THUMB_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
