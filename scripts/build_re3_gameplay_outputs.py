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


PROJECT = "re3_remake_no_commentary"
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
    "#residentevil #residentevil3 #re3remake #jillvalentine #nemesis "
    "#survivalhorror #horrorgaming #gameplayclips #pcgaming #shorts"
)
LONG_HASHTAGS = (
    "#residentevil #residentevil3 #re3remake #jillvalentine "
    "#nemesis #survivalhorror #horrorgaming #pcgaming"
)
BASE_TAGS = (
    "resident evil 3, resident evil 3 remake, re3 remake, re3 gameplay, "
    "resident evil gameplay, jill valentine, nemesis resident evil, "
    "raccoon city, survival horror, horror gameplay, horror gaming, "
    "no commentary gameplay, pc gameplay, gameplay walkthrough, gaming shorts, "
    "gameplay clips, resident evil shorts, resident evil remake, resident evil 2026"
)
SHORT_DESCRIPTION_SUFFIX = (
    "Watch more Resident Evil and horror gameplay highlights on MrLluminati Gaming."
)
LONG_CARD_DURATION = 1.45


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
        slug="01_nemesis_apartment_break_in",
        start="00:11:20.000",
        duration=58.0,
        hook="NEMESIS\nBROKE IN",
        title="Nemesis Breaks Into Jill's Apartment | RE3 Remake #shorts",
        description="Nemesis makes the Resident Evil 3 Remake opening instantly terrifying.",
        tags=f"{BASE_TAGS}, nemesis chase, jill apartment, re3 opening, resident evil 3 nemesis",
        pinned_comment="Would you survive this opening chase?",
        upload_order=1,
    ),
    ShortSpec(
        slug="02_city_escape_fire",
        start="00:14:10.000",
        duration=55.0,
        hook="RACCOON CITY\nIS BURNING",
        title="Raccoon City Is Already Burning | RE3 Remake #shorts",
        description="Jill's escape turns into pure chaos as Raccoon City collapses around her.",
        tags=f"{BASE_TAGS}, raccoon city, re3 city escape, jill valentine escape, zombie outbreak",
        pinned_comment="Best Resident Evil opening: RE2 or RE3?",
        upload_order=2,
    ),
    ShortSpec(
        slug="03_carlos_saves_jill",
        start="00:19:55.000",
        duration=48.0,
        hook="CARLOS SAVED\nJILL",
        title="Carlos Saves Jill From Nemesis | RE3 Remake #shorts",
        description="The first Carlos and Jill moment hits right after Nemesis corners her.",
        tags=f"{BASE_TAGS}, carlos oliveira, carlos saves jill, re3 cutscene, nemesis escape",
        pinned_comment="Carlos arrived at the perfect second. Agree?",
        upload_order=3,
    ),
    ShortSpec(
        slug="04_drain_deimos_ambush",
        start="00:59:15.000",
        duration=55.0,
        hook="THE POWER STATION\nWENT WRONG",
        title="Power Station Ambush | RE3 Remake #shorts",
        description="The power station section turns into one of RE3 Remake's nastiest horror moments.",
        tags=f"{BASE_TAGS}, drain deimos, power station, re3 horror moment, survival horror shorts",
        pinned_comment="This section still feels disgusting. Too much or perfect horror?",
        upload_order=4,
    ),
    ShortSpec(
        slug="05_nemesis_flamethrower",
        start="01:51:25.000",
        duration=58.0,
        hook="NEMESIS BROUGHT\nA FLAMETHROWER",
        title="Nemesis Brought A Flamethrower | RE3 Remake #shorts",
        description="Nemesis upgrades the chase with a flamethrower and turns the street into a boss arena.",
        tags=f"{BASE_TAGS}, nemesis flamethrower, re3 boss fight, resident evil boss, jill vs nemesis",
        pinned_comment="Which Nemesis weapon is scarier: flamethrower or rocket launcher?",
        upload_order=5,
    ),
    ShortSpec(
        slug="06_hospital_horde_defense",
        start="03:39:25.000",
        duration=58.0,
        hook="HOSPITAL HOLDOUT\nSTARTED",
        title="Hospital Horde Defense | RE3 Remake #shorts",
        description="Carlos has to hold the hospital line while zombies flood the room.",
        tags=f"{BASE_TAGS}, hospital defense, carlos hospital, zombie horde, resident evil hospital",
        pinned_comment="Would you barricade first or start shooting?",
        upload_order=6,
    ),
    ShortSpec(
        slug="07_final_nemesis_fight",
        start="04:38:40.000",
        duration=58.0,
        hook="FINAL NEMESIS\nFIGHT",
        title="Final Nemesis Fight Begins | RE3 Remake #shorts",
        description="The final Nemesis encounter begins with Jill trapped in the last arena.",
        tags=f"{BASE_TAGS}, final nemesis, re3 final boss, resident evil final boss, jill vs nemesis",
        pinned_comment="Is this final form terrifying or over the top?",
        upload_order=7,
    ),
    ShortSpec(
        slug="08_railgun_finish",
        start="04:43:20.000",
        duration=55.0,
        hook="THE RAILGUN\nENDED IT",
        title="The Railgun Ended Nemesis | RE3 Remake #shorts",
        description="Jill finishes Nemesis with the railgun in one of RE3 Remake's biggest moments.",
        tags=f"{BASE_TAGS}, railgun nemesis, re3 railgun, nemesis death, resident evil ending",
        pinned_comment="Was this the most satisfying Nemesis finish?",
        upload_order=8,
    ),
]


LONG_PARTS = [
    LongPart(
        slug="re3_part_01_nemesis_city_escape",
        filename="re3_part_01_nemesis_city_escape.mp4",
        title="Resident Evil 3 Remake: Nemesis City Escape | No Commentary Part 1",
        description=(
            "Jill Valentine's nightmare begins in Raccoon City. This story-first RE3 Remake "
            "cut keeps the opening chase, Nemesis attack, city escape, Carlos rescue, and "
            "subway dialogue together while skipping menu downtime."
        ),
        tags=f"{BASE_TAGS}, re3 opening, nemesis chase, jill valentine city escape, carlos saves jill",
        pinned_comment="Did RE3 Remake's opening hook you faster than RE2 Remake?",
        thumbnail_text=("NEMESIS", "CITY ESCAPE"),
        thumbnail_timestamp="00:04:30.000",
        upload_order=9,
        clips=(
            LongClip("NEMESIS CITY ESCAPE", "00:10:30.000", "00:26:10.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_02_downtown_route",
        filename="re3_part_02_downtown_route.mp4",
        title="Resident Evil 3 Remake: Downtown Route Opens Up | No Commentary Part 2",
        description=(
            "Jill gets control of downtown while Raccoon City keeps closing in. This cut keeps "
            "the useful route progress and survival pressure, then drops the slow inventory loops."
        ),
        tags=f"{BASE_TAGS}, downtown raccoon city, re3 downtown, jill valentine gameplay, zombie outbreak",
        pinned_comment="Downtown Raccoon City still has the best RE3 atmosphere. Agree?",
        thumbnail_text=("DOWNTOWN", "ESCAPE"),
        thumbnail_timestamp="00:10:00.000",
        upload_order=10,
        clips=(
            LongClip("DOWNTOWN ROUTE", "00:26:10.000", "00:44:30.000", "gameplay", True),
        ),
    ),
    LongPart(
        slug="re3_part_03_power_station_horror",
        filename="re3_part_03_power_station_horror.mp4",
        title="Resident Evil 3 Remake: Power Station Horror | No Commentary Part 3",
        description=(
            "Jill reaches the power station and RE3 Remake turns from action escape into nasty "
            "survival horror. The Drain Deimos sequence is kept as a continuous horror block."
        ),
        tags=f"{BASE_TAGS}, power station, drain deimos, re3 horror moment, survival horror gameplay",
        pinned_comment="Was the power station the grossest section of RE3 Remake?",
        thumbnail_text=("POWER STATION", "HORROR"),
        thumbnail_timestamp="00:10:30.000",
        upload_order=11,
        clips=(
            LongClip("POWER STATION HORROR", "00:52:30.000", "01:10:45.000", "gameplay", True),
        ),
    ),
    LongPart(
        slug="re3_part_04_subway_route",
        filename="re3_part_04_subway_route.mp4",
        title="Resident Evil 3 Remake: Subway Route Mission | No Commentary Part 4",
        description=(
            "The subway route gets set while Jill, Carlos, and the city are pushed toward the "
            "next Nemesis encounter. Story dialogue and route progress stay together."
        ),
        tags=f"{BASE_TAGS}, subway route, re3 subway, carlos oliveira, jill valentine mission",
        pinned_comment="Subway routing: tense mission design or too much backtracking?",
        thumbnail_text=("SUBWAY", "ROUTE"),
        thumbnail_timestamp="00:08:00.000",
        upload_order=12,
        clips=(
            LongClip("SUBWAY ROUTE", "01:17:15.000", "01:34:30.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_05_flamethrower_nemesis",
        filename="re3_part_05_flamethrower_nemesis.mp4",
        title="Resident Evil 3 Remake: Flamethrower Nemesis Boss Fight | Part 5",
        description=(
            "Nemesis comes back with a flamethrower and the chase turns into a full boss fight. "
            "The setup, fight, and payoff stay in one continuous block."
        ),
        tags=f"{BASE_TAGS}, nemesis flamethrower, re3 boss fight, resident evil boss, jill vs nemesis",
        pinned_comment="Which is scarier: Nemesis chasing you or Nemesis with a flamethrower?",
        thumbnail_text=("FLAMETHROWER", "NEMESIS"),
        thumbnail_timestamp="00:10:00.000",
        upload_order=13,
        clips=(
            LongClip("NEMESIS FLAMETHROWER", "01:50:20.000", "02:06:00.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_06_carlos_rpd",
        filename="re3_part_06_carlos_rpd.mp4",
        title="Resident Evil 3 Remake: Carlos Enters RPD | No Commentary Part 6",
        description=(
            "Carlos takes over at the RPD. This cut keeps the police-station story setup, key dialogue, "
            "and vaccine lead while trimming puzzle and backtracking filler."
        ),
        tags=f"{BASE_TAGS}, carlos rpd, raccoon police department, rpd gameplay, vaccine dialogue",
        pinned_comment="Carlos at the RPD: good change of pace or too much backtracking?",
        thumbnail_text=("CARLOS", "RPD"),
        thumbnail_timestamp="00:10:15.000",
        upload_order=14,
        clips=(
            LongClip("CARLOS ENTERS RPD", "02:15:00.000", "02:27:30.000", "dialogue", True),
            LongClip("VACCINE LEAD", "02:47:00.000", "02:50:15.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_07_clock_tower_escape",
        filename="re3_part_07_clock_tower_escape.mp4",
        title="Resident Evil 3 Remake: Clock Tower Escape | No Commentary Part 7",
        description=(
            "Jill pushes through the city after the RPD section, with Nemesis pressure building "
            "again around the clock tower route. This cut keeps the action readable and continuous."
        ),
        tags=f"{BASE_TAGS}, clock tower, nemesis chase, re3 city fight, jill valentine escape",
        pinned_comment="This stretch feels more like action-horror. Did it work for you?",
        thumbnail_text=("CLOCK TOWER", "ESCAPE"),
        thumbnail_timestamp="00:04:30.000",
        upload_order=15,
        clips=(
            LongClip("CLOCK TOWER ESCAPE", "02:50:15.000", "03:05:45.000", "gameplay", True),
        ),
    ),
    LongPart(
        slug="re3_part_08_hospital_holdout",
        filename="re3_part_08_hospital_holdout.mp4",
        title="Resident Evil 3 Remake: Hospital Holdout | No Commentary Part 8",
        description=(
            "The hospital section turns into a zombie holdout as Carlos protects Jill. This edit keeps "
            "the defense, the vaccine moment, and Jill waking up, without long inventory loops."
        ),
        tags=f"{BASE_TAGS}, hospital holdout, hospital defense, carlos protects jill, zombie horde",
        pinned_comment="Hospital defense was tense. Did Carlos carry this section?",
        thumbnail_text=("HOSPITAL", "HOLDOUT"),
        thumbnail_timestamp="00:05:00.000",
        upload_order=16,
        clips=(
            LongClip("HOSPITAL DEFENSE", "03:33:45.000", "03:45:10.000", "gameplay", True),
            LongClip("JILL WAKES UP", "03:45:10.000", "03:49:15.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_09_nest_lab",
        filename="re3_part_09_nest_lab.mp4",
        title="Resident Evil 3 Remake: NEST Lab Run | No Commentary Part 9",
        description=(
            "Jill reaches the final lab stretch. This part keeps the NEST buildup and route "
            "pressure before the last Nemesis fight."
        ),
        tags=f"{BASE_TAGS}, nest lab, final lab, re3 nest, jill valentine final mission",
        pinned_comment="Did the NEST lab section feel too short, or just enough?",
        thumbnail_text=("NEST", "LAB RUN"),
        thumbnail_timestamp="00:08:00.000",
        upload_order=17,
        clips=(
            LongClip("NEST LAB RUN", "04:14:45.000", "04:30:30.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_10_final_nemesis",
        filename="re3_part_10_final_nemesis.mp4",
        title="Resident Evil 3 Remake: Final Nemesis And Railgun | Part 10",
        description=(
            "The final Nemesis fight begins and Jill uses the railgun to end the monster for good. "
            "The boss fight and railgun payoff stay together without chopping the scene flow."
        ),
        tags=f"{BASE_TAGS}, final nemesis, railgun nemesis, re3 final boss, jill vs nemesis",
        pinned_comment="Was the railgun finish hype or too over the top?",
        thumbnail_text=("FINAL", "NEMESIS"),
        thumbnail_timestamp="00:11:00.000",
        upload_order=18,
        clips=(
            LongClip("FINAL NEMESIS", "04:35:00.000", "04:51:30.000", "dialogue", True),
        ),
    ),
    LongPart(
        slug="re3_part_11_ending_escape",
        filename="re3_part_11_ending_escape.mp4",
        title="Resident Evil 3 Remake Ending: Jill Escapes Raccoon City | Part 11",
        description=(
            "The RE3 Remake finale closes with Jill, Nicolai, the helicopter escape, and the final "
            "ending beat after Raccoon City falls."
        ),
        tags=f"{BASE_TAGS}, re3 ending, resident evil 3 ending, jill escapes, nicolai scene",
        pinned_comment="Did RE3 Remake's ending give Jill the sendoff she deserved?",
        thumbnail_text=("RACCOON CITY", "ENDING"),
        thumbnail_timestamp="00:03:30.000",
        upload_order=19,
        clips=(
            LongClip("ENDING ESCAPE", "04:51:30.000", "04:58:18.000", "dialogue", True),
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


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


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
        "Style: Hook,Arial Black,70,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,54,54,180,1",
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
            r"{\fad(120,220)}RE3 REMAKE NO COMMENTARY"
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
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.08:saturation=0.9[bg2];"
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
        "[0:a]aresample=48000,volume=1.08,alimiter=limit=0.96,"
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


def make_title_card(ffmpeg: str, label: str, out_path: Path, duration: float = LONG_CARD_DURATION) -> None:
    text = label.replace(":", " - ").replace("'", "")
    draw = (
        "drawbox=x=0:y=0:w=1280:h=720:color=0x070909@1:t=fill,"
        "drawgrid=w=80:h=80:t=1:c=0xffffff@0.035,"
        "drawtext=text='MRLLUMINATI GAMING':x=(w-text_w)/2:y=245:fontsize=28:fontcolor=white,"
        f"drawtext=text='{text}':x=(w-text_w)/2:y=320:fontsize=56:fontcolor=white,"
        "drawtext=text='RESIDENT EVIL 3 NO COMMENTARY':x=(w-text_w)/2:y=405:fontsize=30:fontcolor=0xdddddd,"
        "fps=30,setsar=1,format=yuv420p"
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
            draw,
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
    fade = min(0.18, max(0.05, duration / 4))
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
    items: list[Path] = []
    for index, clip in enumerate(part.clips, start=1):
        if clip.card:
            card_path = part_work_dir / f"{index:02d}_card.mp4"
            make_title_card(ffmpeg, clip.label, card_path)
            items.append(card_path)
        clip_path = part_work_dir / f"{index:02d}_{clip.clip_type}.mp4"
        render_long_clip(ffmpeg, source, clip, clip_path)
        items.append(clip_path)

    concat_path = part_work_dir / "concat.txt"
    concat_path.write_text("\n".join(f"file '{item.as_posix()}'" for item in items) + "\n", encoding="utf-8")
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


def clean_outputs() -> None:
    desired_long = {part.filename for part in LONG_PARTS}
    desired_shorts = {f"{short.slug}.mp4" for short in SHORTS}
    desired_thumbs = {f"{part.slug}_thumbnail.jpg" for part in LONG_PARTS}
    for path in SHORT_DIR.glob("*.mp4"):
        if path.name not in desired_shorts:
            path.unlink()
    for path in LONG_DIR.glob("*.mp4"):
        if path.name not in desired_long:
            path.unlink()
    for path in THUMB_DIR.glob("*.jpg"):
        if path.name not in desired_thumbs:
            path.unlink()
    desired_slugs = {part.slug for part in LONG_PARTS} | {short.slug for short in SHORTS}
    for path in REVIEW_DIR.glob("*"):
        if path.name.startswith("overview_") or path.name.startswith("candidate_"):
            continue
        matching = next((slug for slug in desired_slugs if path.name.startswith(slug)), None)
        if matching is None:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


def render_long_form(ffmpeg: str, source: Path) -> list[Path]:
    return [render_long_part(ffmpeg, source, part) for part in LONG_PARTS]


def drawtext_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace(":", r"\:").replace("'", "").replace("%", r"\%")


def font_path(name: str) -> str:
    return f"C\\:/Windows/Fonts/{name}"


def drawtext(text: str, x: int, y: int, size: int, color: str, font: str = "impact.ttf", border: int = 4) -> str:
    return (
        f"drawtext=fontfile='{font_path(font)}':"
        f"text='{drawtext_escape(text)}':"
        f"x={x}:y={y}:fontsize={size}:fontcolor={color}:"
        f"borderw={border}:bordercolor=black@0.92"
    )


def render_thumbnail(ffmpeg: str, video_path: Path, part: LongPart) -> Path:
    out_path = THUMB_DIR / f"{part.slug}_thumbnail.jpg"
    line1, line2 = part.thumbnail_text
    part_number = str(part.upload_order - 8)
    filters = [
        "scale=1280:720:force_original_aspect_ratio=increase",
        "crop=1280:720",
        "setsar=1",
        "eq=contrast=1.15:brightness=-0.035:saturation=1.22",
        "unsharp=5:5:0.72",
        "drawbox=x=0:y=0:w=1280:h=720:color=black@0.10:t=fill",
        "drawbox=x=0:y=0:w=590:h=720:color=black@0.66:t=fill",
        "drawbox=x=42:y=38:w=255:h=56:color=0xB00000@0.98:t=fill",
        "drawbox=x=42:y=111:w=470:h=8:color=0xF4C430@0.98:t=fill",
        drawtext("RE3 REMAKE", 62, 49, 34, "white", "arialbd.ttf", 2),
        "drawbox=x=1082:y=42:w=152:h=58:color=black@0.68:t=fill",
        drawtext(f"PART {part_number}", 1100, 54, 34, "0xF4C430", "arialbd.ttf", 2),
        drawtext(line1, 48, 225, 76, "white", "impact.ttf", 5),
        drawtext(line2, 48, 330, 96, "0xF4C430", "impact.ttf", 5),
        "drawbox=x=46:y=478:w=470:h=62:color=0xB00000@0.94:t=fill",
        drawtext("NO COMMENTARY CUT", 66, 491, 31, "white", "arialbd.ttf", 2),
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


def render_thumbnails(ffmpeg: str, long_paths: list[Path]) -> None:
    paths_by_name = {path.name: path for path in long_paths}
    for part in LONG_PARTS:
        long_path = paths_by_name.get(part.filename, LONG_DIR / part.filename)
        if long_path.exists():
            render_thumbnail(ffmpeg, long_path, part)


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
        draw = (
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
                draw,
                "-q:v",
                "3",
                str(frame),
            ]
        )
    cols, rows = 4, 4
    page_size = cols * rows
    pages = (len(timestamps) + page_size - 1) // page_size
    for page in range(pages):
        start = page * page_size
        count = min(page_size, len(timestamps) - start)
        page_dir = frames_dir / f"page_{page + 1:02d}"
        page_dir.mkdir(parents=True, exist_ok=True)
        for old in page_dir.glob("frame_*.jpg"):
            old.unlink()
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
                "description": f"{short.description} {SHORT_DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail": "",
                "chapters": "",
            }
        )
    long_paths_by_name = {path.name: path for path in long_paths}
    for part in LONG_PARTS:
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
                "thumbnail": f"{part.slug}_thumbnail.jpg",
                "chapters": " | ".join(long_part_chapters(part)),
            }
        )

    csv_path = META_DIR / "re3_remake_no_commentary_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# Resident Evil 3 Remake Upload Pack", "", "## Outputs"]
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
    (META_DIR / "re3_remake_no_commentary_metadata.md").write_text("\n".join(md_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RE3 Remake Shorts and long-form outputs.")
    parser.add_argument("--source", required=True, help="Local gameplay MP4")
    parser.add_argument("--skip-shorts", action="store_true", help="Do not render Shorts")
    parser.add_argument("--skip-long", action="store_true", help="Do not render long-form parts")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Do not render long-form thumbnails")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    clean_outputs()

    short_paths: dict[str, Path] = {short.slug: SHORT_DIR / f"{short.slug}.mp4" for short in SHORTS}
    if not args.skip_shorts:
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
