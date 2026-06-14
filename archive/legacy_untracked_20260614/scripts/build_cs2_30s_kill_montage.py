from __future__ import annotations

import csv
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\abhik\Documents\Short Creation")
SOURCE = Path(r"C:\Users\abhik\Videos\2026-06-11_19-23-39.mp4")
FFMPEG = Path(r"C:\Users\abhik\AppData\Local\CapCut\Apps\7.6.0.3123\ffmpeg.exe")

RUN_NAME = "cs2_kill_montage_20260613"
OUT_DIR = ROOT / "live_video_pipeline" / "short_form" / RUN_NAME
WORK_DIR = ROOT / "live_video_pipeline" / "work" / RUN_NAME
REVIEW_DIR = ROOT / "live_video_pipeline" / "review" / RUN_NAME
META_DIR = ROOT / "live_video_pipeline" / "metadata" / RUN_NAME

OUTPUT = OUT_DIR / "cs2_30s_kill_montage_mrlluminati.mp4"
THUMBNAIL = OUT_DIR / "cs2_30s_kill_montage_thumbnail.jpg"
CSV_PATH = META_DIR / "cs2_30s_kill_montage_metadata.csv"
MD_PATH = META_DIR / "cs2_30s_kill_montage_metadata.md"


@dataclass(frozen=True)
class KillBeat:
    start: float
    duration: float
    label: str
    overlay: str


BEATS = [
    KillBeat(225.05, 3.05, "03:45.050", "DOORWAY SPRAY"),
    KillBeat(285.05, 2.50, "04:45.050", "YARD SPRAY"),
    KillBeat(428.35, 2.90, "07:08.350", "LANE PICK"),
    KillBeat(514.00, 2.85, "08:34.000", "BOX SPRAY"),
    KillBeat(640.15, 1.90, "10:40.150", "CLOSE TRADE"),
    KillBeat(780.45, 3.10, "13:00.450", "POINT BLANK"),
    KillBeat(795.40, 3.85, "13:15.400", "RUSH STOPPED"),
    KillBeat(819.20, 2.45, "13:39.200", "FAST RESET"),
    KillBeat(908.35, 3.15, "15:08.350", "CROSS MAP TAP"),
    KillBeat(948.25, 3.45, "15:48.250", "LONG RANGE PICK"),
    KillBeat(966.10, 3.00, "16:06.100", "HIGH ANGLE"),
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
    fill: tuple[int, int, int, int] | tuple[int, int, int],
    stroke_fill: tuple[int, int, int, int] | tuple[int, int, int] = (0, 0, 0, 230),
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


def make_overlay(index: int, beat: KillBeat) -> Path:
    path = WORK_DIR / f"overlay_{index:02d}.png"
    image = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    red = (232, 42, 47, 245)
    white = (255, 255, 255, 255)
    amber = (255, 206, 84, 255)
    soft_black = (0, 0, 0, 168)
    panel = (0, 0, 0, 144)

    draw.rounded_rectangle((82, 72, 998, 174), radius=30, fill=panel, outline=red, width=3)
    centered_text(draw, (540, 113), "MRLLUMINATI GAMING", font(32), white, stroke_width=3)

    if index == 1:
        centered_text(draw, (540, 292), "CS2 KILL\nMONTAGE", font(88), white, stroke_width=9, line_spacing=2)
    else:
        centered_text(draw, (540, 280), f"KILL #{index:02d}", font(78), white, stroke_width=8)

    draw.rounded_rectangle((86, 1468, 994, 1610), radius=34, fill=soft_black, outline=red, width=4)
    centered_text(draw, (540, 1529), beat.overlay, font(55), amber, stroke_width=6)

    progress_x = 88
    progress_y = 1660
    tick_w = 62
    gap = 10
    for i in range(len(BEATS)):
        color = red if i <= index - 1 else (255, 255, 255, 85)
        draw.rounded_rectangle(
            (progress_x + i * (tick_w + gap), progress_y, progress_x + i * (tick_w + gap) + tick_w, progress_y + 10),
            radius=5,
            fill=color,
        )

    centered_text(draw, (540, 1752), "FAST CS2 KILLS", font(40), white, stroke_width=4)
    image.save(path)
    return path


def render_clip(index: int, beat: KillBeat) -> Path:
    overlay = make_overlay(index, beat)
    out = WORK_DIR / f"clip_{index:02d}.mp4"
    vf = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=24,hue=s=0.72[bgv];"
        "[fg]scale=1080:-2,hue=s=1.10,unsharp=5:5:0.70:3:3:0.30[fgv];"
        "[bgv][fgv]overlay=(W-w)/2:(H-h)/2[base];"
        "[base][1:v]overlay=0:0,format=yuv420p,setsar=1,fps=60[v];"
        "[0:a]aresample=48000,highpass=f=65,acompressor=threshold=-18dB:ratio=2.6:attack=5:release=95,"
        "volume=1.12,alimiter=limit=0.95[a]"
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
            "14000k",
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
        "frame_mid.jpg": 15.4,
        "frame_payoff.jpg": 25.2,
        "frame_end.jpg": 31.1,
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
                "-update",
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
            "fps=1/3,scale=270:-1,tile=3x4:margin=8:padding=4",
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "3",
            REVIEW_DIR / "contact_sheet.jpg",
        ]
    )


def make_thumbnail() -> None:
    image = Image.new("RGB", (1080, 1920), (10, 10, 12))
    base_frame = REVIEW_DIR / "frame_hook.jpg"
    if base_frame.exists():
        base = Image.open(base_frame).convert("RGB").resize((1080, 1920))
        blurred = base.filter(ImageFilter.GaussianBlur(16))
        shade = Image.new("RGB", (1080, 1920), (0, 0, 0))
        image = Image.blend(blurred, shade, 0.32)
        focus = base.crop((0, 595, 1080, 1295)).resize((970, 628))
        image.paste(focus, (55, 590))

    draw = ImageDraw.Draw(image)
    red = (232, 42, 47)
    amber = (255, 202, 67)
    white = (255, 255, 255)
    black = (0, 0, 0)

    draw.rectangle((0, 0, 1080, 360), fill=black)
    draw.rectangle((0, 1700, 1080, 1920), fill=black)
    draw.rounded_rectangle((58, 52, 1022, 326), radius=34, fill=black, outline=red, width=8)
    centered_text(draw, (540, 138), "CS2", font(100), white, stroke_width=6)
    centered_text(draw, (540, 258), "KILL MONTAGE", font(70), amber, stroke_width=5)
    draw.rounded_rectangle((70, 566, 1010, 1250), radius=28, outline=red, width=7)
    draw.rounded_rectangle((92, 1410, 988, 1588), radius=30, fill=red)
    centered_text(draw, (540, 1496), "30 SEC CHAOS", font(78), white, stroke_width=5)
    centered_text(draw, (540, 1782), "MRLLUMINATI GAMING", font(47), white, stroke_width=4)
    image.save(THUMBNAIL, quality=93)


def verify() -> None:
    run([FFMPEG, "-v", "error", "-i", OUTPUT, "-f", "null", "-"])
    info = run([FFMPEG, "-hide_banner", "-i", OUTPUT, "-t", "0.1", "-f", "null", "-"]).stdout
    (REVIEW_DIR / "ffmpeg_probe.txt").write_text(info, encoding="utf-8")


def write_metadata() -> None:
    title = "CS2 Kill Montage Went Hard | 30 Sec Gaming Clips #shorts"
    hashtags = "#cs2 #counterstrike2 #cs2clips #cs2montage #killmontage #gamingclips #fpsgames #pcgaming #hindigaming #mrlluminati #shorts"
    tags = [
        "cs2",
        "counter strike 2",
        "cs2 kill montage",
        "cs2 clips",
        "cs2 hindi",
        "cs2 gameplay",
        "counter strike 2 shorts",
        "gaming shorts",
        "fps shorts",
        "kill montage",
        "fps montage",
        "pc gaming india",
        "mrlluminati gaming",
    ]
    description = (
        "Fast CS2 kill montage from my gameplay. Quick picks, clean sprays, close-range fights, "
        "and clutch timing packed into one short.\n\n"
        "Watch more gameplay clips on MrLluminati Gaming.\n\n"
        f"{hashtags}"
    )
    pinned = "Which kill was the cleanest?"

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
                "# CS2 30 Second Kill Montage Metadata",
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
