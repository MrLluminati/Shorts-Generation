from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


SOURCE = Path(
    r"D:\movies\Chainsaw Man The Movie Reze Arc 2025 1080p AMZN WEBRip DUAL AAC5.1 x265-Jadoo.mkv"
)
MOVIE_DIR = ROOT / "movies" / "Chainsaw Man Reze Arc"
SHORTS_DIR = MOVIE_DIR / "shorts"
METADATA_DIR = MOVIE_DIR / "metadata"
SUBTITLE_DIR = MOVIE_DIR / "work" / "subtitles"
SEGMENT_DIR = MOVIE_DIR / "work" / "viral_segments"

SLUG = "08_they_never_wanted_denji"
OUTPUT = SHORTS_DIR / f"{SLUG}.mp4"
ASS_PATH = SUBTITLE_DIR / f"{SLUG}.ass"
METADATA_PATH = METADATA_DIR / f"{SLUG}.md"

SEGMENTS = [
    ("00:25:56.702", "00:26:01.290"),
    ("00:26:21.560", "00:26:26.523"),
    ("01:02:28.391", "01:02:32.145"),
    ("01:02:32.228", "01:02:36.316"),
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


def ass_escape(text: str) -> str:
    return text.replace("\n", r"\N")


def write_ass() -> None:
    SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Arial,88,&H00FFFFFF,&H000000FF,&H00141414,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,115,1
Style: Punch,Arial,66,&H00FFFFFF,&H000000FF,&H00141414,&HAA000000,-1,0,0,0,100,100,0,0,1,5,1,8,70,70,255,1
Style: Caption,Arial,60,&H00FFFFFF,&H000000FF,&H00141414,&HAA000000,-1,0,0,0,100,100,0,0,1,5,1,2,70,70,245,1
Style: Tag,Arial,38,&H00EDEDED,&H000000FF,&H00141414,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,8,60,60,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [
        ("2", 0.00, 3.20, "Hook", r"{\fad(80,180)}THEY NEVER\NWANTED DENJI"),
        ("2", 3.25, 5.75, "Punch", r"{\fad(80,160)}ONLY HIS POWER"),
        ("2", 9.70, 12.35, "Punch", r"{\fad(80,160)}DENJI SAYS IT OUT LOUD"),
        ("1", 0.00, 17.39, "Tag", "DENJI WAS NOT THE PRIZE"),
        ("3", 0.15, 4.35, "Caption", "Why do you devils want\nChainsaw's heart?"),
        ("3", 4.80, 9.05, "Caption", "Once I get my hands\non Chainsaw's heart..."),
        ("3", 9.85, 13.35, "Caption", "Everyone always wants\nChainsaw's heart!"),
        ("3", 13.45, 17.10, "Caption", "Doesn't anyone want\nDenji's heart?"),
    ]
    lines = [
        f"Dialogue: {layer},{seconds_to_ass(start)},{seconds_to_ass(end)},{style},,0,0,0,,{ass_escape(text)}"
        for layer, start, end, style, text in events
    ]
    ASS_PATH.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def render() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SEGMENT_DIR.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    segment_paths: list[Path] = []
    vf = ",".join(
        [
            "crop=450:800:(iw-450)/2:0",
            "scale=1080:1920:flags=lanczos",
            "setsar=1",
            "eq=contrast=1.08:saturation=1.12",
            "unsharp=5:5:0.48:5:5:0.0",
        ]
    )

    for index, (start, end) in enumerate(SEGMENTS):
        start_sec = ts_to_seconds(start)
        end_sec = ts_to_seconds(end)
        duration = end_sec - start_sec
        segment_path = SEGMENT_DIR / f"{SLUG}_{index + 1:02}.mp4"
        segment_paths.append(segment_path)
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-ss",
                start,
                "-t",
                f"{duration:.3f}",
                "-i",
                str(SOURCE),
                "-map",
                "0:0",
                "-map",
                "0:2",
                "-vf",
                vf,
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
                str(segment_path),
            ],
            cwd=ROOT,
            check=True,
        )

    concat_list = SEGMENT_DIR / f"{SLUG}_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{path.as_posix()}'" for path in segment_paths) + "\n",
        encoding="utf-8",
    )
    ass_filter = f"subtitles={ASS_PATH.relative_to(ROOT).as_posix()}"

    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-vf",
        ass_filter,
        "-map",
        "0:v",
        "-map",
        "0:a",
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
        str(OUTPUT),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def write_metadata() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    metadata = "\n".join(
        [
            "# Viral Test Upload",
            "",
            f"- File: `{OUTPUT.name}`",
            "- Source movie: `Chainsaw Man The Movie Reze Arc`",
            "- Runtime target: `17.39s`",
            "- Upload title: They Never Wanted Denji | Chainsaw Man #shorts",
            "- Description: Everyone keeps chasing Chainsaw's heart, but Denji says the quiet part out loud. This Reze Arc moment explains why the joke actually hurts. SceneCipher HQ decodes anime, movie, and series moments through silent explainers, hidden details, and scene logic.",
            "- Hashtags: #chainsawman #denji #reze #pochita #chainsawmanmovie #rezearc #animeexplained #animeedit #animeedits #sceneexplained #movieexplained #scenecipher #shorts",
            "- Tags: chainsaw man, denji, reze, chainsaw man reze arc, chainsaw man movie, pochita, chainsaw heart, denji heart, they never wanted denji, everyone wants chainsaw heart, anime explained, anime shorts, scene decoded, mappa anime, scenecipher hq",
            "- Pinned comment: Did Denji mean it as a joke, or was that the saddest line?",
            "- Thumbnail text: THEY NEVER WANTED DENJI",
            "- First 2 seconds hook: THEY NEVER WANTED DENJI",
            "- Upload action: Publish as a fresh public Short. Do not upload alongside another Chainsaw Short in the same hour.",
            "",
        ]
    )
    METADATA_PATH.write_text(metadata, encoding="utf-8")


def main() -> None:
    write_ass()
    render()
    write_metadata()
    print(OUTPUT)
    print(METADATA_PATH)


if __name__ == "__main__":
    main()
