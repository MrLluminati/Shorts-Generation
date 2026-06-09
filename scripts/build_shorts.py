from __future__ import annotations

import html
import re
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


SOURCE = Path(
    r"D:\movies\Chainsaw Man The Movie Reze Arc 2025 1080p AMZN WEBRip DUAL AAC5.1 x265-Jadoo.mkv"
)
SRT = ROOT / "work" / "movie_sdh.srt"
SUBTITLE_DIR = ROOT / "work" / "subtitles"
OUTPUT_DIR = ROOT / "outputs"


@dataclass(frozen=True)
class Short:
    slug: str
    title: str
    start: str
    duration: float
    hook: str
    upload_title: str
    description: str
    hashtags: str


SHORTS = [
    Short(
        slug="01_date_to_devil",
        title="Date to Devil",
        start="00:48:45.000",
        duration=50,
        hook="SHE WENT FROM\nDATE TO DEVIL",
        upload_title="Reze's Smile Was the Warning | Chainsaw Man Reze Arc",
        description=(
            "The calmest betrayal is always the loudest. "
            "Reze flips the whole scene in seconds."
        ),
        hashtags="#chainsawman #reze #animeedit #shorts",
    ),
    Short(
        slug="02_bomb_walked_in",
        title="Bomb Walked In",
        start="00:54:08.000",
        duration=59,
        hook="THE BOMB DEVIL\nWALKED IN SMILING",
        upload_title="Bomb Devil Walked In Smiling | Chainsaw Man",
        description=(
            "Everyone realizes too late who just entered the room. "
            "A quiet entrance, then instant panic."
        ),
        hashtags="#chainsawman #bombdevil #anime #shorts",
    ),
    Short(
        slug="03_denji_heart",
        title="Denji's Heart",
        start="01:02:11.000",
        duration=46,
        hook="DENJI FINALLY\nSAID IT",
        upload_title="Does Anyone Want Denji's Heart? | Chainsaw Man",
        description=(
            "Denji turns a fight into the funniest and saddest confession "
            "in the middle of chaos."
        ),
        hashtags="#denji #chainsawman #animefunny #shorts",
    ),
    Short(
        slug="04_easy_choice",
        title="Easy Choice",
        start="01:08:24.000",
        duration=31,
        hook="KILL HER...\nOR LET HER KILL YOU",
        upload_title="Chainsaw Man Had One Choice | Reze Arc",
        description=(
            "Angel gives Chainsaw Man the brutal choice, and Denji answers "
            "without hesitation."
        ),
        hashtags="#chainsawman #reze #animefight #shorts",
    ),
    Short(
        slug="05_run_away_together",
        title="Run Away Together",
        start="01:25:29.000",
        duration=59,
        hook="HE STILL ASKED HER\nTO RUN AWAY",
        upload_title="He Still Asked Reze to Run Away | Chainsaw Man",
        description=(
            "After everything, Denji still chooses the impossible soft answer."
        ),
        hashtags="#chainsawman #denji #reze #animeedit #shorts",
    ),
    Short(
        slug="06_city_mouse",
        title="City Mouse",
        start="00:34:07.500",
        duration=59.5,
        hook="CITY MOUSE\nOR COUNTRY MOUSE?",
        upload_title="The City Mouse Question | Chainsaw Man Reze Arc",
        description=(
            "The sweetest scene hides the whole tragedy in one little fable."
        ),
        hashtags="#chainsawman #reze #denji #anime #shorts",
    ),
]


def ts_to_seconds(value: str) -> float:
    hms, _, millis = value.partition(".")
    hours, minutes, seconds = [int(part) for part in hms.split(":")]
    return hours * 3600 + minutes * 60 + seconds + int((millis or "0").ljust(3, "0")[:3]) / 1000


def seconds_to_ass(seconds: float) -> str:
    seconds = max(0, seconds)
    hours = int(seconds // 3600)
    minutes = int(seconds % 3600 // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis == 100:
        secs += 1
        centis = 0
    return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"


def parse_srt(path: Path) -> list[tuple[float, float, str]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    entries: list[tuple[float, float, str]] = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        match = re.search(
            r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})",
            block,
        )
        if not match:
            continue
        lines = block.strip().splitlines()[2:]
        text = " ".join(lines)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\{\\an\d+\}", "", text)
        text = html.unescape(text).strip()
        entries.append(
            (
                srt_time_to_seconds(match.group(1)),
                srt_time_to_seconds(match.group(2)),
                clean_caption(text),
            )
        )
    return entries


def srt_time_to_seconds(value: str) -> float:
    hours, minutes, rest = value.split(":")
    seconds, millis = rest.split(",")
    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
        + int(millis) / 1000
    )


def clean_caption(text: str) -> str:
    text = re.sub(r"\[(Denji|Reze|Aki|Angel|Beam|Nomo|Kato|Makima|Typhoon|Power|Pochita)\]\s*", "", text)
    text = re.sub(r"\[[^\]]+\]\s*", "", text)
    text = re.sub(r"^\s*-\s*", "", text)
    text = text.replace(" - ", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ass_escape(text: str) -> str:
    text = text.replace("{", "").replace("}", "")
    return text.replace("\n", r"\N")


def wrap_ass(text: str, width: int) -> str:
    lines: list[str] = []
    for paragraph in text.splitlines():
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])
    return r"\N".join(lines[:3])


def make_ass(short: Short, entries: list[tuple[float, float, str]]) -> Path:
    SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)
    start = ts_to_seconds(short.start)
    end = start + short.duration
    ass_path = SUBTITLE_DIR / f"{short.slug}.ass"
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Arial,82,&H00FFFFFF,&H000000FF,&H00141414,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,110,1
Style: Caption,Arial,58,&H00FFFFFF,&H000000FF,&H00141414,&HAA000000,-1,0,0,0,100,100,0,0,1,5,1,2,70,70,245,1
Style: Tag,Arial,38,&H00EDEDED,&H000000FF,&H00141414,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,8,60,60,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [
        f"Dialogue: 2,{seconds_to_ass(0)},{seconds_to_ass(min(4.2, short.duration))},Hook,,0,0,0,,{{\\fad(80,220)}}{ass_escape(short.hook)}",
        f"Dialogue: 1,{seconds_to_ass(0)},{seconds_to_ass(short.duration)},Tag,,0,0,0,,{ass_escape(short.title.upper())}",
    ]
    for cue_start, cue_end, text in entries:
        if not text or cue_end <= start or cue_start >= end:
            continue
        local_start = max(0, cue_start - start)
        local_end = min(short.duration, cue_end - start)
        if local_end - local_start < 0.25:
            continue
        wrapped = wrap_ass(text, 28)
        events.append(
            f"Dialogue: 3,{seconds_to_ass(local_start)},{seconds_to_ass(local_end)},Caption,,0,0,0,,{ass_escape(wrapped)}"
        )
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")
    return ass_path


def render_short(short: Short, ass_path: Path) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{short.slug}.mp4"
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    ass_filter = f"subtitles={ass_path.relative_to(ROOT).as_posix()}"
    fade_out_start = max(0.0, short.duration - 0.35)
    vf = ",".join(
        [
            "crop=450:800:(iw-450)/2:0",
            "scale=1080:1920:flags=lanczos",
            "setsar=1",
            "eq=contrast=1.05:saturation=1.10",
            "unsharp=5:5:0.45:5:5:0.0",
            ass_filter,
            "fade=t=in:st=0:d=0.18",
            f"fade=t=out:st={fade_out_start:.3f}:d=0.35",
        ]
    )
    af = ",".join(
        [
            "afade=t=in:st=0:d=0.10",
            f"afade=t=out:st={fade_out_start:.3f}:d=0.35",
        ]
    )
    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-ss",
        short.start,
        "-t",
        str(short.duration),
        "-i",
        str(SOURCE),
        "-map",
        "0:0",
        "-map",
        "0:2",
        "-vf",
        vf,
        "-af",
        af,
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-ac",
        "2",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    return out_path


def write_metadata(paths: list[Path]) -> None:
    rows = ["# Shorts Pack", ""]
    rows.append(
        "All files are vertical 1080x1920 MP4 drafts with English audio, burned captions, and top-screen hooks."
    )
    rows.append("")
    for short, path in zip(SHORTS, paths, strict=True):
        rows.extend(
            [
                f"## {short.title}",
                f"- File: `{path.name}`",
                f"- Source timestamp: `{short.start}` for `{int(short.duration)}s`",
                f"- Upload title: {short.upload_title}",
                f"- Description: {short.description}",
                f"- Hashtags: {short.hashtags}",
                "",
            ]
        )
    (OUTPUT_DIR / "shorts_metadata.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not SRT.exists():
        raise FileNotFoundError(SRT)
    entries = parse_srt(SRT)
    rendered: list[Path] = []
    for short in SHORTS:
        ass = make_ass(short, entries)
        rendered.append(render_short(short, ass))
    write_metadata(rendered)
    print("Rendered:")
    for path in rendered:
        print(path)


if __name__ == "__main__":
    main()
