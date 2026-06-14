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


PROJECT = "cs2_rank_grind_20260611"
PIPELINE = ROOT / "live_video_pipeline"
SHORT_DIR = PIPELINE / "short_form" / PROJECT
META_DIR = PIPELINE / "metadata" / PROJECT
WORK_DIR = PIPELINE / "work" / PROJECT
REVIEW_DIR = PIPELINE / "review" / PROJECT
ASS_DIR = WORK_DIR / "subtitles"

DEFAULT_SOURCE = Path(
    r"C:\Users\abhik\Downloads\🔴 LIVE CS_GO - Grinding XP & Rank _ Competitive Gameplay _ MrLluminati Gaming.mp4"
)

BASE_HASHTAGS = (
    "#cs2 #counterstrike2 #cs2clips #cs2shorts #hindigaming "
    "#indiangaming #pcgaming #fpsgames #gamingclips #shorts"
)
BASE_TAGS = (
    "counter strike 2, cs2, cs2 hindi, counter strike 2 hindi, cs2 gameplay, "
    "cs2 kill montage, cs2 quick kills, cs2 reaction, cs2 clutch, cs2 spray control, "
    "fps gaming, hindi gaming, indian gaming, pc gameplay india, gaming shorts india, "
    "mrlluminati gaming"
)
DESCRIPTION_SUFFIX = (
    "Fast CS2 Hindi gameplay highlight from MrLluminati Gaming, focused on quick fights, "
    "reaction moments, and rank-grind clips."
)


@dataclass(frozen=True)
class CS2Short:
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


SHORTS = [
    CS2Short(
        slug="01_mid_angle_spray",
        start="00:06:17.500",
        duration=15.8,
        hook="MID ANGLE\nSPRAY",
        beat_one="FIRST CONTACT",
        beat_two="SCOPE LOCKED",
        title="Mid Angle Spray Control | CS2 Hindi #shorts",
        description_lead="A fast CS2 mid-angle fight with quick spray control and no slow setup.",
        tags=f"{BASE_TAGS}, cs2 mid fight, cs2 rifle spray, cs2 mirage, cs2 aim duel",
        pinned_comment="Clean spray or panic spray?",
        thumbnail_text="SPRAY CONTROL",
        upload_order=1,
    ),
    CS2Short(
        slug="02_doorway_peek_went_wrong",
        start="00:08:59.500",
        duration=12.8,
        hook="DOORWAY PEEK\nWENT WRONG",
        beat_one="FAST REACTION",
        beat_two="NO TIME TO THINK",
        title="Doorway Peek Went Wrong | CS2 Hindi #shorts",
        description_lead="A tight doorway peek turns into a fast CS2 reaction fight.",
        tags=f"{BASE_TAGS}, cs2 doorway peek, cs2 reaction shot, cs2 close fight, cs2 aim",
        pinned_comment="Would you swing that doorway or hold the angle?",
        thumbnail_text="BAD PEEK?",
        upload_order=2,
    ),
    CS2Short(
        slug="03_blue_site_scope_duel",
        start="00:04:43.500",
        duration=12.2,
        hook="SCOPE DUEL\nON SITE",
        beat_one="HOLD THE LINE",
        beat_two="QUICK BURST",
        title="Scope Duel On Site | CS2 Hindi #shorts",
        description_lead="A short scoped site fight from the CS2 rank grind.",
        tags=f"{BASE_TAGS}, cs2 scope duel, cs2 site hold, cs2 nuke, cs2 scoped rifle",
        pinned_comment="Hold this angle or reposition faster?",
        thumbnail_text="SCOPE DUEL",
        upload_order=3,
    ),
    CS2Short(
        slug="04_clean_angle_hold",
        start="00:01:38.000",
        duration=13.0,
        hook="CLEAN ANGLE\nHOLD",
        beat_one="WAIT FOR PEEK",
        beat_two="TAP BURST",
        title="Clean Angle Hold | CS2 Hindi #shorts",
        description_lead="A clean angle hold with a quick burst and immediate reposition.",
        tags=f"{BASE_TAGS}, cs2 angle hold, cs2 tap burst, cs2 aim duel, cs2 nuke gameplay",
        pinned_comment="Was this angle worth holding?",
        thumbnail_text="ANGLE HOLD",
        upload_order=4,
    ),
    CS2Short(
        slug="05_long_angle_spray",
        start="00:05:51.250",
        duration=13.5,
        hook="LONG ANGLE\nSPRAY",
        beat_one="COMMIT TO FIGHT",
        beat_two="KEEP PRESSURE",
        title="Long Angle Spray Fight | CS2 Hindi #shorts",
        description_lead="A long-angle CS2 spray fight cut straight to the action.",
        tags=f"{BASE_TAGS}, cs2 long angle, cs2 spray fight, cs2 rifle fight, cs2 fast clips",
        pinned_comment="Would you keep spraying or reset the aim?",
        thumbnail_text="LONG SPRAY",
        upload_order=5,
    ),
    CS2Short(
        slug="06_outside_burst_and_reload",
        start="00:03:11.000",
        duration=13.5,
        hook="OUTSIDE FIGHT\nSTARTED FAST",
        beat_one="CHECK CORNER",
        beat_two="RELOAD RESET",
        title="Outside Fight Started Fast | CS2 Hindi #shorts",
        description_lead="The outside fight starts fast, then resets into a reload and reposition.",
        tags=f"{BASE_TAGS}, cs2 outside fight, cs2 nuke outside, cs2 reload, cs2 quick fight",
        pinned_comment="Good reset, or should the push continue?",
        thumbnail_text="FAST FIGHT",
        upload_order=6,
    ),
    CS2Short(
        slug="07_close_corner_panic",
        start="00:44:32.250",
        duration=13.0,
        hook="CLOSE CORNER\nPANIC",
        beat_one="TOO CLOSE",
        beat_two="RECOVER FAST",
        title="Close Corner Panic | CS2 Hindi #shorts",
        description_lead="A close-corner CS2 reaction moment where the fight gets uncomfortable fast.",
        tags=f"{BASE_TAGS}, cs2 close corner, cs2 panic moment, cs2 reaction, cs2 close fight",
        pinned_comment="Would you back off here or take the duel?",
        thumbnail_text="CLOSE CALL",
        upload_order=7,
    ),
    CS2Short(
        slug="08_multi_enemy_push",
        start="00:26:59.500",
        duration=13.5,
        hook="MULTI ENEMY\nPUSH",
        beat_one="TRACK BOTH",
        beat_two="RESET AIM",
        title="Multi Enemy Push | CS2 Hindi #shorts",
        description_lead="A short multi-enemy CS2 push with quick aim tracking.",
        tags=f"{BASE_TAGS}, cs2 multi enemy, cs2 aim tracking, cs2 push, cs2 rifle clips",
        pinned_comment="Which enemy would you focus first?",
        thumbnail_text="MULTI PUSH",
        upload_order=8,
    ),
    CS2Short(
        slug="09_garage_fight_got_messy",
        start="00:00:37.500",
        duration=12.5,
        hook="GARAGE FIGHT\nGOT MESSY",
        beat_one="FIRST SWING",
        beat_two="BAD TRADE",
        title="Garage Fight Got Messy | CS2 Hindi #shorts",
        description_lead="A messy early garage fight with a fast swing and bad trade.",
        tags=f"{BASE_TAGS}, cs2 garage fight, cs2 early fight, cs2 trade, cs2 rank grind",
        pinned_comment="Would you take that trade or fall back?",
        thumbnail_text="MESSY FIGHT",
        upload_order=9,
    ),
]


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


def write_ass(short: CS2Short) -> Path:
    path = ASS_DIR / f"{short.slug}.ass"
    duration = short.duration
    second_start = min(max(duration - 5.2, 6.2), max(6.2, duration - 2.8))
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 720",
        "PlayResY: 1280",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        (
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
            "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
        ),
        "Style: Logo,Arial,22,&H00FFFFFF,&H000000FF,&HAA000000,&HAA000000,-1,0,0,0,100,100,1,0,1,2,0,8,30,30,28,1",
        "Style: Hook,Arial Black,50,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,5,2,8,34,34,122,1",
        "Style: Beat,Arial Black,36,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,1,0,1,4,1,2,48,48,178,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 6,{ass_time(0)},{ass_time(duration)},Logo,,0,0,0,,MRLLUMINATI GAMING",
        (
            f"Dialogue: 10,{ass_time(0.12)},{ass_time(2.7)},Hook,,0,0,0,,"
            r"{\fad(80,180)\t(0,260,\fscx106\fscy106)}"
            f"{ass_escape(short.hook)}"
        ),
        (
            f"Dialogue: 8,{ass_time(3.1)},{ass_time(min(6.4, duration - 0.7))},Beat,,0,0,0,,"
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


def render_short(ffmpeg: str, source: Path, short: CS2Short) -> Path:
    ass_path = write_ass(short)
    output = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.35)

    # The source is a vertical live export with the actual 16:9 gameplay embedded
    # around y=350. Crop the gameplay first, then build a clean Shorts layout.
    video_filter = (
        "[0:v]crop=720:405:0:350,split=2[bg][fg];"
        "[bg]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
        "boxblur=22:1,eq=brightness=-0.08:saturation=1.08[bg2];"
        "[fg]scale=720:405:flags=lanczos,setsar=1[fg2];"
        "[bg2][fg2]overlay=0:437,"
        "drawbox=x=0:y=436:w=720:h=407:color=white@0.14:t=2,"
        "eq=contrast=1.05:saturation=1.08:brightness=0.01,"
        "unsharp=5:5:0.45:3:3:0.2,"
        "delogo=x=558:y=694:w=158:h=74,"
        "drawbox=x=584:y=748:w=132:h=54:color=black@0.85:t=fill,"
        f"{subtitle_filter_arg(ass_path)},"
        "fade=t=in:st=0:d=0.10,"
        f"fade=t=out:st={fade_out:.3f}:d=0.35,"
        "format=yuv420p[v]"
    )
    audio_filter = (
        "[0:a]aresample=48000,highpass=f=65,"
        "acompressor=threshold=-18dB:ratio=2.6:attack=8:release=120,"
        "volume=1.10,alimiter=limit=0.95,"
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
            "18",
            "-r",
            "30",
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


def make_review_assets(ffmpeg: str, video_path: Path, short: CS2Short) -> None:
    slug = short.slug
    frame_dir = REVIEW_DIR / "frames" / slug
    frame_dir.mkdir(parents=True, exist_ok=True)
    positions = [
        ("hook", 0.6),
        ("fight", min(short.duration * 0.42, max(0.8, short.duration - 1.0))),
        ("payoff", max(0.8, short.duration - 1.0)),
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
            "fps=1/2,scale=144:-1,tile=5x2",
            "-frames:v",
            "1",
            str(REVIEW_DIR / f"{slug}_contact.jpg"),
        ]
    )


def write_metadata(paths: dict[str, Path]) -> None:
    rows = []
    for short in SHORTS:
        rows.append(
            {
                "upload_order": short.upload_order,
                "file": paths[short.slug].name,
                "source_start": short.start,
                "duration_seconds": short.duration,
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )

    csv_path = META_DIR / "cs2_rank_grind_shorts_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# CS2 Rank Grind Shorts Pack", ""]
    md_lines.extend(
        [
            "- Source: Counter Strike 2 live gameplay",
            "- Style: cropped gameplay, blurred gameplay background, short factual overlays",
            "- Upload rule: under 30 seconds, quick fight/reaction only",
            "",
        ]
    )
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
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
    (META_DIR / "cs2_rank_grind_shorts_metadata.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )


def verify_outputs(ffmpeg: str, paths: dict[str, Path]) -> None:
    for path in paths.values():
        run(
            [
                ffmpeg,
                "-v",
                "error",
                "-i",
                str(path),
                "-f",
                "null",
                "-",
            ]
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CS2 rank-grind Shorts.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local CS2 live gameplay MP4")
    parser.add_argument("--only", nargs="*", help="Optional slugs to render")
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
    paths: dict[str, Path] = {
        short.slug: SHORT_DIR / f"{short.slug}.mp4"
        for short in SHORTS
        if (SHORT_DIR / f"{short.slug}.mp4").exists()
    }

    for short in selected:
        print(f"Rendering CS2 Short: {short.slug}")
        output = render_short(ffmpeg, source, short)
        paths[short.slug] = output
        make_review_assets(ffmpeg, output, short)

    missing = [short.slug for short in SHORTS if short.slug not in paths]
    if missing:
        raise SystemExit(f"Missing rendered shorts: {', '.join(missing)}")

    verify_outputs(ffmpeg, paths)
    write_metadata(paths)
    print(f"Rendered {len(paths)} CS2 Shorts to {SHORT_DIR}")
    print(f"Metadata written to {META_DIR}")
    print(f"Review assets written to {REVIEW_DIR}")


if __name__ == "__main__":
    main()
