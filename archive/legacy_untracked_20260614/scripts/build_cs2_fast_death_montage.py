from __future__ import annotations

import csv
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\abhik\Documents\Short Creation")
SOURCE = Path(r"C:\Users\abhik\Videos\2026-06-11_19-23-39.mp4")
FFMPEG = Path(r"C:\Users\abhik\AppData\Local\CapCut\Apps\7.6.0.3123\ffmpeg.exe")

RUN_NAME = "cs2_death_montage_20260613"
OUT_DIR = ROOT / "live_video_pipeline" / "short_form" / RUN_NAME
WORK_DIR = ROOT / "live_video_pipeline" / "work" / RUN_NAME
REVIEW_DIR = ROOT / "live_video_pipeline" / "review" / RUN_NAME
META_DIR = ROOT / "live_video_pipeline" / "metadata" / RUN_NAME

OUTPUT = OUT_DIR / "cs2_fast_death_montage_mrlluminati.mp4"
THUMBNAIL = OUT_DIR / "cs2_fast_death_montage_thumbnail.jpg"
CSV_PATH = META_DIR / "cs2_fast_death_montage_metadata.csv"
MD_PATH = META_DIR / "cs2_fast_death_montage_metadata.md"


@dataclass(frozen=True)
class DeathBeat:
    start: float
    duration: float
    label: str
    overlay: str


BEATS = [
    DeathBeat(47.75, 2.45, "00:47.750", "BAD PEEK"),
    DeathBeat(93.10, 2.55, "01:33.100", "SPRAY PANIC"),
    DeathBeat(294.20, 2.65, "04:54.200", "TOO CLOSE"),
    DeathBeat(589.15, 2.25, "09:49.150", "INSTANT PUNISH"),
    DeathBeat(683.85, 1.95, "11:23.850", "GRENADE PAIN"),
    DeathBeat(729.45, 2.10, "12:09.450", "WRONG ANGLE"),
    DeathBeat(749.20, 2.25, "12:29.200", "NO SPACE"),
    DeathBeat(803.55, 2.10, "13:23.550", "LOW HP PROBLEM"),
    DeathBeat(878.10, 2.75, "14:38.100", "OPEN TARGET"),
    DeathBeat(999.50, 1.95, "16:39.500", "LAST BULLET"),
    DeathBeat(1010.00, 1.85, "16:50.000", "FINAL DEATH"),
]


def run(cmd: list[str | Path]) -> subprocess.CompletedProcess[str]:
    printable = " ".join(str(part) for part in cmd)
    print(printable)
    result = subprocess.run(
        [str(part) for part in cmd],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout)
        result.check_returncode()
    return result


def ensure_dirs() -> None:
    for directory in (OUT_DIR, WORK_DIR, REVIEW_DIR, META_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    stroke_fill: tuple[int, int, int, int] = (0, 0, 0, 230),
    stroke_width: int = 6,
    line_spacing: int = 8,
) -> None:
    x, y = xy
    lines = text.split("\n")
    heights = []
    widths = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=text_font, stroke_width=stroke_width)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    total_h = sum(heights) + line_spacing * (len(lines) - 1)
    cy = y - total_h // 2
    for line, w, h in zip(lines, widths, heights):
        draw.text(
            (x - w // 2, cy),
            line,
            font=text_font,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
        )
        cy += h + line_spacing


def make_overlay(index: int, beat: DeathBeat) -> Path:
    path = WORK_DIR / f"overlay_{index:02d}.png"
    image = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    red = (232, 42, 47, 245)
    white = (255, 255, 255, 255)
    soft_black = (0, 0, 0, 170)
    panel = (0, 0, 0, 150)

    draw.rounded_rectangle((86, 72, 994, 182), radius=34, fill=panel, outline=red, width=3)
    centered_text(draw, (540, 116), "MRLLUMINATI GAMING", font(33), white, stroke_width=3)

    if index == 1:
        centered_text(draw, (540, 282), "I DIED\nTOO FAST", font(92), white, stroke_width=9, line_spacing=4)
    else:
        centered_text(draw, (540, 282), f"DEATH #{index:02d}", font(78), white, stroke_width=8)

    draw.rounded_rectangle((88, 1468, 992, 1612), radius=38, fill=soft_black, outline=red, width=4)
    centered_text(draw, (540, 1530), beat.overlay, font(57), white, stroke_width=6)

    progress_x = 126
    progress_y = 1662
    tick_w = 64
    gap = 13
    for i in range(len(BEATS)):
        color = red if i <= index - 1 else (255, 255, 255, 100)
        draw.rounded_rectangle(
            (progress_x + i * (tick_w + gap), progress_y, progress_x + i * (tick_w + gap) + tick_w, progress_y + 10),
            radius=5,
            fill=color,
        )

    centered_text(draw, (540, 1752), "CS2 DEATH MONTAGE", font(39), white, stroke_width=4)
    image.save(path)
    return path


def make_thumbnail() -> None:
    image = Image.new("RGB", (1080, 1920), (12, 12, 14))
    base_frame = REVIEW_DIR / "frame_hook.jpg"
    if base_frame.exists():
        base = Image.open(base_frame).convert("RGB").resize((1080, 1920))
        blurred = base.filter(ImageFilter.GaussianBlur(18))
        shade = Image.new("RGB", (1080, 1920), (0, 0, 0))
        image = Image.blend(blurred, shade, 0.38)
        focus = base.crop((0, 650, 1080, 1268)).resize((960, 550))
        image.paste(focus, (60, 635))

    draw = ImageDraw.Draw(image)
    red = (232, 42, 47)
    white = (255, 255, 255)
    black = (0, 0, 0)
    draw.rectangle((0, 0, 1080, 360), fill=(0, 0, 0))
    draw.rectangle((0, 1700, 1080, 1920), fill=(0, 0, 0))
    draw.rounded_rectangle((58, 58, 1022, 324), radius=34, fill=(0, 0, 0), outline=red, width=8)
    centered_text(draw, (540, 142), "CS2", font(88), white, stroke_width=6)
    centered_text(draw, (540, 254), "DEATH MONTAGE", font(70), red, stroke_width=5)
    draw.rounded_rectangle((70, 600, 1010, 1220), radius=26, outline=red, width=7)
    draw.rounded_rectangle((92, 1416, 988, 1588), radius=30, fill=red)
    centered_text(draw, (540, 1500), "I DIED TOO FAST", font(74), white, stroke_width=5)
    centered_text(draw, (540, 1778), "MRLLUMINATI GAMING", font(46), white, stroke_width=4)
    image.save(THUMBNAIL, quality=92)


def render_clip(index: int, beat: DeathBeat) -> Path:
    overlay = make_overlay(index, beat)
    out = WORK_DIR / f"clip_{index:02d}.mp4"
    vf = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=24,hue=s=0.72[bgv];"
        "[fg]scale=1080:-2,hue=s=1.08,unsharp=5:5:0.65:3:3:0.25[fgv];"
        "[bgv][fgv]overlay=(W-w)/2:(H-h)/2[base];"
        "[base][1:v]overlay=0:0,format=yuv420p,setsar=1,fps=30[v];"
        "[0:a]aresample=48000,highpass=f=65,acompressor=threshold=-18dB:ratio=2.5:attack=6:release=110,"
        "volume=1.10,alimiter=limit=0.95[a]"
    )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-ss",
            f"{beat.start:.3f}",
            "-t",
            f"{beat.duration:.3f}",
            "-i",
            SOURCE,
            "-loop",
            "1",
            "-t",
            f"{beat.duration:.3f}",
            "-i",
            overlay,
            "-filter_complex",
            vf,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "h264_nvenc",
            "-b:v",
            "10000k",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            "-shortest",
            out,
        ]
    )
    return out


def concat_clips(paths: list[Path]) -> None:
    concat_file = WORK_DIR / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{str(path).replace(chr(39), chr(39) + chr(92) + chr(39) + chr(39))}'" for path in paths),
        encoding="utf-8",
    )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_file,
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            OUTPUT,
        ]
    )


def review_frames() -> None:
    points = {
        "frame_hook.jpg": 0.7,
        "frame_mid.jpg": 11.5,
        "frame_payoff.jpg": 21.0,
        "frame_end.jpg": 24.2,
    }
    for name, second in points.items():
        run(
            [
                FFMPEG,
                "-y",
                "-hide_banner",
                "-ss",
                f"{second:.2f}",
                "-i",
                OUTPUT,
                "-frames:v",
                "1",
                "-q:v",
                "2",
                REVIEW_DIR / name,
            ]
        )

    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-i",
            OUTPUT,
            "-vf",
            "fps=1/3,scale=270:-1,tile=3x3:margin=8:padding=4",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            REVIEW_DIR / "contact_sheet.jpg",
        ]
    )


def verify() -> None:
    run([FFMPEG, "-v", "error", "-i", OUTPUT, "-f", "null", "-"])
    info = run([FFMPEG, "-hide_banner", "-i", OUTPUT, "-t", "0.1", "-f", "null", "-"]).stdout
    (REVIEW_DIR / "ffmpeg_probe.txt").write_text(info, encoding="utf-8")


def write_metadata() -> None:
    title = "I Died Too Fast in CS2 | Funny Death Montage #shorts"
    hashtags = "#cs2 #counterstrike2 #cs2clips #cs2funny #gamingclips #fpsgames #deathmontage #pcgaming #hindigaming #mrlluminati #shorts"
    tags = [
        "cs2",
        "counter strike 2",
        "cs2 death montage",
        "cs2 funny moments",
        "cs2 hindi",
        "cs2 gameplay",
        "counter strike 2 shorts",
        "gaming shorts",
        "fps shorts",
        "death montage",
        "funny gaming clips",
        "pc gaming india",
        "mrlluminati gaming",
    ]
    description = (
        "Fast CS2 death montage from my gameplay. Bad peeks, panic sprays, close-range punishment, "
        "and way too many instant deaths.\n\n"
        "Watch more gameplay clips on MrLluminati Gaming.\n\n"
        f"{hashtags}"
    )
    pinned = "Which death was the most painful: bad peek, close range, or grenade?"

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "filename",
                "title",
                "description",
                "hashtags",
                "tags",
                "pinned_comment",
                "thumbnail",
                "source",
                "source_windows",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "filename": OUTPUT.name,
                "title": title,
                "description": description,
                "hashtags": hashtags,
                "tags": ", ".join(tags),
                "pinned_comment": pinned,
                "thumbnail": THUMBNAIL.name,
                "source": str(SOURCE),
                "source_windows": "; ".join(f"{beat.label} + {beat.duration:.2f}s ({beat.overlay})" for beat in BEATS),
            }
        )

    MD_PATH.write_text(
        "\n".join(
            [
                "# CS2 Fast Death Montage Metadata",
                "",
                f"Output: `{OUTPUT}`",
                f"Thumbnail: `{THUMBNAIL}`",
                "",
                f"Title: {title}",
                "",
                "Description:",
                description,
                "",
                f"Hashtags: {hashtags}",
                "",
                f"Tags: {', '.join(tags)}",
                "",
                f"Pinned comment: {pinned}",
                "",
                "Source windows:",
                *[f"- {beat.label} + {beat.duration:.2f}s - {beat.overlay}" for beat in BEATS],
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not FFMPEG.exists():
        raise FileNotFoundError(FFMPEG)
    ensure_dirs()
    paths = [render_clip(index, beat) for index, beat in enumerate(BEATS, start=1)]
    concat_clips(paths)
    review_frames()
    make_thumbnail()
    verify()
    write_metadata()
    print(f"Created {OUTPUT}")
    print(f"Created {THUMBNAIL}")
    print(f"Created {CSV_PATH}")
    print(f"Created {MD_PATH}")


if __name__ == "__main__":
    main()
