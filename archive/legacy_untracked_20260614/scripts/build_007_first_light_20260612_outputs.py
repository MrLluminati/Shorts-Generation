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


PROJECT = "007_first_light_20260612"
PIPELINE = ROOT / "live_video_pipeline"
LONG_DIR = PIPELINE / "long_form" / PROJECT
SHORT_DIR = PIPELINE / "short_form" / PROJECT
THUMB_DIR = PIPELINE / "thumbnails" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"
LONG_WORK_DIR = WORK_DIR / "longform_segments"

DEFAULT_SOURCE = Path(r"C:\Users\abhik\Videos\2026-06-11_23-02-51.mp4")

LONG_FILE = "007_first_light_hindi_story_highlights_mrlluminati.mp4"
LONG_THUMB = "007_first_light_story_highlights_thumbnail.jpg"
CUSTOM_LONG_THUMB = "007_first_light_custom_thumbnail.jpg"

LONG_HASHTAGS = (
    "#007firstlight #jamesbond #bondgame #hindigaming #indiangaming "
    "#pcgaming #storygame #gameplaywalkthrough"
)
LONG_TAGS = (
    "007 first light, 007 first light gameplay, 007 first light hindi, james bond game, "
    "bond game, james bond gameplay hindi, hindi gaming, indian gaming, pc gameplay india, "
    "story gameplay, cinematic gameplay, 007 first light walkthrough, mrlluminati gaming"
)
SHORT_HASHTAGS = (
    "#007firstlight #jamesbond #bondgame #007game #hindigaming "
    "#indiangaming #pcgaming #gamingclips #shorts"
)
SHORT_TAGS = (
    "007 first light, 007 first light gameplay, 007 first light hindi, james bond game, "
    "bond game, james bond gameplay, hindi gaming, indian gaming, pc gameplay india, "
    "007 first light shorts, gaming shorts india, mrlluminati gaming"
)
DESCRIPTION_SUFFIX = (
    "Watch more Hindi gameplay highlights, story games, action moments, and PC gaming videos "
    "on MrLluminati Gaming."
)
AUDIO_QUALITY_NOTE = (
    "Apologies for the slightly rough audio quality in this recording; OBS captured duplicate audio, "
    "and I cleaned it as much as possible in editing."
)
ALREADY_UPLOADED_LONG_PARTS = {"part_01_opening_training"}
AUDIO_ECHO_DELAY_MS = 38
AUDIO_ECHO_CANCEL_VOLUME = -0.45


@dataclass(frozen=True)
class LongClip:
    label: str
    start: str
    end: str

    @property
    def duration(self) -> float:
        return parse_timecode(self.end) - parse_timecode(self.start)


@dataclass(frozen=True)
class LongPart:
    slug: str
    file: str
    title: str
    thumbnail: str
    summary: str
    clips: tuple[LongClip, ...]

    @property
    def duration(self) -> float:
        return sum(clip.duration for clip in self.clips)


@dataclass(frozen=True)
class ShortClip:
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


LONG_PARTS = (
    LongPart(
        slug="part_01_opening_training",
        file="007_first_light_hindi_part_01_opening_training.mp4",
        title="007 First Light Hindi Gameplay Part 1 - Training Begins | MrLluminati Gaming",
        thumbnail="007_first_light_part_01_thumbnail.jpg",
        summary="the loading transition, opening briefing, island drive, and training sequence.",
        clips=(
            LongClip("Loading, Briefing, Drive, And Training", "00:00:15.000", "00:24:08.000"),
        ),
    ),
    LongPart(
        slug="part_02_q_lab_story",
        file="007_first_light_hindi_part_02_q_lab_story.mp4",
        title="007 First Light Hindi Gameplay Part 2 - Q Lab Story Cut | MrLluminati Gaming",
        thumbnail="007_first_light_part_02_thumbnail.jpg",
        summary="the Q Branch debrief, lab story, apartment search, and February reveal.",
        clips=(
            LongClip("Debrief And Q Branch", "00:24:08.000", "00:37:18.000"),
            LongClip("Apartment Search And February Reveal", "00:43:18.000", "00:51:04.000"),
        ),
    ),
    LongPart(
        slug="part_03_escape_july_setup",
        file="007_first_light_hindi_part_03_escape_july_setup.mp4",
        title="007 First Light Hindi Gameplay Part 3 - Advanced Training And July Setup | MrLluminati Gaming",
        thumbnail="007_first_light_part_03_thumbnail.jpg",
        summary="the post-February dialogue, advanced training setup, and July transition before the night mission begins.",
        clips=(
            LongClip("Advanced Training And July Setup", "00:51:04.000", "01:06:12.000"),
        ),
    ),
    LongPart(
        slug="part_04_advanced_training_party_entry",
        file="007_first_light_hindi_part_04_advanced_training_party_entry.mp4",
        title="007 First Light Hindi Gameplay Part 4 - Night Mission Clean Run | MrLluminati Gaming",
        thumbnail="007_first_light_part_04_thumbnail.jpg",
        summary="the night mission clean run, with the failed restart and pause-menu attempt removed.",
        clips=(
            LongClip("Night Mission Setup", "01:06:12.000", "01:16:27.000"),
            LongClip("Successful Checkpoint Run", "01:21:00.000", "01:22:28.000"),
        ),
    ),
    LongPart(
        slug="part_05_gala_crowd_finale",
        file="007_first_light_hindi_part_05_gala_crowd_finale.mp4",
        title="007 First Light Hindi Gameplay Part 5 - Nightclub Finale | MrLluminati Gaming",
        thumbnail="007_first_light_part_05_thumbnail.jpg",
        summary="the nightclub invitation, club infiltration, and finale sequence.",
        clips=(
            LongClip("Nightclub Invitation And Finale", "01:22:38.000", "01:47:08.000"),
        ),
    ),
)

SHORTS = (
    ShortClip(
        slug="01_drive_through",
        start="00:13:43.000",
        duration=17.0,
        hook="THE DRIVE\nGOT MESSY",
        beat_one="OBJECTIVE SET",
        beat_two="KEEP MOVING",
        title="The Drive Got Messy | 007 First Light Hindi #shorts",
        description_lead="A fast drive-through objective moment from the 007 First Light Hindi gameplay recording.",
        tags=f"{SHORT_TAGS}, 007 driving, drive through, bond car gameplay",
        pinned_comment="Would you push through or slow down here?",
        thumbnail_text="DRIVE THROUGH",
        upload_order=1,
    ),
    ShortClip(
        slug="02_beach_drive_turn",
        start="00:17:14.500",
        duration=19.0,
        hook="THE DRIVE\nGOT TENSE",
        beat_one="NO SLOWDOWN",
        beat_two="BAD ROAD",
        title="The Drive Got Tense | 007 First Light Hindi #shorts",
        description_lead="The island drive turns tense fast in this 007 First Light gameplay moment.",
        tags=f"{SHORT_TAGS}, 007 driving, james bond driving, bond car gameplay",
        pinned_comment="Would you slow down here or push it?",
        thumbnail_text="TENSE DRIVE",
        upload_order=2,
    ),
    ShortClip(
        slug="03_balcony_door_fight",
        start="00:21:30.000",
        duration=19.0,
        hook="THE DOOR FIGHT\nSTARTED FAST",
        beat_one="NO COVER",
        beat_two="PUSH THROUGH",
        title="Door Fight Started Fast | 007 First Light Hindi #shorts",
        description_lead="A fast door fight from the early mission section of 007 First Light.",
        tags=f"{SHORT_TAGS}, door fight, 007 action, first light combat",
        pinned_comment="Would you push or wait for backup?",
        thumbnail_text="DOOR FIGHT",
        upload_order=3,
    ),
    ShortClip(
        slug="04_february_reveal",
        start="00:50:48.000",
        duration=13.0,
        hook="THE MONTH\nCHANGED",
        beat_one="STORY TURN",
        beat_two="FEBRUARY",
        title="The February Reveal | 007 First Light Hindi #shorts",
        description_lead="A clean story-card reveal from the 007 First Light recording.",
        tags=f"{SHORT_TAGS}, 007 story reveal, february reveal, bond story game",
        pinned_comment="Did this time jump land for you?",
        thumbnail_text="FEBRUARY",
        upload_order=6,
    ),
    ShortClip(
        slug="05_corridor_gunfight",
        start="01:05:28.000",
        duration=16.5,
        hook="CORRIDOR FIGHT\nSTARTED",
        beat_one="FIRST SHOT",
        beat_two="KEEP MOVING",
        title="Corridor Fight Started Fast | 007 First Light Hindi #shorts",
        description_lead="A short corridor gunfight cut straight to the action.",
        tags=f"{SHORT_TAGS}, corridor gunfight, bond combat, 007 first light action",
        pinned_comment="Clean fight or messy survival?",
        thumbnail_text="CORRIDOR FIGHT",
        upload_order=4,
    ),
    ShortClip(
        slug="06_party_fight_turn",
        start="01:17:26.000",
        duration=17.5,
        hook="THE PARTY\nTURNED LOUD",
        beat_one="LIGHTS ON",
        beat_two="FIGHT STARTS",
        title="The Party Turned Loud | 007 First Light Hindi #shorts",
        description_lead="A party scene flips into action during the 007 First Light mission.",
        tags=f"{SHORT_TAGS}, party fight, bond party scene, 007 action clip",
        pinned_comment="Best party entrance or worst idea?",
        thumbnail_text="PARTY FIGHT",
        upload_order=5,
    ),
    ShortClip(
        slug="07_blue_room_sneak",
        start="01:27:48.500",
        duration=18.0,
        hook="SNEAKING THROUGH\nTHE CLUB",
        beat_one="STAY LOW",
        beat_two="BAD TIMING",
        title="Sneaking Through The Club | 007 First Light Hindi #shorts",
        description_lead="A tense club stealth moment from the 007 First Light gameplay.",
        tags=f"{SHORT_TAGS}, club stealth, 007 stealth, james bond stealth gameplay",
        pinned_comment="Would you sneak or rush this room?",
        thumbnail_text="CLUB STEALTH",
        upload_order=7,
    ),
    ShortClip(
        slug="08_final_crowd_moment",
        start="01:44:28.000",
        duration=23.0,
        hook="THE CROWD SCENE\nGOT INTENSE",
        beat_one="NO WAY OUT",
        beat_two="FINAL TURN",
        title="The Crowd Scene Got Intense | 007 First Light Hindi #shorts",
        description_lead="A late-game crowd moment turns into one of the most intense scenes in the recording.",
        tags=f"{SHORT_TAGS}, 007 crowd scene, bond finale, first light ending moment",
        pinned_comment="Was this the strongest scene of the recording?",
        thumbnail_text="CROWD SCENE",
        upload_order=8,
    ),
    ShortClip(
        slug="09_training_takedown",
        start="00:15:14.000",
        duration=18.0,
        hook="TRAINING GOT\nPERSONAL",
        beat_one="FIRST TEST",
        beat_two="CLEAN TAKEDOWN",
        title="Training Takedown Went Clean | 007 First Light Hindi #shorts",
        description_lead="A quick training takedown moment from the early 007 First Light mission.",
        tags=f"{SHORT_TAGS}, 007 training, bond training, hand to hand combat, takedown gameplay",
        pinned_comment="Would you pass this training test first try?",
        thumbnail_text="TRAINING TAKEDOWN",
        upload_order=9,
    ),
    ShortClip(
        slug="10_first_shootout",
        start="00:17:55.500",
        duration=11.5,
        hook="FIRST SHOOTOUT\nHIT FAST",
        beat_one="NO WARNING",
        beat_two="QUICK SHOTS",
        title="First Shootout Hit Fast | 007 First Light Hindi #shorts",
        description_lead="The first shootout section hits quickly in this 007 First Light gameplay clip.",
        tags=f"{SHORT_TAGS}, 007 shootout, bond gunfight, quick kills, action gameplay",
        pinned_comment="Was this clean aim or pure panic?",
        thumbnail_text="FIRST SHOOTOUT",
        upload_order=10,
    ),
    ShortClip(
        slug="11_lab_fight",
        start="00:20:45.000",
        duration=18.0,
        hook="THE LAB FIGHT\nGOT HEAVY",
        beat_one="CLOSE RANGE",
        beat_two="NO ESCAPE",
        title="The Lab Fight Got Heavy | 007 First Light Hindi #shorts",
        description_lead="A close-range fight sequence from the 007 First Light training mission.",
        tags=f"{SHORT_TAGS}, lab fight, 007 combat, bond hand combat, action shorts",
        pinned_comment="Hand-to-hand fights or gunfights: which works better for Shorts?",
        thumbnail_text="LAB FIGHT",
        upload_order=11,
    ),
    ShortClip(
        slug="12_night_mission_entry",
        start="01:06:15.000",
        duration=18.0,
        hook="NIGHT MISSION\nSTARTED SILENT",
        beat_one="STAY LOW",
        beat_two="FIRST MOVE",
        title="Night Mission Started Silent | 007 First Light Hindi #shorts",
        description_lead="The night mission begins with a quiet infiltration setup in 007 First Light.",
        tags=f"{SHORT_TAGS}, night mission, stealth gameplay, 007 stealth, bond infiltration",
        pinned_comment="Silent entry or loud entry?",
        thumbnail_text="NIGHT MISSION",
        upload_order=12,
    ),
    ShortClip(
        slug="13_rooftop_takedown",
        start="01:16:09.000",
        duration=18.0,
        hook="ROOFTOP GUARD\nWENT DOWN",
        beat_one="CLOSE IN",
        beat_two="NO ALARM",
        title="Rooftop Guard Went Down | 007 First Light Hindi #shorts",
        description_lead="A clean rooftop takedown from the night mission section.",
        tags=f"{SHORT_TAGS}, rooftop takedown, stealth takedown, 007 night mission, bond stealth",
        pinned_comment="Clean stealth or risky move?",
        thumbnail_text="ROOFTOP TAKEDOWN",
        upload_order=13,
    ),
    ShortClip(
        slug="14_checkpoint_run",
        start="01:21:00.000",
        duration=25.0,
        hook="THE CHECKPOINT\nRUN WORKED",
        beat_one="KEEP MOVING",
        beat_two="MISSION SAVED",
        title="Checkpoint Run Worked | 007 First Light Hindi #shorts",
        description_lead="The successful checkpoint run after the messy attempt, trimmed to the clean playable moment.",
        tags=f"{SHORT_TAGS}, checkpoint run, 007 mission, clean run, stealth escape",
        pinned_comment="Would you call this clean recovery?",
        thumbnail_text="CHECKPOINT RUN",
        upload_order=14,
    ),
    ShortClip(
        slug="15_nightclub_mission",
        start="01:23:00.000",
        duration=24.0,
        hook="THE NIGHTCLUB\nMISSION STARTED",
        beat_one="NEW LEAD",
        beat_two="BLEND IN",
        title="Nightclub Mission Started | 007 First Light Hindi #shorts",
        description_lead="The mission shifts into the nightclub sequence with a new lead and a different pace.",
        tags=f"{SHORT_TAGS}, nightclub mission, 007 nightclub, bond mission, stealth club gameplay",
        pinned_comment="Did the nightclub section look better than the training section?",
        thumbnail_text="NIGHTCLUB MISSION",
        upload_order=15,
    ),
    ShortClip(
        slug="16_final_table_reveal",
        start="01:45:30.000",
        duration=24.0,
        hook="THE TABLE SCENE\nFELT IMPORTANT",
        beat_one="EVERYONE STOPS",
        beat_two="NEXT TARGET",
        title="Final Table Reveal | 007 First Light Hindi #shorts",
        description_lead="A late mission table scene sets up the next story beat in 007 First Light.",
        tags=f"{SHORT_TAGS}, table scene, 007 story, bond cutscene, final reveal",
        pinned_comment="Story scene or action scene: which one should I upload more?",
        thumbnail_text="TABLE REVEAL",
        upload_order=16,
    ),
)


def ensure_dirs() -> None:
    for directory in (LONG_DIR, SHORT_DIR, THUMB_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR, LONG_WORK_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


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


def ffmpeg_text(value: str) -> str:
    return value.replace("\\", r"\\").replace(":", r"\:").replace("'", r"\'").replace("%", r"\%")


def drawtext(text: str, x: str | int, y: str | int, size: int, color: str = "white", border: int = 3) -> str:
    return (
        f"drawtext=text='{ffmpeg_text(text)}':x={x}:y={y}:fontsize={size}:"
        f"fontcolor={color}:borderw={border}:bordercolor=black@0.95"
    )


def encode_args() -> list[str]:
    return [
        "-c:v",
        "h264_nvenc",
        "-preset",
        "p5",
        "-tune",
        "hq",
        "-cq",
        "19",
        "-b:v",
        "0",
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
    ]


def make_card(ffmpeg: str, title: str, index: int) -> Path:
    out = LONG_WORK_DIR / f"{index:03d}_card.mp4"
    duration = 0.85
    vf = ",".join(
        [
            "drawbox=x=0:y=0:w=2560:h=1440:color=0x030507@1:t=fill",
            "drawbox=x=0:y=0:w=2560:h=1440:color=0x122B3A@0.35:t=fill",
            "drawbox=x=0:y=0:w=2560:h=1440:color=black@0.22:t=fill",
            "drawbox=x=244:y=508:w=12:h=200:color=0xF4C430@0.96:t=fill",
            drawtext("MRLLUMINATI GAMING", 264, 446, 34, "white", 2),
            drawtext(title.upper(), 278, 546, 78, "white", 5),
            drawtext("007 FIRST LIGHT HINDI STORY CUT", 278, 660, 38, "0xF4C430", 3),
            "format=yuv420p",
        ]
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
            f"color=c=0x030507:s=2560x1440:r=60:d={duration:.3f}",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=channel_layout=stereo:sample_rate=48000:d={duration:.3f}",
            "-vf",
            vf,
            *encode_args(),
            "-shortest",
            str(out),
        ]
    )
    return out


def render_long_clip(ffmpeg: str, source: Path, clip: LongClip, index: int, work_dir: Path = LONG_WORK_DIR) -> Path:
    safe_label = "".join(ch if ch.isalnum() else "_" for ch in clip.label.lower()).strip("_")
    out = work_dir / f"{index:03d}_{safe_label}.mp4"
    fade = 0.18
    fade_out = max(0.0, clip.duration - fade)
    vf = ",".join(
        [
            "fps=60",
            "eq=contrast=1.04:saturation=1.06:brightness=0.002",
            "unsharp=5:5:0.28",
            f"fade=t=in:st=0:d={fade:.3f}",
            f"fade=t=out:st={fade_out:.3f}:d={fade:.3f}",
            "drawbox=x=0:y=0:w=2560:h=62:color=black@0.16:t=fill",
            drawtext("MRLLUMINATI GAMING", "w-tw-42", 22, 24, "white", 1),
            "format=yuv420p",
        ]
    )
    af = (
        "aresample=48000,volume=1.03,alimiter=limit=0.97,"
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
            f"{clip.duration:.3f}",
            "-i",
            str(source),
            "-vf",
            vf,
            "-af",
            af,
            *encode_args(),
            str(out),
        ]
    )
    return out


def concat_videos(ffmpeg: str, pieces: list[Path], out_path: Path, work_dir: Path = LONG_WORK_DIR) -> None:
    list_path = work_dir / f"{out_path.stem}_concat.txt"
    list_path.write_text(
        "\n".join(f"file '{piece.as_posix()}'" for piece in pieces),
        encoding="utf-8",
    )
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
            str(list_path),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(out_path),
        ]
    )


def long_chapters(part: LongPart) -> list[str]:
    elapsed = 0.0
    chapters = []
    for clip in part.clips:
        chapters.append(f"{fmt_time(elapsed)} {clip.label}")
        elapsed += clip.duration
    return chapters


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_short_ass(short: ShortClip) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    duration = short.duration
    second_start = min(max(duration - 5.0, 6.2), max(6.2, duration - 2.8))
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
        "Style: Logo,Arial,27,&H00FFFFFF,&H000000FF,&HAA000000,&HAA000000,-1,0,0,0,100,100,1,0,1,2,0,8,36,36,34,1",
        "Style: Hook,Arial Black,66,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,6,2,8,54,54,176,1",
        "Style: Beat,Arial Black,42,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,1,0,1,4,1,2,62,62,205,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 6,{ass_time(0)},{ass_time(duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.12)},{ass_time(2.85)},Hook,,0,0,0,,"
            r"{\fad(80,180)\t(0,260,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 8,{ass_time(3.15)},{ass_time(min(6.5, duration - 0.7))},Beat,,0,0,0,,"
            r"{\fad(90,160)}"
            f"{ass_escape(short.beat_one)}"
        ),
        (
            f"Dialogue: 8,{ass_time(second_start)},{ass_time(max(second_start + 1.8, duration - 0.55))},Beat,,0,0,0,,"
            r"{\fad(90,180)}"
            f"{ass_escape(short.beat_two)}"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, source: Path, short: ShortClip) -> Path:
    ass_path = write_short_ass(short)
    out = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.35)
    vf = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=24:1,eq=brightness=-0.08:saturation=1.05[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=655:w=1080:h=3:color=white@0.12:t=fill,"
        "drawbox=x=0:y=1262:w=1080:h=3:color=white@0.12:t=fill,"
        "eq=contrast=1.05:saturation=1.08:brightness=0.006,"
        "unsharp=5:5:0.38,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.10,"
        f"fade=t=out:st={fade_out:.3f}:d=0.35,"
        "format=yuv420p[v]"
    )
    af = (
        "[0:a]aresample=48000,asplit=2[dry][echo];"
        f"[echo]adelay={AUDIO_ECHO_DELAY_MS}|{AUDIO_ECHO_DELAY_MS},"
        f"volume={AUDIO_ECHO_CANCEL_VOLUME}[cancel];"
        "[dry][cancel]amix=inputs=2:normalize=0,highpass=f=55,"
        "acompressor=threshold=-18dB:ratio=2.2:attack=8:release=120,"
        "volume=1.12,alimiter=limit=0.97,"
        "afade=t=in:st=0:d=0.08,"
        f"afade=t=out:st={fade_out:.3f}:d=0.35[a]"
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
            f"{vf};{af}",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "h264_nvenc",
            "-preset",
            "p5",
            "-tune",
            "hq",
            "-cq",
            "20",
            "-b:v",
            "0",
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
            str(out),
        ]
    )
    return out


def review_frame(ffmpeg: str, video: Path, name: str, second: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
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
            str(video),
            "-frames:v",
            "1",
            str(out),
        ]
    )


def make_short_review(ffmpeg: str, video: Path, short: ShortClip) -> None:
    frame_dir = REVIEW_DIR / "shorts_frames" / short.slug
    review_frame(ffmpeg, video, short.slug, 0.6, frame_dir / "hook.jpg")
    review_frame(ffmpeg, video, short.slug, min(short.duration * 0.45, short.duration - 0.8), frame_dir / "middle.jpg")
    review_frame(ffmpeg, video, short.slug, max(0.8, short.duration - 1.0), frame_dir / "payoff.jpg")
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-vf",
            "fps=1/2,scale=180:-1,tile=5x2",
            "-frames:v",
            "1",
            str(REVIEW_DIR / f"{short.slug}_contact.jpg"),
        ]
    )


def make_long_review(ffmpeg: str, video: Path, part: LongPart) -> None:
    frame_dir = REVIEW_DIR / "longform_frames" / part.slug
    total = part.duration
    for label, sec in (
        ("hook", 20.0),
        ("quarter", total * 0.25),
        ("middle", total * 0.50),
        ("ending", max(1.0, total - 20.0)),
    ):
        review_frame(ffmpeg, video, label, sec, frame_dir / f"{label}.jpg")


def make_long_thumbnail(ffmpeg: str, source: Path) -> None:
    out = THUMB_DIR / LONG_THUMB
    vf = ",".join(
        [
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
            "eq=contrast=1.08:saturation=1.10:brightness=-0.01",
            "drawbox=x=0:y=0:w=1280:h=720:color=black@0.20:t=fill",
            "drawbox=x=0:y=0:w=1280:h=116:color=black@0.68:t=fill",
            "drawbox=x=0:y=586:w=1280:h=134:color=black@0.74:t=fill",
            drawtext("007 FIRST LIGHT", 54, 28, 58, "white", 4),
            drawtext("HINDI STORY HIGHLIGHTS", 54, 616, 48, "0xF4C430", 4),
            drawtext("MRLLUMINATI GAMING", "w-tw-46", 666, 28, "white", 2),
            "format=yuvj420p",
        ]
    )
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            "01:44:39.000",
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-vf",
            vf,
            "-q:v",
            "2",
            str(out),
        ]
    )


def write_metadata(long_paths: dict[str, Path], short_paths: dict[str, Path]) -> None:
    recommended_thumb = CUSTOM_LONG_THUMB if (THUMB_DIR / CUSTOM_LONG_THUMB).exists() else LONG_THUMB
    long_rows = []
    for index, part in enumerate(LONG_PARTS, 1):
        if part.slug in ALREADY_UPLOADED_LONG_PARTS:
            continue
        chapters = long_chapters(part)
        thumbnail = part.thumbnail if (THUMB_DIR / part.thumbnail).exists() else recommended_thumb
        long_description = (
            f"007 First Light Hindi gameplay Part {index}. This part covers {part.summary} "
            f"{AUDIO_QUALITY_NOTE} {DESCRIPTION_SUFFIX}\n\nChapters:\n" + "\n".join(chapters)
        )
        long_rows.append(
            {
                "upload_order": index,
                "file": long_paths[part.slug].name,
                "title": part.title,
                "duration": fmt_time(part.duration),
                "description": long_description,
                "hashtags": LONG_HASHTAGS,
                "tags": LONG_TAGS,
                "thumbnail": thumbnail,
                "chapters": " | ".join(chapters),
            }
        )
    with (META_DIR / "007_first_light_20260612_longform_metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(long_rows[0].keys()))
        writer.writeheader()
        writer.writerows(long_rows)

    short_rows = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        short_rows.append(
            {
                "upload_order": short.upload_order,
                "file": short_paths[short.slug].name,
                "source_start": short.start,
                "duration_seconds": short.duration,
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": SHORT_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )
    with (META_DIR / "007_first_light_20260612_shorts_metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(short_rows[0].keys()))
        writer.writeheader()
        writer.writerows(short_rows)

    md = [
        "# 007 First Light 2026-06-12 Outputs",
        "",
        "## Longform Parts",
        "- Part 1 has already been uploaded. Use the entries below for Part 2 onward.",
        "",
    ]
    for row in long_rows:
        md.extend(
            [
                f"### {row['upload_order']}. {row['file']}",
                f"- Title: {row['title']}",
                f"- Duration target: {row['duration']}",
                f"- Thumbnail: {row['thumbnail']}",
                *([f"- Backup thumbnail: {LONG_THUMB}"] if row["thumbnail"] != LONG_THUMB else []),
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                "- Chapters:",
                *[f"  - {chapter}" for chapter in row["chapters"].split(" | ")],
                "",
            ]
        )
    md.extend(["## Shorts"])
    for row in short_rows:
        md.extend(
            [
                f"### {row['upload_order']}. {row['file']}",
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
    (META_DIR / "007_first_light_20260612_metadata.md").write_text("\n".join(md), encoding="utf-8")


def verify(ffmpeg: str, paths: list[Path]) -> None:
    for path in paths:
        run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"])


def render_longform(ffmpeg: str, source: Path, only_slug: str | None = None) -> dict[str, Path]:
    outputs: dict[str, Path] = {}
    for part in LONG_PARTS:
        if only_slug and part.slug != only_slug:
            continue
        work_dir = LONG_WORK_DIR / part.slug
        work_dir.mkdir(parents=True, exist_ok=True)
        for old in work_dir.glob("*"):
            if old.is_file():
                old.unlink()
        pieces: list[Path] = []
        for index, clip in enumerate(part.clips, 1):
            print(f"Rendering {part.slug}: {clip.label}")
            pieces.append(render_long_clip(ffmpeg, source, clip, index, work_dir))
        out = LONG_DIR / part.file
        print(f"Concatenating {part.slug}")
        concat_videos(ffmpeg, pieces, out, work_dir)
        outputs[part.slug] = out
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 007 First Light 2026-06-12 longform and Shorts.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local recording MP4")
    parser.add_argument("--skip-long", action="store_true", help="Only render Shorts")
    parser.add_argument("--skip-shorts", action="store_true", help="Only render longform")
    parser.add_argument("--long-part", choices=[part.slug for part in LONG_PARTS], help="Render only one longform part")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    long_paths: dict[str, Path] = {
        part.slug: LONG_DIR / part.file
        for part in LONG_PARTS
        if (LONG_DIR / part.file).exists()
    }
    if not args.skip_long:
        long_paths.update(render_longform(ffmpeg, source, args.long_part))
        for part in LONG_PARTS:
            if args.long_part and part.slug != args.long_part:
                continue
            make_long_review(ffmpeg, long_paths[part.slug], part)
        make_long_thumbnail(ffmpeg, source)

    short_paths: dict[str, Path] = {
        short.slug: SHORT_DIR / f"{short.slug}.mp4"
        for short in SHORTS
        if (SHORT_DIR / f"{short.slug}.mp4").exists()
    }
    if not args.skip_shorts:
        for short in SHORTS:
            print(f"Rendering Short: {short.slug}")
            out = render_short(ffmpeg, source, short)
            short_paths[short.slug] = out
            make_short_review(ffmpeg, out, short)

    missing = [short.slug for short in SHORTS if short.slug not in short_paths]
    if missing:
        raise SystemExit(f"Missing rendered shorts: {', '.join(missing)}")
    missing_long = [part.slug for part in LONG_PARTS if part.slug not in long_paths]
    if missing_long:
        raise SystemExit(f"Missing longform outputs: {', '.join(missing_long)}")

    verify(ffmpeg, [*[long_paths[p.slug] for p in LONG_PARTS], *[short_paths[s.slug] for s in SHORTS]])
    write_metadata(long_paths, short_paths)
    print(f"Longform parts: {LONG_DIR}")
    print(f"Shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    recommended_thumb = CUSTOM_LONG_THUMB if (THUMB_DIR / CUSTOM_LONG_THUMB).exists() else LONG_THUMB
    print(f"Thumbnail: {THUMB_DIR / recommended_thumb}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
