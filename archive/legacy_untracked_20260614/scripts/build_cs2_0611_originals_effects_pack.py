from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

import imageio_ffmpeg


PROJECT = "cs2_0611_originals_effects_20260613"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE_DIR = Path(r"C:\Users\abhik\Videos\Shorts\0611(1)")

BASE_HASHTAGS = (
    "#cs2 #counterstrike2 #cs2clips #cs2shorts #ancient "
    "#fpsgaming #gamingclips #indiangaming #pcgaming #shorts"
)
BASE_TAGS = (
    "cs2, counter strike 2, cs2 shorts, cs2 clips, cs2 ancient, cs2 quick kills, "
    "cs2 fight, cs2 reaction, cs2 aim, cs2 spray control, cs2 gameplay india, "
    "fps gaming, indian gaming, pc gameplay india, mrlluminati gaming"
)
DESCRIPTION_SUFFIX = (
    "CS2 Ancient Shorts from MrLluminati Gaming, reworked from the original trimmed clips "
    "without cutting any source portion."
)


@dataclass(frozen=True)
class EffectShort:
    slug: str
    source_numbers: tuple[int, ...]
    hook: str
    beat_one: str
    beat_two: str
    title: str
    description_lead: str
    tags: str
    pinned_comment: str
    thumbnail_text: str
    upload_order: int


SHORTS = (
    EffectShort(
        slug="01_ancient_b_fight_got_loud",
        source_numbers=(22,),
        hook="ANCIENT B\nGOT LOUD",
        beat_one="HOLD THE LINE",
        beat_two="STAY ALIVE",
        title="Ancient B Fight Got Loud | CS2 #shorts",
        description_lead="A full trimmed CS2 Ancient B fight, kept as one complete source clip.",
        tags=f"{BASE_TAGS}, cs2 ancient b site, cs2 b fight, cs2 hold angle",
        pinned_comment="Would you hold this angle or rotate?",
        thumbnail_text="B FIGHT",
        upload_order=1,
    ),
    EffectShort(
        slug="02_close_range_fight_went_wild",
        source_numbers=(15, 17),
        hook="CLOSE RANGE\nWENT WILD",
        beat_one="NO SPACE",
        beat_two="RESET FAST",
        title="Close Range Fight Went Wild | CS2 Ancient #shorts",
        description_lead="Two complete trimmed CS2 clips merged without cutting either source clip.",
        tags=f"{BASE_TAGS}, cs2 close range, cs2 ancient fight, cs2 panic fight",
        pinned_comment="Close-range fights or long angles: what should I upload more?",
        thumbnail_text="CLOSE RANGE",
        upload_order=2,
    ),
    EffectShort(
        slug="03_b_wall_pressure_was_real",
        source_numbers=(24, 16),
        hook="B WALL\nPRESSURE",
        beat_one="STAY CALM",
        beat_two="KEEP HOLDING",
        title="B Wall Pressure Was Real | CS2 #shorts",
        description_lead="Complete B-wall pressure clips from CS2 Ancient, merged as full A-to-B trims.",
        tags=f"{BASE_TAGS}, cs2 b wall, cs2 pressure, cs2 ancient b site",
        pinned_comment="Would you keep holding or fall back?",
        thumbnail_text="B WALL",
        upload_order=3,
    ),
    EffectShort(
        slug="04_low_hp_still_holding",
        source_numbers=(21, 23),
        hook="LOW HP\nSTILL HOLDING",
        beat_one="NO PANIC",
        beat_two="SURVIVE IT",
        title="Low HP Still Holding | CS2 Ancient #shorts",
        description_lead="Low-HP CS2 Ancient pressure clips, kept as full original trims.",
        tags=f"{BASE_TAGS}, cs2 low hp, cs2 survival, cs2 ancient pressure",
        pinned_comment="Would you fight this on low HP?",
        thumbnail_text="LOW HP HOLD",
        upload_order=4,
    ),
    EffectShort(
        slug="05_stairs_fight_got_messy",
        source_numbers=(14, 20),
        hook="STAIRS FIGHT\nGOT MESSY",
        beat_one="FULL PRESSURE",
        beat_two="BAD TIMING",
        title="Stairs Fight Got Messy | CS2 #shorts",
        description_lead="Full trimmed stairs-pressure clips from CS2 Ancient with no internal cuts.",
        tags=f"{BASE_TAGS}, cs2 stairs fight, cs2 ancient stairs, cs2 pressure fight",
        pinned_comment="Was this bad timing or bad position?",
        thumbnail_text="STAIRS FIGHT",
        upload_order=5,
    ),
    EffectShort(
        slug="06_box_fight_survival",
        source_numbers=(13, 19),
        hook="BOX FIGHT\nSURVIVAL",
        beat_one="CLOSE ANGLE",
        beat_two="WATCH CORNER",
        title="Box Fight Survival | CS2 Ancient #shorts",
        description_lead="Two complete box-area CS2 Ancient clips merged without trimming the sources.",
        tags=f"{BASE_TAGS}, cs2 box fight, cs2 ancient box, cs2 close angle",
        pinned_comment="Would you clear the box first?",
        thumbnail_text="BOX FIGHT",
        upload_order=6,
    ),
    EffectShort(
        slug="07_pistol_angle_hold",
        source_numbers=(7, 11),
        hook="PISTOL ANGLE\nHOLD",
        beat_one="WAIT FOR PEEK",
        beat_two="HOLD IT",
        title="Pistol Angle Hold | CS2 #shorts",
        description_lead="Complete pistol-angle and hold clips, packaged as one CS2 Short.",
        tags=f"{BASE_TAGS}, cs2 pistol angle, cs2 angle hold, cs2 ancient hold",
        pinned_comment="Swing first or wait for the peek?",
        thumbnail_text="PISTOL HOLD",
        upload_order=7,
    ),
    EffectShort(
        slug="08_outside_reset_fight",
        source_numbers=(5, 10),
        hook="OUTSIDE RESET\nFIGHT",
        beat_one="CHECK ANGLE",
        beat_two="RESET",
        title="Outside Reset Fight | CS2 Ancient #shorts",
        description_lead="Outside-fight CS2 clips kept whole and merged into one clean Shorts package.",
        tags=f"{BASE_TAGS}, cs2 outside fight, cs2 reset fight, cs2 ancient outside",
        pinned_comment="Good reset or should the fight continue?",
        thumbnail_text="OUTSIDE RESET",
        upload_order=8,
    ),
    EffectShort(
        slug="09_tunnel_rotation_fight",
        source_numbers=(9, 25),
        hook="TUNNEL ROTATION\nFIGHT",
        beat_one="KEEP MOVING",
        beat_two="LAST ANGLE",
        title="Tunnel Rotation Fight | CS2 #shorts",
        description_lead="Two full trimmed rotation clips from CS2 Ancient, merged without cutting either clip.",
        tags=f"{BASE_TAGS}, cs2 tunnel fight, cs2 rotation, cs2 ancient rotation",
        pinned_comment="Was the rotation too late?",
        thumbnail_text="ROTATION",
        upload_order=9,
    ),
    EffectShort(
        slug="10_opening_route_pressure",
        source_numbers=(8, 1),
        hook="OPENING ROUTE\nPRESSURE",
        beat_one="FIRST MOVE",
        beat_two="CONTACT",
        title="Opening Route Pressure | CS2 Ancient #shorts",
        description_lead="Opening pressure clips from the trimmed CS2 Ancient set, kept complete.",
        tags=f"{BASE_TAGS}, cs2 opening fight, cs2 ancient route, cs2 first contact",
        pinned_comment="Good opening route or too risky?",
        thumbnail_text="OPENING ROUTE",
        upload_order=10,
    ),
    EffectShort(
        slug="11_underpass_angle_hold",
        source_numbers=(12, 4),
        hook="UNDERPASS\nANGLE HOLD",
        beat_one="DARK ANGLE",
        beat_two="CHECK IT",
        title="Underpass Angle Hold | CS2 #shorts",
        description_lead="Full underpass and angle-hold source clips merged as one CS2 Short.",
        tags=f"{BASE_TAGS}, cs2 underpass, cs2 angle hold, cs2 dark angle",
        pinned_comment="Would you clear this angle slower?",
        thumbnail_text="UNDERPASS",
        upload_order=11,
    ),
    EffectShort(
        slug="12_fast_frag_chain",
        source_numbers=(3, 6, 2, 18),
        hook="FAST FRAG\nCHAIN",
        beat_one="QUICK CLIPS",
        beat_two="NO TRIMS",
        title="Fast Frag Chain | CS2 Ancient #shorts",
        description_lead="Four short original CS2 trims merged whole into one fast Ancient Short.",
        tags=f"{BASE_TAGS}, cs2 fast frag, cs2 quick clips, cs2 ancient short clips",
        pinned_comment="Should I keep these ultra-fast clips separate next time?",
        thumbnail_text="FAST FRAGS",
        upload_order=12,
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


def source_file(source_dir: Path, number: int) -> Path:
    path = source_dir / f"0611(1)-{number}.mp4"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def media_duration(ffmpeg: str, path: Path) -> float:
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if not match:
        raise RuntimeError(f"Could not read duration for {path}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def write_ass(short: EffectShort, duration: float) -> Path:
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
        "Style: Logo,Arial,30,&H00FFFFFF,&H000000FF,&H99000000,&H99000000,-1,0,0,0,100,100,1,0,1,2,0,8,48,48,42,1",
        "Style: Hook,Arial Black,76,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,7,3,8,50,50,160,1",
        "Style: Beat,Arial Black,52,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,6,2,2,70,70,240,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 6,{ass_time(0)},{ass_time(duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.08)},{ass_time(min(2.1, duration - 0.5))},Hook,,0,0,0,,"
            r"{\fad(50,120)\t(0,180,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 8,{ass_time(3.1)},{ass_time(min(4.8, duration - 0.8))},Beat,,0,0,0,,"
            r"{\fad(60,120)}"
            f"{ass_escape(short.beat_one)}"
        ),
        (
            f"Dialogue: 8,{ass_time(max(5.4, duration - 2.8))},{ass_time(duration - 0.45)},Beat,,0,0,0,,"
            r"{\fad(60,150)}"
            f"{ass_escape(short.beat_two)}"
        ),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def video_filter(index: int) -> str:
    return (
        f"[{index}:v]fps=30,split=2[bg{index}][fg{index}];"
        f"[bg{index}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"boxblur=24:1,eq=brightness=-0.10:saturation=1.08[bg{index}b];"
        f"[fg{index}]scale=1080:-2:flags=lanczos,setsar=1[fg{index}b];"
        f"[bg{index}b][fg{index}b]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=655:w=1080:h=3:color=white@0.14:t=fill,"
        "drawbox=x=0:y=1262:w=1080:h=3:color=white@0.14:t=fill,"
        "eq=contrast=1.07:saturation=1.12:brightness=0.006,"
        "unsharp=5:5:0.45:3:3:0.20,"
        f"format=yuv420p[v{index}]"
    )


def audio_filter(index: int) -> str:
    return (
        f"[{index}:a]aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,"
        "highpass=f=65,acompressor=threshold=-18dB:ratio=2.6:attack=8:release=120,"
        f"volume=1.10,alimiter=limit=0.95[a{index}]"
    )


def render_short(ffmpeg: str, source_dir: Path, short: EffectShort, durations: dict[int, float]) -> Path:
    files = [source_file(source_dir, number) for number in short.source_numbers]
    duration = sum(durations[number] for number in short.source_numbers)
    ass_path = write_ass(short, duration)
    out = SHORT_DIR / f"{short.slug}.mp4"

    inputs: list[str] = []
    filters: list[str] = []
    concat_refs: list[str] = []
    for index, file in enumerate(files):
        inputs.extend(["-i", str(file)])
        filters.append(video_filter(index))
        filters.append(audio_filter(index))
        concat_refs.append(f"[v{index}][a{index}]")

    filters.append(f"{''.join(concat_refs)}concat=n={len(files)}:v=1:a=1[vcat][acat]")
    filters.append(
        f"[vcat]{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.05,"
        f"fade=t=out:st={max(0, duration - 0.20):.3f}:d=0.20[vout]"
    )
    filters.append(f"[acat]afade=t=out:st={max(0, duration - 0.20):.3f}:d=0.20[aout]")

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
            str(out),
        ]
    )
    return out


def make_review_assets(ffmpeg: str, path: Path, short: EffectShort, duration: float) -> None:
    frame_dir = REVIEW_DIR / "frames" / short.slug
    frame_dir.mkdir(parents=True, exist_ok=True)
    for label, second in (
        ("hook", 0.6),
        ("middle", min(max(1.0, duration * 0.50), duration - 0.8)),
        ("ending", max(0.8, duration - 0.8)),
    ):
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
                str(path),
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
            str(path),
            "-vf",
            "fps=1/2,scale=216:-1,tile=5x2",
            "-frames:v",
            "1",
            str(REVIEW_DIR / f"{short.slug}_contact.jpg"),
        ]
    )


def write_metadata(paths: dict[str, Path], durations: dict[int, float]) -> None:
    rows = []
    used: list[int] = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        used.extend(short.source_numbers)
        source_files = [f"0611(1)-{number}.mp4" for number in short.source_numbers]
        duration = sum(durations[number] for number in short.source_numbers)
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": paths[short.slug].name,
                "source_files": " + ".join(source_files),
                "duration_seconds": round(duration, 2),
                "source_rule": "full original clips only; no source trim; no internal cuts",
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )

    expected = list(range(1, 26))
    if sorted(used) != expected:
        raise RuntimeError(f"Source clip coverage mismatch. Used: {sorted(used)}")

    csv_path = META_DIR / "cs2_0611_originals_effects_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# CS2 0611 Original Trim Effects Pack",
        "",
        f"- Source folder: {DEFAULT_SOURCE_DIR}",
        "- Rule: every source clip is used whole. No internal source trimming.",
        "- Output: 12 Shorts made from 25 original clips, grouped toward 15-20 seconds where possible.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['upload_order']}. {row['file']}",
                f"- Source files: {row['source_files']}",
                f"- Duration: {row['duration_seconds']}s",
                f"- Rule: {row['source_rule']}",
                f"- Title: {row['title']}",
                f"- Description: {row['description']}",
                f"- Hashtags: {row['hashtags']}",
                f"- Tags: {row['tags']}",
                f"- Pinned comment: {row['pinned_comment']}",
                f"- Thumbnail text: {row['thumbnail_text']}",
                "",
            ]
        )
    (META_DIR / "cs2_0611_originals_effects_metadata.md").write_text("\n".join(lines), encoding="utf-8")


def verify_outputs(ffmpeg: str, paths: dict[str, Path]) -> None:
    for path in paths.values():
        run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build effects-only CS2 Shorts from original trimmed 0611 clips.")
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()

    ensure_dirs()
    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        raise SystemExit(f"Source folder not found: {source_dir}")

    selected = [short for short in SHORTS if not args.only or short.slug in set(args.only)]
    if args.only and len(selected) != len(set(args.only)):
        known = ", ".join(short.slug for short in SHORTS)
        raise SystemExit(f"Unknown slug in --only. Known slugs: {known}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    durations = {number: media_duration(ffmpeg, source_file(source_dir, number)) for number in range(1, 26)}

    paths: dict[str, Path] = {}
    for short in selected:
        duration = sum(durations[number] for number in short.source_numbers)
        sources = ", ".join(str(number) for number in short.source_numbers)
        print(f"Rendering {short.slug}: clips {sources} ({duration:.2f}s)")
        out = render_short(ffmpeg, source_dir, short, durations)
        paths[short.slug] = out
        make_review_assets(ffmpeg, out, short, duration)

    if not args.only:
        verify_outputs(ffmpeg, paths)
        write_metadata(paths, durations)
    print(f"Rendered {len(paths)} Shorts to {SHORT_DIR}")
    print(f"Metadata written to {META_DIR}")
    print(f"Review assets written to {REVIEW_DIR}")


if __name__ == "__main__":
    main()
