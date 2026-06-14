from __future__ import annotations

import argparse
import csv
import json
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


PROJECT = "One Piece Skypiea Arc"
OUTPUT_ROOT = ROOT / "movies" / PROJECT
SHORT_DIR = OUTPUT_ROOT / "shorts_synced_v2"
META_DIR = OUTPUT_ROOT / "metadata_synced_v2"
WORK_DIR = OUTPUT_ROOT / "work_synced_v2"
REVIEW_DIR = OUTPUT_ROOT / "review_synced_v2"
ASS_DIR = WORK_DIR / "ass"
ACCURATE_SEEK_PREROLL = 6.0

SOURCE_FILES = {
    "part1": Path(
        r"D:\movies\One Piece\0153-0195 Skypiea Arc (third major arc)\0153-0157 Skypiea Arc Part 1, Dub.mp4"
    ),
    "part2": Path(
        r"D:\movies\One Piece\0153-0195 Skypiea Arc (third major arc)\0158-0167 Skypiea Arc Part 2, Dub.mp4"
    ),
    "part3": Path(
        r"D:\movies\One Piece\0153-0195 Skypiea Arc (third major arc)\0168-0179 Skypiea Arc Part 3, Dub.mp4"
    ),
    "part4": Path(
        r"D:\movies\One Piece\0153-0195 Skypiea Arc (third major arc)\0180-0186 Skypiea Arc Part 4, Dub.mp4"
    ),
    "part5": Path(
        r"D:\movies\One Piece\0153-0195 Skypiea Arc (third major arc)\0187-0195 Skypiea Arc Part 5, Dub.mp4"
    ),
}

BASE_HASHTAGS = (
    "#onepiece #onepieceanime #skypiea #skypieaarc #luffy #enel #eneru "
    "#strawhats #animeexplained #animeedit #sceneexplained #animecommunity "
    "#scenecypherhq #shorts"
)
BASE_TAGS = (
    "one piece, one piece skypiea, skypiea arc, luffy vs enel, luffy vs eneru, "
    "enel one piece, eneru one piece, golden bell one piece, nico robin poneglyph, "
    "noland one piece, calgara one piece, straw hats, anime explained, one piece explained, "
    "one piece shorts, anime shorts, scene explained, scenecypher hq"
)
DESCRIPTION_SUFFIX = (
    "SceneCypher HQ decodes anime, movie, and series moments through hidden details, "
    "scene logic, and character choices."
)


@dataclass(frozen=True)
class SkypieaShort:
    slug: str
    source_key: str
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
    SkypieaShort(
        slug="01_heavens_gate",
        source_key="part1",
        start="00:17:30.000",
        duration=28.8,
        hook="THEY REACHED\nHEAVEN'S GATE",
        beats=("THE SKY LOOKS\nPEACEFUL", "THE RULES ARE\nALREADY STRANGE"),
        title="Heaven's Gate Changed The Arc | One Piece Skypiea #shorts",
        description_lead="Skypiea starts feeling different the moment Heaven's Gate turns the sky into a place with rules, tolls, and danger.",
        tags=f"{BASE_TAGS}, heavens gate one piece, skypiea entrance, conis one piece",
        pinned_comment="Would you trust Heaven's Gate the first time you saw it?",
        thumbnail_text="HEAVEN'S GATE",
        upload_order=4,
    ),
    SkypieaShort(
        slug="02_sky_island_warning",
        source_key="part1",
        start="00:23:30.000",
        duration=28.8,
        hook="SKYPIEA LOOKED\nTOO PEACEFUL",
        beats=("ANGEL BEACH\nFEELS SAFE", "THAT'S WHY\nIT WORKS"),
        title="Skypiea Looked Too Peaceful | One Piece Explained #shorts",
        description_lead="The arc hides its danger under a bright, calm island, so the first warning lands harder when the crew realizes this place is controlled.",
        tags=f"{BASE_TAGS}, angel beach one piece, sky island one piece, skypiea explained",
        pinned_comment="Is Skypiea's peaceful intro the best misdirection in One Piece?",
        thumbnail_text="TOO PEACEFUL",
        upload_order=8,
    ),
    SkypieaShort(
        slug="03_gods_judgement",
        source_key="part2",
        start="00:15:00.000",
        duration=28.8,
        hook="GOD'S JUDGEMENT\nWAS REAL",
        beats=("ONE BLAST\nCHANGES THE TONE", "ENEL'S FEAR\nSTARTS EARLY"),
        title="God's Judgement Was Real | One Piece Skypiea #shorts",
        description_lead="This is where Skypiea stops feeling like a wonderland and starts feeling like a place where one unseen power can erase anyone.",
        tags=f"{BASE_TAGS}, god's judgement one piece, enel lightning, skypiea lightning",
        pinned_comment="Was this the first moment Enel felt terrifying?",
        thumbnail_text="GOD'S JUDGEMENT",
        upload_order=1,
    ),
    SkypieaShort(
        slug="04_ordeal_trap",
        source_key="part2",
        start="00:47:30.000",
        duration=28.8,
        hook="THE ORDEAL\nWAS A TRAP",
        beats=("THE TEST IS\nNOT RANDOM", "THE PRIESTS KNOW\nTHE TERRAIN"),
        title="The Ordeal Was A Trap | One Piece Skypiea #shorts",
        description_lead="The ordeal works because the crew is not just fighting an enemy. They are fighting a space designed to confuse them.",
        tags=f"{BASE_TAGS}, skypiea ordeal, satori one piece, one piece trial",
        pinned_comment="Which Skypiea ordeal was the most annoying to survive?",
        thumbnail_text="ORDEAL TRAP",
        upload_order=7,
    ),
    SkypieaShort(
        slug="05_enel_was_watching",
        source_key="part2",
        start="02:53:45.000",
        duration=28.8,
        hook="ENEL WAS\nALREADY WATCHING",
        beats=("THE VILLAIN\nSTOPS HIDING", "EVERYONE IS\nON HIS BOARD"),
        title="Enel Was Already Watching | One Piece Explained #shorts",
        description_lead="Enel becomes scarier when he stops feeling distant and starts looking like someone who has been tracking every move from above.",
        tags=f"{BASE_TAGS}, enel reveal, eneru reveal, skypiea villain, mantra one piece",
        pinned_comment="Did Enel feel unbeatable when he finally showed up?",
        thumbnail_text="ENEL WATCHED",
        upload_order=2,
    ),
    SkypieaShort(
        slug="06_robin_found_jaya",
        source_key="part3",
        start="01:13:00.000",
        duration=28.8,
        hook="ROBIN FOUND\nTHE REAL ISLAND",
        beats=("THE RUINS ARE\nNOT DECORATION", "SKYPIEA CONNECTS\nBACK TO JAYA"),
        title="Robin Found The Real Island | One Piece Skypiea #shorts",
        description_lead="Robin's discovery matters because Skypiea is not just a sky adventure. It is a missing piece of Jaya's history.",
        tags=f"{BASE_TAGS}, nico robin skypiea, robin ruins, jaya skypiea, one piece history",
        pinned_comment="Robin scenes quietly carry so much of Skypiea. Agree?",
        thumbnail_text="ROBIN FOUND IT",
        upload_order=5,
    ),
    SkypieaShort(
        slug="07_chopper_stood_alone",
        source_key="part3",
        start="01:15:00.000",
        duration=28.8,
        hook="CHOPPER HAD\nTO STAND ALONE",
        beats=("NO CREW\nTO HIDE BEHIND", "THIS IS HIS\nCOURAGE TEST"),
        title="Chopper Had To Stand Alone | One Piece Skypiea #shorts",
        description_lead="Chopper's Skypiea fight works because the danger is simple: he is scared, alone, and still has to protect the mission.",
        tags=f"{BASE_TAGS}, chopper skypiea, chopper vs gedatsu, one piece chopper fight",
        pinned_comment="Is this one of Chopper's underrated courage moments?",
        thumbnail_text="CHOPPER ALONE",
        upload_order=10,
    ),
    SkypieaShort(
        slug="08_zoro_cut_the_trial",
        source_key="part3",
        start="03:03:00.000",
        duration=28.8,
        hook="ZORO CUT\nTHROUGH THE TRIAL",
        beats=("THE PRIEST USES\nTHE SKY", "ZORO ANSWERS\nWITH PRESSURE"),
        title="Zoro Cut Through The Trial | One Piece Skypiea #shorts",
        description_lead="Zoro's fight turns the floating ruins into a weapon, then flips it back with pure pressure and timing.",
        tags=f"{BASE_TAGS}, zoro skypiea, zoro vs ohm, one piece zoro fight, zoro sword scene",
        pinned_comment="Which Zoro Skypiea moment is your favorite?",
        thumbnail_text="ZORO CUTS",
        upload_order=11,
    ),
    SkypieaShort(
        slug="09_enel_cleared_the_board",
        source_key="part3",
        start="03:36:30.000",
        duration=28.8,
        hook="ENEL CLEARED\nTHE BOARD",
        beats=("THE SURVIVAL GAME\nWAS CONTROL", "HE WANTED FEAR\nBEFORE VICTORY"),
        title="Enel Cleared The Board | One Piece Skypiea #shorts",
        description_lead="Enel's survival game is cruel because he is not chasing a fair fight. He is proving the island belongs to him.",
        tags=f"{BASE_TAGS}, enel survival game, skypiea survival game, enel god complex",
        pinned_comment="Was Enel's survival game his coldest move?",
        thumbnail_text="ENEL'S GAME",
        upload_order=6,
    ),
    SkypieaShort(
        slug="10_reject_dial",
        source_key="part4",
        start="00:18:20.000",
        duration=28.8,
        hook="THE REJECT DIAL\nALMOST ENDED GOD",
        beats=("WYPER BETS\nEVERYTHING", "ENEL STILL\nSTANDS UP"),
        title="The Reject Dial Almost Ended Enel | One Piece #shorts",
        description_lead="Wyper's attack lands because it finally makes Enel look beatable, then the arc twists the knife by letting him rise again.",
        tags=f"{BASE_TAGS}, reject dial one piece, wyper vs enel, enel revival, skypiea fight",
        pinned_comment="Did Wyper deserve more respect for this hit?",
        thumbnail_text="REJECT DIAL",
        upload_order=3,
    ),
    SkypieaShort(
        slug="11_luffy_rubber_reveal",
        source_key="part4",
        start="00:25:00.000",
        duration=28.8,
        hook="LIGHTNING COULDN'T\nTOUCH LUFFY",
        beats=("ENEL'S POWER\nFINALLY BREAKS", "THE ANSWER WAS\nRUBBER"),
        title="Lightning Couldn't Touch Luffy | One Piece Skypiea #shorts",
        description_lead="The rubber reveal is perfect because it turns Enel's godlike power into the one matchup he never prepared for.",
        tags=f"{BASE_TAGS}, luffy rubber, luffy immune to lightning, luffy vs enel, enel shocked",
        pinned_comment="Best natural counter in One Piece?",
        thumbnail_text="RUBBER WINS",
        upload_order=9,
    ),
    SkypieaShort(
        slug="12_ark_maxim_escape",
        source_key="part4",
        start="00:55:00.000",
        duration=28.8,
        hook="ENEL BUILT\nHIS EXIT",
        beats=("ARK MAXIM\nIS NOT A SHIP", "IT IS HIS\nAPOCALYPSE PLAN"),
        title="Enel Built His Exit | One Piece Skypiea Explained #shorts",
        description_lead="Ark Maxim matters because Enel's plan is not just to win. He wants to leave the island after proving nobody can stop him.",
        tags=f"{BASE_TAGS}, ark maxim, enel ark maxim, skypiea maxim, one piece enel plan",
        pinned_comment="Was Ark Maxim one of the coolest villain machines?",
        thumbnail_text="ARK MAXIM",
        upload_order=12,
    ),
    SkypieaShort(
        slug="13_sanji_needed_a_light",
        source_key="part4",
        start="01:23:30.000",
        duration=28.8,
        hook="SANJI ONLY\nNEEDED A LIGHT",
        beats=("HE WAS HURT\nBUT STILL MOVED", "STYLE MEETS\nSACRIFICE"),
        title="Sanji Needed A Light | One Piece Skypiea #shorts",
        description_lead="Sanji's line hits because he turns a brutal hit into a calm flex, and still protects the crew when the ship is falling apart.",
        tags=f"{BASE_TAGS}, sanji skypiea, sanji needed a light, sanji enel, sanji cool moment",
        pinned_comment="Is this Sanji's smoothest pre-timeskip moment?",
        thumbnail_text="SANJI'S LIGHT",
        upload_order=13,
    ),
    SkypieaShort(
        slug="14_gold_ball_counter",
        source_key="part5",
        start="01:46:45.000",
        duration=28.8,
        hook="THE GOLD BALL\nBECAME A WEAPON",
        beats=("ENEL MADE IT\nA PRISON", "LUFFY MADE IT\nTHE COUNTER"),
        title="The Gold Ball Became A Weapon | One Piece Skypiea #shorts",
        description_lead="The final counter works because Luffy turns the thing slowing him down into the exact weight needed to reach Enel.",
        tags=f"{BASE_TAGS}, luffy gold ball, luffy vs enel final, golden rifle one piece",
        pinned_comment="Did the gold ball payoff surprise you?",
        thumbnail_text="GOLD COUNTER",
        upload_order=14,
    ),
    SkypieaShort(
        slug="15_noland_was_right",
        source_key="part5",
        start="01:55:30.000",
        duration=28.8,
        hook="THE LIAR\nWAS RIGHT",
        beats=("NOLAND'S STORY\nWAS NEVER FAKE", "THE BELL CARRIES\nTHE PROOF"),
        title="The Liar Was Right | One Piece Skypiea Explained #shorts",
        description_lead="Skypiea's emotional payoff is that Noland was never lying. The island, the gold, and the bell were waiting in the sky.",
        tags=f"{BASE_TAGS}, noland the liar, mont blanc noland, calgara one piece, skypiea backstory",
        pinned_comment="Noland and Calgara deserved better, didn't they?",
        thumbnail_text="LIAR WAS RIGHT",
        upload_order=15,
    ),
    SkypieaShort(
        slug="16_bell_proved_the_truth",
        source_key="part5",
        start="02:18:30.000",
        duration=28.8,
        hook="THE BELL\nPROVED THE TRUTH",
        beats=("ONE SOUND\nCROSSES HISTORY", "LUFFY ANSWERS\nA 400 YEAR PROMISE"),
        title="The Bell Proved The Truth | One Piece Skypiea #shorts",
        description_lead="The golden bell is not just treasure. It is proof that a promise, a friendship, and a lost island were all real.",
        tags=f"{BASE_TAGS}, golden bell one piece, shandora bell, luffy rings bell, skypiea ending",
        pinned_comment="Did the bell scene make Skypiea worth it?",
        thumbnail_text="THE BELL RANG",
        upload_order=16,
    ),
    SkypieaShort(
        slug="17_robin_hidden_message",
        source_key="part5",
        start="02:20:00.000",
        duration=28.8,
        hook="ROBIN FOUND\nTHE HIDDEN MESSAGE",
        beats=("THE PONEGLYPH\nWASN'T THE END", "ROGER LEFT\nA TRACK"),
        title="Robin Found The Hidden Message | One Piece Skypiea #shorts",
        description_lead="Robin's scene matters because Skypiea quietly connects the Void Century, the Poneglyphs, and Roger's final path.",
        tags=f"{BASE_TAGS}, robin poneglyph, skypiea poneglyph, roger message, void century one piece",
        pinned_comment="Did you catch how important Roger's message was?",
        thumbnail_text="HIDDEN MESSAGE",
        upload_order=17,
    ),
    SkypieaShort(
        slug="18_treasure_too_big",
        source_key="part5",
        start="02:25:00.000",
        duration=28.8,
        hook="THE TREASURE\nWAS TOO BIG",
        beats=("THE CREW THINKS\nTHEY'RE ESCAPING", "SKYPIEA ENDS\nWITH A GIFT"),
        title="The Treasure Was Too Big | One Piece Skypiea #shorts",
        description_lead="The ending is funny because the Straw Hats think they are running from punishment, while the island is literally trying to give them gold.",
        tags=f"{BASE_TAGS}, skypiea treasure, straw hats leave skypiea, one piece funny ending",
        pinned_comment="Would you run too, or stay for the gold?",
        thumbnail_text="TOO MUCH GOLD",
        upload_order=18,
    ),
)


def ensure_dirs() -> None:
    for directory in (SHORT_DIR, META_DIR, WORK_DIR, REVIEW_DIR, ASS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)


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


def source_for(short: SkypieaShort) -> Path:
    source = SOURCE_FILES[short.source_key]
    if not source.exists():
        raise FileNotFoundError(source)
    return source


def write_ass(short: SkypieaShort) -> Path:
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
        "Style: Hook,Arial Black,60,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,6,2,8,58,58,178,1",
        "Style: Beat,Arial Black,42,&H00FFFFFF,&H000000FF,&H00111111,&H99000000,-1,0,0,0,100,100,0,0,1,4,1,5,82,82,0,1",
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
            f"Dialogue: 9,{ass_time(6.2)},{ass_time(10.2)},Beat,,0,0,0,,"
            r"{\fad(100,180)}" + ass_escape(beat_1)
        )
    if beat_2:
        lines.append(
            f"Dialogue: 9,{ass_time(15.2)},{ass_time(19.4)},Beat,,0,0,0,,"
            r"{\fad(100,180)}" + ass_escape(beat_2)
        )
    lines.append(
        f"Dialogue: 7,{ass_time(max(0, short.duration - 4.2))},{ass_time(max(0, short.duration - 0.55))},Lower,,0,0,0,,"
        r"{\fad(120,220)}ONE PIECE / SKYPIEA DECODED"
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_short(ffmpeg: str, short: SkypieaShort) -> Path:
    ass_path = write_ass(short)
    source = source_for(short)
    out_path = SHORT_DIR / f"{short.slug}.mp4"
    fade_out = max(0.0, short.duration - 0.35)
    source_start = parse_timecode(short.start)
    input_seek = max(0.0, source_start - ACCURATE_SEEK_PREROLL)
    trim_seek = source_start - input_seek
    video_filter = (
        "[0:v]setpts=PTS-STARTPTS,split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=24:1,eq=brightness=-0.045:saturation=0.9[bg2];"
        "[fg]scale=1080:-2:flags=lanczos,setsar=1,"
        "eq=contrast=1.05:saturation=1.08,unsharp=5:5:0.35[fg2];"
        "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,"
        "drawbox=x=0:y=0:w=1080:h=1920:color=black@0.08:t=fill,"
        f"fade=t=in:st=0:d=0.14,fade=t=out:st={fade_out:.3f}:d=0.35,"
        f"{subtitle_filter_arg(ass_path)},format=yuv420p"
    )
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{input_seek:.3f}",
        "-i",
        str(source),
        "-ss",
        f"{trim_seek:.3f}",
        "-t",
        f"{short.duration:.3f}",
        "-filter_complex",
        video_filter,
        "-af",
        "aresample=48000:async=1:first_pts=0,asetpts=PTS-STARTPTS,volume=1.03,alimiter=limit=0.96,"
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
        "-avoid_negative_ts",
        "make_zero",
        str(out_path),
    ]
    run(command)
    return out_path


def review_contact(ffmpeg: str, video_path: Path, short: SkypieaShort) -> None:
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


def combined_contact(ffmpeg: str) -> None:
    contact_dir = REVIEW_DIR / "combined_contacts"
    contact_dir.mkdir(parents=True, exist_ok=True)
    for stale in contact_dir.glob("contact_*.jpg"):
        stale.unlink()
    index = 0
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        src = REVIEW_DIR / f"{short.slug}_contact.jpg"
        if src.exists():
            dst = contact_dir / f"contact_{index:03d}.jpg"
            dst.write_bytes(src.read_bytes())
            index += 1
    if index == 0:
        return
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
            str(contact_dir / "contact_%03d.jpg"),
            "-vf",
            f"tile=1x{index}",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(REVIEW_DIR / "all_shorts_contact.jpg"),
        ]
    )


def probe_output(ffprobe: str | None, path: Path) -> dict[str, str]:
    if not ffprobe:
        return {}
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height,r_frame_rate,duration",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ]
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return {
        "codec": stream.get("codec_name", ""),
        "width": str(stream.get("width", "")),
        "height": str(stream.get("height", "")),
        "fps": stream.get("r_frame_rate", ""),
        "duration": data.get("format", {}).get("duration", stream.get("duration", "")),
    }


def write_metadata(paths: dict[str, Path], probes: dict[str, dict[str, str]]) -> None:
    rows = []
    for short in sorted(SHORTS, key=lambda item: item.upload_order):
        source_name = source_for(short).name
        rows.append(
            {
                "upload_order": short.upload_order,
                "slug": short.slug,
                "file": paths[short.slug].name,
                "source_file": source_name,
                "source_start": short.start,
                "duration": f"{short.duration:.1f}",
                "probe_duration": probes.get(short.slug, {}).get("duration", ""),
                "title": short.title,
                "description": f"{short.description_lead} {DESCRIPTION_SUFFIX}",
                "hashtags": BASE_HASHTAGS,
                "tags": short.tags,
                "pinned_comment": short.pinned_comment,
                "thumbnail_text": short.thumbnail_text,
            }
        )
    csv_path = META_DIR / "one_piece_skypiea_scenecypher_metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# One Piece Skypiea Arc SceneCypher Shorts", ""]
    md_lines.extend(
        [
            "Upload note: these are transformed SceneCypher-style explainers with commentary overlays.",
            "No mirror flip is applied.",
            "",
        ]
    )
    for row in rows:
        md_lines.extend(
            [
                f"## {row['file']}",
                f"- Upload order: {row['upload_order']}",
                f"- Source file: {row['source_file']}",
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
    (META_DIR / "one_piece_skypiea_scenecypher_metadata.md").write_text(
        "\n".join(md_lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SceneCypher HQ One Piece Skypiea Shorts.")
    parser.add_argument("--only", nargs="*", default=None, help="Optional slug list to render")
    args = parser.parse_args()

    ensure_dirs()
    for source in SOURCE_FILES.values():
        if not source.exists():
            raise FileNotFoundError(source)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    bundled_ffprobe = Path(ffmpeg).with_name("ffprobe.exe")
    ffprobe = str(bundled_ffprobe) if bundled_ffprobe.exists() else shutil.which("ffprobe")
    selected = [short for short in SHORTS if args.only is None or short.slug in args.only]
    paths = {short.slug: SHORT_DIR / f"{short.slug}.mp4" for short in SHORTS}
    probes: dict[str, dict[str, str]] = {}
    for short in selected:
        print(f"Rendering {short.slug}")
        path = render_short(ffmpeg, short)
        paths[short.slug] = path
        review_contact(ffmpeg, path, short)
        probes[short.slug] = probe_output(ffprobe, path)
    for short in SHORTS:
        path = paths[short.slug]
        if path.exists() and short.slug not in probes:
            probes[short.slug] = probe_output(ffprobe, path)
    combined_contact(ffmpeg)
    write_metadata(paths, probes)
    print(f"Shorts: {SHORT_DIR}")
    print(f"Metadata: {META_DIR}")
    print(f"Review: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
