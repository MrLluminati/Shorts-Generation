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


PROJECT = "cs2_shorts_file_kill_montages_20260613"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE = Path(r"C:\Users\abhik\Videos\Shorts\Shorts.mp4")

BASE_HASHTAGS = (
    "#cs2 #counterstrike2 #cs2clips #cs2shorts #ancient "
    "#fpsgaming #gamingclips #indiangaming #pcgaming #shorts"
)
BASE_TAGS = (
    "cs2, counter strike 2, cs2 shorts, cs2 clips, cs2 ancient, cs2 kill montage, "
    "counter strike 2 kill montage, cs2 quick kills, cs2 reaction, cs2 aim, "
    "cs2 spray control, fps gaming, indian gaming, pc gameplay india, mrlluminati gaming"
)
DESCRIPTION_SUFFIX = (
    "Fast CS2 kill montage from MrLluminati Gaming, cut for quick fights, clean reactions, "
    "and no filler walking."
)


@dataclass(frozen=True)
class Burst:
    start: str
    duration: float


@dataclass(frozen=True)
class MontageShort:
    slug: str
    bursts: tuple[Burst, ...]
    hook: str
    beat_one: str
    beat_two: str
    title: str
    description_lead: str
    tags: str
    pinned_comment: str
    thumbnail_text: str
    upload_order: int

    @property
    def duration(self) -> float:
        return sum(burst.duration for burst in self.bursts) - 0.10 * (len(self.bursts) - 1)


SHORTS = (
    MontageShort(
        slug="01_ancient_quick_kill_chain",
        bursts=(
            Burst("00:00:03.300", 2.8),
            Burst("00:00:35.500", 2.8),
            Burst("00:02:04.300", 3.0),
            Burst("00:02:24.500", 3.4),
        ),
        hook="KILL CHAIN\nSTARTED FAST",
        beat_one="NO FILLER",
        beat_two="ONE MORE",
        title="CS2 Ancient Kill Chain Went Fast | #cs2 #shorts",
        description_lead="A fast Ancient kill-chain montage cut straight to the fights.",
        tags=f"{BASE_TAGS}, cs2 ancient kill chain, cs2 fast kills, cs2 montage shorts",
        pinned_comment="Best kill in this chain?",
        thumbnail_text="KILL CHAIN",
        upload_order=1,
    ),
    MontageShort(
        slug="02_low_hp_spray_survival",
        bursts=(
            Burst("00:01:31.700", 3.8),
            Burst("00:02:33.800", 3.2),
            Burst("00:02:46.400", 4.0),
        ),
        hook="LOW HP\nSTILL FIGHTING",
        beat_one="HOLD ANGLE",
        beat_two="SURVIVE IT",
        title="Low HP Spray Survival | CS2 Ancient #shorts",
        description_lead="Low HP fights stitched into a quick CS2 Ancient survival montage.",
        tags=f"{BASE_TAGS}, cs2 low hp, cs2 survival, cs2 spray survival, cs2 ancient fights",
        pinned_comment="Would you keep fighting on low HP?",
        thumbnail_text="LOW HP FIGHT",
        upload_order=2,
    ),
    MontageShort(
        slug="03_close_range_panic_kills",
        bursts=(
            Burst("00:02:23.600", 4.0),
            Burst("00:02:47.700", 3.8),
            Burst("00:03:16.000", 4.3),
        ),
        hook="CLOSE RANGE\nPANIC KILLS",
        beat_one="TOO CLOSE",
        beat_two="RESET FAST",
        title="Close Range Panic Kills | CS2 #shorts",
        description_lead="Close-range CS2 fights cut into a quick panic-kill montage.",
        tags=f"{BASE_TAGS}, cs2 close range, cs2 panic kills, cs2 close fight, cs2 quick montage",
        pinned_comment="Close fights or long angles: what should I post more?",
        thumbnail_text="PANIC KILLS",
        upload_order=3,
    ),
    MontageShort(
        slug="04_angle_hold_montage",
        bursts=(
            Burst("00:00:58.800", 3.2),
            Burst("00:01:04.100", 3.5),
            Burst("00:02:10.500", 3.0),
            Burst("00:03:06.800", 3.5),
        ),
        hook="ANGLE HOLD\nMONTAGE",
        beat_one="WAIT FOR PEEK",
        beat_two="BURST FIRE",
        title="Angle Hold Montage | CS2 Ancient #shorts",
        description_lead="Angle holds and quick reaction bursts from a CS2 Ancient round.",
        tags=f"{BASE_TAGS}, cs2 angle hold, cs2 peek reaction, cs2 burst fire, cs2 ancient angles",
        pinned_comment="Hold the angle or swing first?",
        thumbnail_text="ANGLE HOLD",
        upload_order=4,
    ),
    MontageShort(
        slug="05_final_fight_kill_montage",
        bursts=(
            Burst("00:03:06.400", 4.4),
            Burst("00:03:16.000", 5.4),
            Burst("00:02:24.500", 3.0),
        ),
        hook="FINAL FIGHTS\nGOT LOUD",
        beat_one="KEEP FIRING",
        beat_two="LAST PICK",
        title="Final Fight Kill Montage | CS2 #shorts",
        description_lead="The loudest late-round fights packed into a short CS2 kill montage.",
        tags=f"{BASE_TAGS}, cs2 final fight, cs2 late round, cs2 kill montage, cs2 ancient",
        pinned_comment="Did the final fight deserve a full clip?",
        thumbnail_text="FINAL FIGHTS",
        upload_order=5,
    ),
)


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def ass_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:d}:{minutes:02d}:{secs:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def subtitle_filter_arg(path: Path) -> str:
    return f"subtitles=filename='{path.relative_to(ROOT).as_posix()}'"


def write_ass(short: MontageShort) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    duration = short.duration
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
        "Style: Logo,Arial,30,&H00FFFFFF,&H000000FF,&H99000000,&H99000000,-1,0,0,0,100,100,1,0,1,2,0,8,48,48,42,1",
        "Style: Hook,Arial Black,76,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,7,3,8,50,50,160,1",
        "Style: Beat,Arial Black,52,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,6,2,2,70,70,240,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 6,{ass_time(0)},{ass_time(duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.08)},{ass_time(min(2.0, duration - 0.5))},Hook,,0,0,0,,"
            r"{\fad(50,120)\t(0,180,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 8,{ass_time(3.0)},{ass_time(min(4.7, duration - 0.8))},Beat,,0,0,0,,"
            r"{\fad(60,120)}"
            f"{ass_escape(short.beat_one)}"
        ),
        (
            f"Dialogue: 8,{ass_time(max(5.8, duration - 2.7))},{ass_time(duration - 0.45)},Beat,,0,0,0,,"
            r"{\fad(60,150)}"
            f"{ass_escape(short.beat_two)}"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def video_layout_filter(input_index: int, label: str) -> str:
    return (
        f"[{input_index}:v]fps=30,split=2[bg{label}][fg{label}];"
        f"[bg{label}]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,boxblur=24:1,eq=brightness=-0.10:saturation=1.08[bg{label}b];"
        f"[fg{label}]scale=1080:-2:flags=lanczos,setsar=1[fg{label}b];"
        f"[bg{label}b][fg{label}b]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=655:w=1080:h=3:color=white@0.14:t=fill,"
        "drawbox=x=0:y=1262:w=1080:h=3:color=white@0.14:t=fill,"
        "eq=contrast=1.06:saturation=1.10:brightness=0.006,"
        "unsharp=5:5:0.42:3:3:0.18,"
        f"format=yuv420p[v{label}]"
    )


def audio_filter(input_index: int, label: str, duration: float) -> str:
    return (
        f"[{input_index}:a]aresample=48000,highpass=f=65,"
        "acompressor=threshold=-18dB:ratio=2.6:attack=8:release=120,"
        "volume=1.10,alimiter=limit=0.95,"
        f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0.0, duration - 0.03):.3f}:d=0.03[a{label}]"
    )


def xfade_chain(labels: list[str], durations: list[float]) -> tuple[str, str, str]:
    if len(labels) == 1:
        return "", f"[v{labels[0]}]", f"[a{labels[0]}]"

    parts: list[str] = []
    current_v = f"[v{labels[0]}]"
    current_a = f"[a{labels[0]}]"
    elapsed = durations[0]
    transition = 0.10

    for index, label in enumerate(labels[1:], start=1):
        v_out = f"vx{index}"
        a_out = f"ax{index}"
        offset = elapsed - transition
        parts.append(
            f"{current_v}[v{label}]xfade=transition=fade:duration={transition:.2f}:"
            f"offset={offset:.3f}[{v_out}]"
        )
        parts.append(
            f"{current_a}[a{label}]acrossfade=d={transition:.2f}:c1=tri:c2=tri[{a_out}]"
        )
        current_v = f"[{v_out}]"
        current_a = f"[{a_out}]"
        elapsed += durations[index] - transition

    return ";".join(parts), current_v, current_a


def render_short(ffmpeg: str, source: Path, short: MontageShort) -> Path:
    ass_path = write_ass(short)
    output = SHORT_DIR / f"{short.slug}.mp4"
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    durations: list[float] = []

    for index, burst in enumerate(short.bursts):
        inputs.extend(["-ss", burst.start, "-t", f"{burst.duration:.3f}", "-i", str(source)])
        label = str(index)
        labels.append(label)
        durations.append(burst.duration)
        filters.append(video_layout_filter(index, label))
        filters.append(audio_filter(index, label, burst.duration))

    chain, video_label, audio_label = xfade_chain(labels, durations)
    if chain:
        filters.append(chain)
    filters.append(
        f"{video_label}{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.04,"
        f"fade=t=out:st={max(0, short.duration - 0.18):.3f}:d=0.18[vout]"
    )
    filters.append(f"{audio_label}afade=t=out:st={max(0, short.duration - 0.18):.3f}:d=0.18[aout]")

    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[vout]",
            "-map",
            "[aout]",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
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
            str(output),
        ]
    )
    return output


def make_review_assets(ffmpeg: str, video_path: Path, short: MontageShort) -> None:
    frame_dir = REVIEW_DIR / "frames" / short.slug
    frame_dir.mkdir(parents=True, exist_ok=True)
    positions = [
        ("hook", 0.6),
        ("middle", min(max(1.0, short.duration * 0.50), short.duration - 0.8)),
        ("payoff", max(0.8, short.duration - 0.8)),
    ]
    for label, second in positions:
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
                str(video_path),
                "-frames:v",
                "1",
                str(frame_dir / f"{label}.jpg"),
            ]
        )
    run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video_path),
            "-vf",
            "fps=2,scale=216:-1,tile=5x3",
            "-frames:v",
            "1",
            str(REVIEW_DIR / f"{short.slug}_contact.jpg"),
        ]
    )


def write_metadata(paths: dict[str, Path]) -> None:
    rows = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": paths[short.slug].name,
                "source_bursts": " | ".join(f"{burst.start}+{burst.duration:.1f}s" for burst in short.bursts),
                "duration_seconds": round(short.duration, 2),
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )

    csv_path = META_DIR / "cs2_shorts_file_kill_montages_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# CS2 Kill Montage Shorts",
        "",
        f"- Source: {DEFAULT_SOURCE}",
        "- Style: multi-burst kill montage, no filler walking",
        "- Layout: blurred 1080x1920 background with centered gameplay",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['upload_order']}. {row['file']}",
                f"- Source bursts: {row['source_bursts']}",
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
    (META_DIR / "cs2_shorts_file_kill_montages_metadata.md").write_text("\n".join(lines), encoding="utf-8")


def verify_outputs(ffmpeg: str, paths: dict[str, Path]) -> None:
    for path in paths.values():
        run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build kill montage Shorts from C:/Users/abhik/Videos/Shorts/Shorts.mp4.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()

    ensure_dirs()
    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    selected = [short for short in SHORTS if not args.only or short.slug in set(args.only)]
    if args.only and len(selected) != len(set(args.only)):
        known = ", ".join(short.slug for short in SHORTS)
        raise SystemExit(f"Unknown slug in --only. Known slugs: {known}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    paths: dict[str, Path] = {}
    for short in selected:
        print(f"Rendering kill montage: {short.slug}")
        output = render_short(ffmpeg, source, short)
        paths[short.slug] = output
        make_review_assets(ffmpeg, output, short)

    verify_outputs(ffmpeg, paths)
    write_metadata(paths)
    print(f"Rendered {len(paths)} kill montage Shorts to {SHORT_DIR}")
    print(f"Metadata written to {META_DIR}")
    print(f"Review assets written to {REVIEW_DIR}")


if __name__ == "__main__":
    main()
