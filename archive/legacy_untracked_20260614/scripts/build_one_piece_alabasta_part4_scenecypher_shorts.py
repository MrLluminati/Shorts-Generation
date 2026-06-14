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


PROJECT = "One Piece Alabasta Part 4"
OUTPUT_ROOT = ROOT / "movies" / PROJECT
SHORT_DIR = OUTPUT_ROOT / "shorts"
META_DIR = OUTPUT_ROOT / "metadata"
WORK_DIR = OUTPUT_ROOT / "work"
REVIEW_DIR = OUTPUT_ROOT / "review"
ASS_DIR = WORK_DIR / "ass"

DEFAULT_SOURCE = Path(
    r"D:\movies\One Piece\0093-00130 Alabasta Arc (second major arc)\0120-0130 Alabasta Arc Part 4, Dub.mp4"
)

BASE_HASHTAGS = (
    "#onepiece #onepieceanime #alabasta #alabastaarc #luffy #crocodile "
    "#vivi #strawhats #animeexplained #animeedit #sceneexplained "
    "#scenecypherhq #shorts"
)
BASE_TAGS = (
    "one piece, one piece alabasta, alabasta arc, luffy vs crocodile, "
    "crocodile one piece, princess vivi, straw hats, anime explained, "
    "one piece explained, one piece shorts, anime shorts, scene explained, "
    "scenecypher hq"
)
DESCRIPTION_SUFFIX = (
    "SceneCypher HQ decodes anime, movie, and series moments through hidden details, "
    "scene logic, and character choices."
)


@dataclass(frozen=True)
class AlabastaShort:
    slug: str
    start: str
    duration: float
    hook: str
    beats: tuple[str, ...]
    title: str
    description_lead: str
    tags: str
    pinned_comment: str
    thumbnail_text: str
    upload_order: int


SHORTS = (
    AlabastaShort(
        slug="01_luffy_still_stands",
        start="00:45:00.000",
        duration=28.5,
        hook="LUFFY STILL\nSTANDS",
        beats=("CROCODILE EXPECTS\nFEAR", "LUFFY ANSWERS\nWITH WILL"),
        title="Luffy Still Standing Changed The Fight | One Piece Alabasta #shorts",
        description_lead="This Alabasta moment works because Luffy's body is almost done, but his choice still refuses Crocodile's control.",
        tags=f"{BASE_TAGS}, luffy still standing, luffy alabasta, luffy willpower",
        pinned_comment="Was this the moment Crocodile started losing control?",
        thumbnail_text="LUFFY STANDS",
        upload_order=1,
    ),
    AlabastaShort(
        slug="02_crocodile_trusted_the_pressure",
        start="00:54:58.000",
        duration=28.5,
        hook="CROCODILE KNEW\nTHE CLOCK WAS WINNING",
        beats=("HE DOESN'T\nNEED TO RUSH", "THE PRESSURE\nIS HIS WEAPON"),
        title="Crocodile Trusted The Pressure | One Piece Explained #shorts",
        description_lead="Crocodile feels dangerous here because he lets the timer do half the fighting for him.",
        tags=f"{BASE_TAGS}, crocodile villain, crocodile alabasta, one piece villain explained",
        pinned_comment="Crocodile's scariest weapon here: power or patience?",
        thumbnail_text="CROCODILE'S CLOCK",
        upload_order=3,
    ),
    AlabastaShort(
        slug="03_clock_made_every_second_hurt",
        start="01:17:00.000",
        duration=29.0,
        hook="THE CLOCK MADE\nEVERY SECOND HURT",
        beats=("ALABASTA'S WAR\nBECOMES A TIMER", "ONE DELAY\nMEANS EVERYONE LOSES"),
        title="The Clock Made Alabasta Hurt | One Piece #shorts",
        description_lead="The bomb clock turns the arc from a fight into a deadline, which is why every reaction suddenly feels heavier.",
        tags=f"{BASE_TAGS}, alabasta bomb, one piece clock tower, alabasta countdown",
        pinned_comment="Did the countdown make this arc more stressful?",
        thumbnail_text="EVERY SECOND HURTS",
        upload_order=4,
    ),
    AlabastaShort(
        slug="04_four_seconds_changed_the_arc",
        start="01:40:28.000",
        duration=29.0,
        hook="FOUR SECONDS\nCHANGED THE ARC",
        beats=("THE BOMB IS\nNOT JUST ACTION", "IT FORCES\nEVERY CHOICE"),
        title="Four Seconds Changed Alabasta | One Piece #shorts",
        description_lead="The countdown works because it compresses the entire kingdom's fear into one tiny window.",
        tags=f"{BASE_TAGS}, four seconds one piece, alabasta bomb scene, one piece countdown",
        pinned_comment="Best countdown moment in One Piece?",
        thumbnail_text="4 SECONDS",
        upload_order=5,
    ),
    AlabastaShort(
        slug="05_vivi_saw_the_war_continue",
        start="02:03:28.000",
        duration=29.0,
        hook="VIVI SAW\nTHE WAR CONTINUE",
        beats=("WINNING THE FIGHT\nWASN'T ENOUGH", "SHE NEEDED\nTHE PEOPLE TO HEAR"),
        title="Vivi Saw The War Continue | One Piece Alabasta #shorts",
        description_lead="Vivi's pain lands because the villain can lose and the war can still keep moving without her voice reaching anyone.",
        tags=f"{BASE_TAGS}, vivi alabasta, princess vivi, alabasta war, one piece emotional scene",
        pinned_comment="Was Vivi the emotional center of Alabasta?",
        thumbnail_text="VIVI'S WAR",
        upload_order=2,
    ),
    AlabastaShort(
        slug="06_rain_finally_answered",
        start="02:05:00.000",
        duration=29.0,
        hook="THE RAIN\nFINALLY ANSWERED",
        beats=("ALABASTA NEEDED\nPROOF", "THE SKY BECOMES\nTHE PAYOFF"),
        title="The Rain Finally Answered | One Piece Alabasta #shorts",
        description_lead="The rain is not just weather. It is the kingdom finally seeing that Crocodile's lie has broken.",
        tags=f"{BASE_TAGS}, alabasta rain, one piece rain scene, crocodile defeated",
        pinned_comment="Did the rain hit harder than the final punch?",
        thumbnail_text="RAIN ANSWERED",
        upload_order=6,
    ),
    AlabastaShort(
        slug="07_silent_goodbye",
        start="03:05:36.000",
        duration=28.5,
        hook="THE GOODBYE\nSTAYED SILENT",
        beats=("NO SPEECH\nNEEDED", "THE MARKS CARRY\nTHE ANSWER"),
        title="The Silent Goodbye Still Hurts | One Piece Alabasta #shorts",
        description_lead="The farewell works because the Straw Hats choose silence, and that makes the answer feel even louder.",
        tags=f"{BASE_TAGS}, alabasta goodbye, straw hats goodbye, vivi goodbye, one piece farewell",
        pinned_comment="Is this still one of the best Straw Hat goodbyes?",
        thumbnail_text="SILENT GOODBYE",
        upload_order=7,
    ),
    AlabastaShort(
        slug="08_robin_changes_the_ship",
        start="03:20:20.000",
        duration=28.5,
        hook="ROBIN CHANGED\nTHE SHIP'S FUTURE",
        beats=("THE ARC ENDS\nWITH A QUESTION", "TRUST STARTS\nAS A RISK"),
        title="Robin Changed The Crew's Future | One Piece #shorts",
        description_lead="Robin's arrival works as a quiet twist: the war ends, but the next mystery is already sitting on the ship.",
        tags=f"{BASE_TAGS}, nico robin joins, robin straw hats, robin alabasta, one piece crew",
        pinned_comment="Did you trust Robin the first time she appeared on the ship?",
        thumbnail_text="ROBIN'S RISK",
        upload_order=8,
    ),
)


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def parse_timecode(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_ass(short: AlabastaShort) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    beat_1 = short.beats[0] if short.beats else ""
    beat_2 = short.beats[1] if len(short.beats) > 1 else ""
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
        "Style: Logo,Arial,26,&H00FFFFFF,&H000000FF,&H99000000,&H99000000,-1,0,0,0,100,100,2,0,1,2,0,8,40,40,34,1",
        "Style: Hook,Arial Black,62,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,58,58,178,1",
        "Style: Beat,Arial Black,43,&H00FFFFFF,&H000000FF,&H00111111,&H99000000,-1,0,0,0,100,100,0,0,1,4,1,5,82,82,0,1",
        "Style: Lower,Arial Black,31,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,1,2,70,70,186,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 8,{ass_time(0)},{ass_time(short.duration)},Logo,,0,0,0,,SCENECYPHER HQ",
        (
            f"Dialogue: 10,{ass_time(0.18)},{ass_time(3.70)},Hook,,0,0,0,,"
            r"{\fad(80,220)\t(0,280,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
    ]
    if beat_1:
        lines.append(
            f"Dialogue: 9,{ass_time(8.0)},{ass_time(12.8)},Beat,,0,0,0,,"
            r"{\fad(100,180)}" + ass_escape(beat_1)
        )
    if beat_2:
        lines.append(
            f"Dialogue: 9,{ass_time(17.0)},{ass_time(22.2)},Beat,,0,0,0,,"
            r"{\fad(100,180)}" + ass_escape(beat_2)
        )
    lines.append(
        f"Dialogue: 7,{ass_time(max(0, short.duration - 4.2))},{ass_time(max(0, short.duration - 0.55))},Lower,,0,0,0,,"
        r"{\fad(120,220)}ONE PIECE / ALABASTA DECODED"
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, source: Path, short: AlabastaShort) -> Path:
    ass_path = write_ass(short)
    out_path = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.35)
    video_filter = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.04:saturation=0.92[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1,"
        "eq=contrast=1.05:saturation=1.08,unsharp=5:5:0.35[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=0:w=1080:h=1920:color=black@0.08:t=fill,"
        f"fade=t=in:st=0:d=0.14,fade=t=out:st={fade_out:.3f}:d=0.35,"
        f"{subtitle_filter_arg(ass_path)},format=yuv420p"
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
            video_filter,
            "-af",
            "aresample=48000,volume=1.03,alimiter=limit=0.96,"
            f"afade=t=in:st=0:d=0.12,afade=t=out:st={fade_out:.3f}:d=0.35",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-r",
            "30000/1001",
            "-pix_fmt",
            "yuv420p",
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


def review_contact(ffmpeg: str, video_path: Path, short: AlabastaShort) -> None:
    frame_dir = REVIEW_DIR / f"{short.slug}_frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    stamps = [0.8, short.duration * 0.33, short.duration * 0.66, max(0.5, short.duration - 1.0)]
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
                "-vf",
                "scale=270:480",
                "-q:v",
                "3",
                str(frame_dir / f"frame_{index:03d}.jpg"),
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
            str(frame_dir / "frame_%03d.jpg"),
            "-vf",
            "tile=4x1",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(REVIEW_DIR / f"{short.slug}_contact.jpg"),
        ]
    )


def write_metadata(paths: dict[str, Path]) -> None:
    rows = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        rows.append(
            {
                "upload_order": short.upload_order,
                "slug": short.slug,
                "file": paths[short.slug].name,
                "source_start": short.start,
                "duration": f"{short.duration:.1f}",
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )
    csv_path = META_DIR / "one_piece_alabasta_part4_scenecypher_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# One Piece Alabasta Part 4 SceneCypher Shorts", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
                f"- Source start: {row['source_start']}",
                f"- Duration: {row['duration']}s",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                f"- Thumbnail text: {row['thumbnail_text']}",
                "",
            ]
        )
    (META_DIR / "one_piece_alabasta_part4_scenecypher_metadata.md").write_text(
        "\n".join(md_lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SceneCypher HQ One Piece Alabasta Shorts.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local One Piece source MP4")
    parser.add_argument("--only", nargs="*", default=None, help="Optional slug list to render")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise FileNotFoundError(source)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    selected = [short for short in SHORTS if args.only is None or short.slug in args.only]
    paths = {short.slug: SHORT_DIR / f"{short.slug}.mp4" for short in SHORTS}
    for short in selected:
        print(f"Rendering {short.slug}")
        path = render_short(ffmpeg, source, short)
        paths[short.slug] = path
        review_contact(ffmpeg, path, short)
    write_metadata(paths)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
