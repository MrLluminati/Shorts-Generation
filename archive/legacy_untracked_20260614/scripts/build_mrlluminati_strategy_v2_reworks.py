from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\abhik\Documents\Short Creation")
PIPELINE = ROOT / "live_video_pipeline"
FFMPEG = Path(r"C:\Users\abhik\AppData\Local\CapCut\Apps\7.6.0.3123\ffmpeg.exe")
PY_DATE = "20260614"

SHORT_ROOT = PIPELINE / "short_form"
META_ROOT = PIPELINE / "metadata"
WORK_ROOT = PIPELINE / "work"
REVIEW_ROOT = PIPELINE / "review"

CS2_RAW = Path(r"C:\Users\abhik\Videos\2026-06-11_19-23-39.mp4")
FIRST_LIGHT_0609_RAW = Path(r"C:\Users\abhik\Videos\2026-06-09_14-17-59.mp4")
FIRST_LIGHT_0611_RAW = Path(r"C:\Users\abhik\Videos\2026-06-11_23-02-51.mp4")

GTA_MONEY_OLD = SHORT_ROOT / "gta_v_grand_rp_money_grind"
GTA_DRIVING_OLD = SHORT_ROOT / "gta_v_grand_rp_driving_batch"
GTA_BATCH2_OLD = SHORT_ROOT / "gta_v_grand_rp_batch_02"


@dataclass(frozen=True)
class Segment:
    source: Path
    start: float
    duration: float
    label: str
    source_note: str = "Raw recording"
    crop_center_gameplay: bool = False
    echo_fix: bool = False


@dataclass(frozen=True)
class ShortSpec:
    batch: str
    game: str
    topic: str
    hook: str
    payoff: str
    title: str
    alternatives: tuple[str, str, str, str, str]
    description: str
    short_description: str
    tags: tuple[str, ...]
    targeted_hashtags: tuple[str, ...]
    recommended_hashtags: tuple[str, ...]
    hook_options: tuple[str, str, str, str, str]
    pinned_comment: str
    selection_reason: str
    first_second_reason: str
    music_style: str
    content_type: str
    segments: tuple[Segment, ...]

    @property
    def filename_stem(self) -> str:
        return f"short_{PY_DATE}_{self.game}_{self.topic}_v2"

    @property
    def duration(self) -> float:
        return sum(segment.duration for segment in self.segments)


def old_short(batch_dir: Path, name: str) -> Path:
    return batch_dir / name


SKULL = "\U0001F480"
FIRE = "\U0001F525"

SPECS: tuple[ShortSpec, ...] = (
    ShortSpec(
        batch="cs2_strategy_v2_20260614",
        game="cs2",
        topic="peeked_wrong_time",
        hook="THEY PEEKED\nONE BY ONE",
        payoff="FAST FRAGS ONLY",
        title=f"They Peeked One By One {SKULL} | CS2 #Shorts",
        alternatives=(
            f"He Peeked at the Wrong Time {SKULL} | CS2",
            f"CS2 Timing Was Illegal {SKULL}",
            f"They Pushed One By One {SKULL} | CS2",
            f"I Was Already Waiting {SKULL} | CS2",
            f"Fast Frags Only {FIRE} | CS2",
        ),
        description=(
            "Fast CS2 kill moments trimmed for the Shorts feed: quick peeks, clean timing, "
            "and no dead setup. More CS2 clips on MrLluminati Gaming.\n\n"
            "#CS2 #CS2Shorts #FragMontage #GamingShorts #MrLluminatiGaming"
        ),
        short_description="Quick CS2 kill moments with fast peeks and clean timing.",
        tags=(
            "cs2",
            "counter strike 2",
            "cs2 shorts",
            "cs2 kill montage",
            "counter strike 2 shorts",
            "gaming shorts",
            "fps montage",
            "mrlluminati gaming",
        ),
        targeted_hashtags=("#CS2", "#CounterStrike2", "#CS2Shorts", "#FragMontage", "#FPSGaming", "#GamingShorts"),
        recommended_hashtags=("#CS2", "#CS2Shorts", "#FragMontage", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=(
            "THEY PEEKED ONE BY ONE",
            "HE PEEKED TOO LATE",
            "I WAS ALREADY WAITING",
            "FAST FRAGS ONLY",
            "THAT TIMING WAS ILLEGAL",
        ),
        pinned_comment="Which peek was the cleanest?",
        selection_reason="Replaces the 32s kill montage with only the clearest readable kill beats.",
        first_second_reason="The first frame already shows an enemy in the doorway with the hook promising repeated peeks.",
        music_style="No baked music; add aggressive phonk or FPS montage audio in YouTube Shorts if desired.",
        content_type="Clean aim / montage",
        segments=(
            Segment(CS2_RAW, 225.05, 2.75, "Doorway spray"),
            Segment(CS2_RAW, 428.35, 2.65, "Lane pick"),
            Segment(CS2_RAW, 514.00, 2.55, "Box spray"),
            Segment(CS2_RAW, 780.45, 2.85, "Point blank"),
            Segment(CS2_RAW, 795.40, 2.90, "Rush stopped"),
        ),
    ),
    ShortSpec(
        batch="cs2_strategy_v2_20260614",
        game="cs2",
        topic="solo_queue_pain",
        hook="SOLO QUEUE\nIS PAIN",
        payoff="INSTANT PUNISH",
        title=f"Solo Queue Is Pain {SKULL} | CS2 #Shorts",
        alternatives=(
            f"CS2 Solo Queue Moment {SKULL}",
            f"I Died Too Fast {SKULL} | CS2",
            f"Bad Peek, Instant Punish {SKULL}",
            f"No Space to Breathe {SKULL} | CS2",
            "CS2 Timing Hurt Me",
        ),
        description=(
            "CS2 solo queue pain cut down to the fastest fail moments: bad peeks, instant punishment, "
            "and zero time to react. More CS2 clips on MrLluminati Gaming.\n\n"
            "#CS2 #SoloQueue #CS2Shorts #GamingShorts #MrLluminatiGaming"
        ),
        short_description="Fast CS2 solo queue fail moments with no slow setup.",
        tags=(
            "cs2",
            "counter strike 2",
            "cs2 funny moments",
            "cs2 fails",
            "solo queue",
            "counter strike shorts",
            "fps shorts",
            "mrlluminati gaming",
        ),
        targeted_hashtags=("#CS2", "#SoloQueue", "#CS2Fails", "#CS2Shorts", "#FPSGaming", "#GamingShorts"),
        recommended_hashtags=("#CS2", "#SoloQueue", "#CS2Fails", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=(
            "SOLO QUEUE IS PAIN",
            "BAD PEEK INSTANT PUNISH",
            "I DIED TOO FAST",
            "NO SPACE TO BREATHE",
            "CS2 HUMBLED ME",
        ),
        pinned_comment="Which death was the most painful?",
        selection_reason="Replaces the 24s death montage with only the fastest fail/payoff beats.",
        first_second_reason="The hook tells viewers this is a relatable CS2 fail before the first punish lands.",
        music_style="No baked music; use funny suspense or meme audio in YouTube Shorts.",
        content_type="Funny / fail",
        segments=(
            Segment(CS2_RAW, 47.75, 2.20, "Bad peek"),
            Segment(CS2_RAW, 294.20, 2.30, "Too close"),
            Segment(CS2_RAW, 589.15, 2.15, "Instant punish"),
            Segment(CS2_RAW, 729.45, 1.95, "Wrong angle"),
            Segment(CS2_RAW, 878.10, 2.45, "Open target"),
        ),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="rooftop_landing",
        hook="THIS LANDING\nGOT TIGHT",
        payoff="TOO CLOSE",
        title=f"This Landing Got Tight {SKULL} | GTA RP #Shorts",
        alternatives=(
            "GTA RP Landing Was Too Close",
            f"Almost Missed the Rooftop {SKULL} | GTA RP",
            "Clean Rooftop Landing | GTA RP",
            "This Helicopter Landing Got Risky",
            "GTA RP Chopper Landing Moment",
        ),
        description=(
            "A tight GTA RP helicopter landing trimmed straight to the risky part. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A tight GTA RP helicopter landing with no slow setup.",
        tags=("gta rp", "gta 5", "grand rp", "gta helicopter", "gta landing", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAHelicopter", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("THIS LANDING GOT TIGHT", "TOO CLOSE", "CLEAN LANDING?", "CHOPPER GOT RISKY", "ROOFTOP MOMENT"),
        pinned_comment="Clean landing or too risky?",
        selection_reason="The old GTA raw file is missing, so this v2 uses the old local rooftop Short and trims to the landing payoff.",
        first_second_reason="The hook creates immediate risk around the chopper landing instead of labeling the clip generically.",
        music_style="No baked music; add chill phonk or suspense audio in Shorts.",
        content_type="Cinematic / driving",
        segments=(Segment(old_short(GTA_MONEY_OLD, "03_rooftop_landing.mp4"), 4.0, 14.5, "Old output 00:04.0-00:18.5; original script raw approx 00:41:42-00:41:56.5", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="mountain_money_run",
        hook="LOW FLYING\nWAS RISKY",
        payoff="MOUNTAIN RUN",
        title=f"Low Flying Was Risky {SKULL} | GTA RP #Shorts",
        alternatives=(
            "GTA RP Mountain Flight Got Risky",
            "Flying Low in Grand RP",
            f"This Mountain Run Was Close {SKULL}",
            "GTA RP Helicopter Money Run",
            "Grand RP Chopper Run",
        ),
        description=(
            "A GTA RP helicopter money run trimmed to the risky mountain-flight section. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #GTAHelicopter #MrLluminatiGaming"
        ),
        short_description="A risky low helicopter run across the GTA RP mountains.",
        tags=("gta rp", "grand rp", "gta helicopter", "gta mountain flight", "gta money grind", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAHelicopter", "#GamingClips", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAHelicopter", "#MrLluminatiGaming"),
        hook_options=("LOW FLYING WAS RISKY", "MOUNTAIN RUN", "TOO LOW?", "CHOPPER MONEY RUN", "GRAND RP FLIGHT"),
        pinned_comment="Would you fly this low or play it safe?",
        selection_reason="Uses the strongest movement from the old mountain money run instead of the full 29s route.",
        first_second_reason="The viewer instantly knows this is about risky flying, not a slow travel clip.",
        music_style="No baked music; add chill phonk or flight/suspense audio in Shorts.",
        content_type="Cinematic / driving",
        segments=(Segment(old_short(GTA_MONEY_OLD, "02_mountain_money_run.mp4"), 3.0, 14.0, "Old output 00:03.0-00:17.0; original script raw approx 00:28:58-00:29:12", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="air_taxi_takeoff",
        hook="AIR TAXI\nTOOK OFF",
        payoff="CITY RUN",
        title="Air Taxi Took Off | GTA RP #Shorts",
        alternatives=(
            "GTA RP Air Taxi Run",
            "Grand RP Chopper Takeoff",
            "The Air Taxi Started Fast",
            "GTA RP City Flight",
            "Helicopter Job Took Off | GTA RP",
        ),
        description=(
            "A short GTA RP air taxi takeoff cut straight to the movement. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #GTAHelicopter #MrLluminatiGaming"
        ),
        short_description="A quick GTA RP air taxi takeoff and city run.",
        tags=("gta rp", "grand rp", "gta helicopter", "gta air taxi", "gta city flight", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAHelicopter", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("AIR TAXI TOOK OFF", "CITY RUN", "CHOPPER JOB STARTED", "GRAND RP FLIGHT", "FAST TAKEOFF"),
        pinned_comment="Would you use air taxi in GTA RP?",
        selection_reason="The old 31s takeoff is reduced to the takeoff/movement only.",
        first_second_reason="The hook makes the roleplay action immediately clear.",
        music_style="No baked music; add chill phonk or city-flight audio in Shorts.",
        content_type="Cinematic / driving",
        segments=(Segment(old_short(GTA_MONEY_OLD, "06_air_taxi_takeoff.mp4"), 1.0, 14.5, "Old output 00:01.0-00:15.5; original script raw approx 01:22:19-01:22:33.5", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="tunnel_speed_run",
        hook="TUNNEL SPEED\nGOT WILD",
        payoff="NO SLOWDOWN",
        title=f"Tunnel Speed Got Wild {SKULL} | GTA RP #Shorts",
        alternatives=(
            "GTA RP Tunnel Run Went Fast",
            "No Slowdown in the Tunnel",
            f"This Tunnel Run Was Risky {SKULL}",
            "Grand RP Speed Run Moment",
            "GTA Driving Got Tight",
        ),
        description=(
            "A GTA RP tunnel speed run trimmed down to the fast part only. "
            "More driving clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GTADriving #GrandRP #MrLluminatiGaming"
        ),
        short_description="A fast GTA RP tunnel driving moment.",
        tags=("gta rp", "gta driving", "gta tunnel", "grand rp", "gta cars", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GrandRP", "#GamingClips", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GrandRP", "#MrLluminatiGaming"),
        hook_options=("TUNNEL SPEED GOT WILD", "NO SLOWDOWN", "TOO FAST?", "GTA DRIVING MOMENT", "TUNNEL RUN"),
        pinned_comment="Would you slow down in the tunnel?",
        selection_reason="Keeps the fast tunnel-driving payoff from the old 45s driving Short.",
        first_second_reason="Speed/risk is clear before the road stretch begins.",
        music_style="No baked music; add phonk or driving audio in Shorts.",
        content_type="Driving",
        segments=(Segment(old_short(GTA_DRIVING_OLD, "02_tunnel_speed_run.mp4"), 6.0, 15.0, "Old output 00:06.0-00:21.0; original script raw approx 00:05:36-00:05:51", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="rural_road_flip",
        hook="ALMOST FLIPPED\nBUT SAVED IT",
        payoff="PURE LUCK",
        title=f"Almost Flipped but Saved It {SKULL} | GTA RP #Shorts",
        alternatives=(
            "GTA RP Almost Flipped",
            "Saved the Car Somehow | GTA RP",
            f"That Turn Was Too Close {SKULL}",
            "Grand RP Driving Fail Almost Happened",
            "GTA RP Rural Road Save",
        ),
        description=(
            "A GTA RP rural-road near flip cut down to the important save. "
            "More driving chaos on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GTADriving #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A near flip on a GTA RP rural road, trimmed fast.",
        tags=("gta rp", "gta near flip", "gta driving fail", "grand rp", "gta car save", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GrandRP", "#GamingFails", "#GamingShorts"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("ALMOST FLIPPED BUT SAVED IT", "PURE LUCK", "TOO CLOSE", "RURAL ROAD CHAOS", "CAR SURVIVED"),
        pinned_comment="Skill save or pure luck?",
        selection_reason="This is the strongest GTA driving conflict because it has a clear danger/payoff.",
        first_second_reason="The hook promises a near crash immediately, so viewers know what to watch for.",
        music_style="No baked music; add funny hit or driving suspense audio in Shorts.",
        content_type="Funny / driving",
        segments=(Segment(old_short(GTA_DRIVING_OLD, "09_rural_road_flip.mp4"), 2.0, 15.0, "Old output 00:02.0-00:17.0; original script raw approx 01:44:12-01:44:27", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="city_lanes_tight",
        hook="CITY LANES\nGOT TIGHT",
        payoff="CLOSE CONTROL",
        title="City Lanes Got Tight | GTA RP #Shorts",
        alternatives=(
            "GTA RP Tight City Driving",
            "Clean Control in City Lanes",
            "Grand RP City Lane Cut",
            "GTA Driving Got Close",
            "Tight Lanes in GTA RP",
        ),
        description=(
            "A GTA RP city-lane driving moment cut to the tightest movement. "
            "More driving clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GTADriving #GrandRP #MrLluminatiGaming"
        ),
        short_description="A tight GTA RP city-lane driving cut.",
        tags=("gta rp", "gta driving", "gta city driving", "grand rp", "gta tight lanes", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GrandRP", "#GamingClips", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GTADriving", "#GrandRP", "#MrLluminatiGaming"),
        hook_options=("CITY LANES GOT TIGHT", "CLOSE CONTROL", "TOO CLOSE?", "GTA CITY RUN", "TIGHT LANES"),
        pinned_comment="Would you call this clean control?",
        selection_reason="Turns the old 55s city drive into a single tight-lane driving beat.",
        first_second_reason="The hook frames the clip as a close-control moment, not generic cruising.",
        music_style="No baked music; add chill phonk or driving beat in Shorts.",
        content_type="Driving",
        segments=(Segment(old_short(GTA_DRIVING_OLD, "07_city_lane_cut.mp4"), 10.0, 15.0, "Old output 00:10.0-00:25.0; original script raw approx 00:58:15-00:58:30", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="runway_checkpoint",
        hook="RUNWAY CHECKPOINT\nGOT TIGHT",
        payoff="LAND IT",
        title="Runway Checkpoint Got Tight | GTA RP #Shorts",
        alternatives=(
            "GTA RP Plane Landing Got Tight",
            "Grand RP Runway Checkpoint",
            "This Plane Checkpoint Was Close",
            "GTA RP Pilot Job Moment",
            "Runway Landing in Grand RP",
        ),
        description=(
            "A GTA RP plane-job runway checkpoint trimmed to the landing pressure. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #GTAPlane #MrLluminatiGaming"
        ),
        short_description="A tight runway checkpoint from a GTA RP plane job.",
        tags=("gta rp", "gta plane", "grand rp", "gta runway landing", "gta pilot job", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAPlane", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAPlane", "#MrLluminatiGaming"),
        hook_options=("RUNWAY CHECKPOINT GOT TIGHT", "LAND IT", "TOO CLOSE?", "PLANE JOB MOMENT", "RUNWAY PRESSURE"),
        pinned_comment="Clean landing or too close to the checkpoint?",
        selection_reason="Keeps the runway/landing pressure from the old 48s plane job Short.",
        first_second_reason="The hook gives the viewer a simple landing-pressure story immediately.",
        music_style="No baked music; add suspense or flight audio in Shorts.",
        content_type="Cinematic / driving",
        segments=(Segment(old_short(GTA_BATCH2_OLD, "05_runway_checkpoint_landing.mp4"), 15.0, 15.0, "Old output 00:15.0-00:30.0; original script raw approx 00:52:43-00:52:58", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="black_car_pullup",
        hook="THIS RP PULLUP\nFELT SUSPICIOUS",
        payoff="BLACK CAR",
        title=f"This RP Pullup Felt Suspicious {SKULL} | GTA RP #Shorts",
        alternatives=(
            "GTA RP Pullup Felt Suspicious",
            "Black Car RP Pullup | GTA RP",
            "This Meeting Felt Suspicious",
            "Grand RP Black Car Moment",
            "GTA RP Randoms Are Wild",
        ),
        description=(
            "A suspicious GTA RP black-car pullup trimmed into a short roleplay moment. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #Roleplay #MrLluminatiGaming"
        ),
        short_description="A suspicious black-car pullup from GTA RP.",
        tags=("gta rp", "grand rp", "gta roleplay", "gta black car", "gta rp meetup", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#Roleplay", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#Roleplay", "#MrLluminatiGaming"),
        hook_options=("THIS RP PULLUP FELT SUSPICIOUS", "BLACK CAR", "SUSPICIOUS MEETING", "RP MOMENT", "RANDOMS ARE WILD"),
        pinned_comment="Would you stay there or leave?",
        selection_reason="Reframes the old 50s pullup as a short suspicious RP moment.",
        first_second_reason="The hook creates curiosity around the car/meeting immediately.",
        music_style="No baked music; add dark luxury or suspense audio in Shorts.",
        content_type="RP / cinematic",
        segments=(Segment(old_short(GTA_BATCH2_OLD, "06_black_car_rp_pullup.mp4"), 3.0, 14.5, "Old output 00:03.0-00:17.5; original script raw approx 00:29:58-00:30:12.5", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="gta_strategy_v2_20260614",
        game="gta",
        topic="night_plane_takeoff",
        hook="NIGHT PLANE\nTOOK OFF",
        payoff="CITY LIGHTS",
        title="Night Plane Took Off | GTA RP #Shorts",
        alternatives=(
            "GTA RP Night Plane Run",
            "Grand RP Plane Takeoff",
            "Night Flying in GTA RP",
            "GTA RP Airport Takeoff",
            "City Lights Plane Run",
        ),
        description=(
            "A GTA RP night plane takeoff trimmed to the clean flight moment. "
            "More Grand RP clips on MrLluminati Gaming.\n\n"
            "#GTARP #GTA5 #GrandRP #GTAPlane #MrLluminatiGaming"
        ),
        short_description="A short GTA RP night plane takeoff.",
        tags=("gta rp", "grand rp", "gta plane", "gta night flight", "gta airport", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAPlane", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#GTARP", "#GTA5", "#GrandRP", "#GTAPlane", "#MrLluminatiGaming"),
        hook_options=("NIGHT PLANE TOOK OFF", "CITY LIGHTS", "PLANE JOB STARTED", "NIGHT FLYING", "TAKEOFF MOMENT"),
        pinned_comment="Night flying or daytime flying?",
        selection_reason="Cuts the old 55s plane run down to one takeoff/flyover beat.",
        first_second_reason="The hook tells viewers to watch the takeoff and city-light payoff.",
        music_style="No baked music; add cinematic/chill flight audio in Shorts.",
        content_type="Cinematic / driving",
        segments=(Segment(old_short(GTA_BATCH2_OLD, "11_night_plane_takeoff.mp4"), 5.0, 15.0, "Old output 00:05.0-00:20.0; original script raw approx 03:00:05-03:00:20", "Fallback from old local Short because raw GTA file is missing", True),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="warzone_shore",
        hook="BOND WOKE UP\nIN FIRE",
        payoff="MOVE FAST",
        title=f"Bond Woke Up in Fire {SKULL} | 007 First Light #Shorts",
        alternatives=(
            "007 First Light Starts in Fire",
            "Bond Woke Up in a Warzone",
            "This 007 Opening Was Chaos",
            "007 First Light Fire Scene",
            "Bond Had to Move Fast",
        ),
        description=(
            "A short 007 First Light opening moment cut straight to the burning-shore chaos. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="Bond wakes up in a burning 007 First Light opening moment.",
        tags=("007 first light", "james bond game", "007 gameplay", "bond game", "gaming shorts", "hindi gaming", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#007Game", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("BOND WOKE UP IN FIRE", "MOVE FAST", "WARZONE SHORE", "007 OPENING CHAOS", "THE MISSION STARTED"),
        pinned_comment="Strong opening or too slow for Shorts?",
        selection_reason="Reworks the 58s opening shore Short into a quick fire/chaos story beat.",
        first_second_reason="The burning shore plus hook gives instant danger/context.",
        music_style="No baked music; add spy-action or cinematic tension audio in Shorts.",
        content_type="Cinematic / action",
        segments=(Segment(FIRST_LIGHT_0609_RAW, 248.0, 14.0, "Raw approx 00:04:08-00:04:22"),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="room_not_empty",
        hook="THE ROOM\nWAS NOT EMPTY",
        payoff="STAY READY",
        title=f"The Room Was Not Empty {SKULL} | 007 First Light #Shorts",
        alternatives=(
            "Bond Found Something Inside",
            "007 Room Search Got Tense",
            "The Room Was Not Empty | 007",
            "Bond Had to Stay Ready",
            "007 First Light Tense Room",
        ),
        description=(
            "A tense 007 First Light room-search moment trimmed for a faster Shorts payoff. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A tense room-search moment from 007 First Light.",
        tags=("007 first light", "james bond game", "bond stealth", "007 gameplay", "story game", "gaming shorts", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#StealthGame", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("THE ROOM WAS NOT EMPTY", "STAY READY", "BOND FOUND SOMETHING", "TENSE ROOM", "NOT EMPTY"),
        pinned_comment="Stealth moments or action moments: which should I post more?",
        selection_reason="Reworks a 58s hidden-room Short into one tense curiosity beat.",
        first_second_reason="The hook creates immediate mystery without over-explaining.",
        music_style="No baked music; add spy tension or suspense audio in Shorts.",
        content_type="Cinematic / story moment",
        segments=(Segment(FIRST_LIGHT_0609_RAW, 1416.0, 15.0, "Raw approx 00:23:36-00:23:51"),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="ambush_hit_fast",
        hook="THE AMBUSH\nHIT FAST",
        payoff="NO WARNING",
        title=f"The Ambush Hit Fast {SKULL} | 007 First Light #Shorts",
        alternatives=(
            "Bond Got Ambushed Fast",
            "007 Ambush Came Out of Nowhere",
            "No Warning in 007 First Light",
            "Bond Reacted Fast",
            "007 First Light Action Moment",
        ),
        description=(
            "A quick 007 First Light ambush moment cut straight to the action. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A fast ambush moment from 007 First Light.",
        tags=("007 first light", "james bond game", "007 ambush", "bond action", "gaming shorts", "hindi gaming", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#ActionGaming", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("THE AMBUSH HIT FAST", "NO WARNING", "BOND REACTED FAST", "ACTION STARTED", "AMBUSH MOMENT"),
        pinned_comment="Was this the best action moment from the opening mission?",
        selection_reason="Reworks the 58s ambush Short into a fast action-first cut.",
        first_second_reason="The hook and immediate danger tell viewers exactly why to stay.",
        music_style="No baked music; add spy-action/trailer audio in Shorts.",
        content_type="Action",
        segments=(Segment(FIRST_LIGHT_0609_RAW, 2068.0, 16.0, "Raw approx 00:34:28-00:34:44"),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="first_shootout",
        hook="BOND REACTED\nINSTANTLY",
        payoff="FIRST SHOOTOUT",
        title=f"Bond Reacted Instantly {FIRE} | 007 First Light #Shorts",
        alternatives=(
            "First Shootout Hit Fast | 007",
            "Bond Took the Shot Fast",
            "007 Quick Reaction Moment",
            "Enemy Never Saw Bond Coming",
            "Fastest 007 Shootout",
        ),
        description=(
            "A fast 007 First Light shootout moment with rough recording audio cleaned as much as possible. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A fast first-shootout moment from 007 First Light.",
        tags=("007 first light", "james bond game", "007 shootout", "bond action", "gaming shorts", "hindi gaming", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#ActionGaming", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("BOND REACTED INSTANTLY", "FIRST SHOOTOUT", "FAST TAKEDOWN", "TOOK THE SHOT", "ACTION HIT FAST"),
        pinned_comment="Clean aim or pure panic?",
        selection_reason="Already short, but repackaged with a stronger first-second hook and v2 metadata.",
        first_second_reason="The hook says reaction/action immediately, matching the shootout.",
        music_style="No baked music; add spy-action beat in Shorts. Audio has echo reduction applied.",
        content_type="Action",
        segments=(Segment(FIRST_LIGHT_0611_RAW, 1075.5, 11.5, "Raw approx 00:17:55.5-00:18:07", echo_fix=True),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="rooftop_takedown",
        hook="ROOFTOP GUARD\nWENT DOWN",
        payoff="CLEAN STEALTH",
        title=f"Rooftop Guard Went Down {SKULL} | 007 First Light #Shorts",
        alternatives=(
            "007 Rooftop Takedown",
            "Bond Cleared Him Fast",
            "Clean Stealth Takedown | 007",
            "Enemy Never Saw Bond Coming",
            "Rooftop Stealth Moment | 007",
        ),
        description=(
            "A clean rooftop takedown from 007 First Light, trimmed for a faster Shorts payoff. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A clean rooftop takedown from 007 First Light.",
        tags=("007 first light", "james bond game", "007 takedown", "bond stealth", "gaming shorts", "hindi gaming", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#StealthGame", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("ROOFTOP GUARD WENT DOWN", "CLEAN STEALTH", "BOND CLEARED HIM", "FAST TAKEDOWN", "NO ONE SAW IT"),
        pinned_comment="Stealth takedown or loud action: which is better?",
        selection_reason="Keeps the cleanest stealth payoff from the night mission.",
        first_second_reason="The hook gives a clear takedown promise before the scene plays.",
        music_style="No baked music; add stealth/spy audio in Shorts. Audio has echo reduction applied.",
        content_type="Action / stealth",
        segments=(Segment(FIRST_LIGHT_0611_RAW, 4569.0, 15.0, "Raw approx 01:16:09-01:16:24", echo_fix=True),),
    ),
    ShortSpec(
        batch="007_strategy_v2_20260614",
        game="007",
        topic="corridor_fight",
        hook="NO TIME\nTO RELOAD",
        payoff="PUSH THROUGH",
        title=f"No Time to Reload {SKULL} | 007 First Light #Shorts",
        alternatives=(
            "Corridor Fight Started Fast | 007",
            "Bond Had to Push Through",
            "007 Corridor Fight Moment",
            "Fast 007 Gunfight",
            "Bond Had No Time",
        ),
        description=(
            "A quick 007 First Light corridor fight trimmed to the action and payoff. "
            "More 007 Hindi gameplay on MrLluminati Gaming.\n\n"
            "#007FirstLight #JamesBond #BondGame #GamingShorts #MrLluminatiGaming"
        ),
        short_description="A fast corridor fight from 007 First Light.",
        tags=("007 first light", "james bond game", "007 gunfight", "bond action", "gaming shorts", "hindi gaming", "mrlluminati gaming"),
        targeted_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#ActionGaming", "#GamingShorts", "#HindiGaming"),
        recommended_hashtags=("#007FirstLight", "#JamesBond", "#BondGame", "#GamingShorts", "#MrLluminatiGaming"),
        hook_options=("NO TIME TO RELOAD", "PUSH THROUGH", "CORRIDOR FIGHT", "FAST GUNFIGHT", "BOND HAD NO TIME"),
        pinned_comment="Would you push here or reload first?",
        selection_reason="Uses a compact action section from the existing 007 night-mission recording.",
        first_second_reason="The hook creates urgency before the gunfight begins.",
        music_style="No baked music; add fast spy-action audio in Shorts. Audio has echo reduction applied.",
        content_type="Action",
        segments=(Segment(FIRST_LIGHT_0611_RAW, 3928.0, 14.0, "Raw approx 01:05:28-01:05:42", echo_fix=True),),
    ),
)


def run(cmd: list[str | Path]) -> subprocess.CompletedProcess[str]:
    printable = " ".join(str(part) for part in cmd)
    print(printable)
    result = subprocess.run(
        [str(part) for part in cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode:
        print(result.stdout)
        result.check_returncode()
    return result


def ensure_dirs() -> None:
    batches = {spec.batch for spec in SPECS}
    for batch in batches:
        for root in (SHORT_ROOT, META_ROOT, WORK_ROOT, REVIEW_ROOT):
            (root / batch).mkdir(parents=True, exist_ok=True)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def text_size(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont, stroke_width: int) -> tuple[int, int]:
    lines = text.split("\n")
    widths = []
    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=text_font, stroke_width=stroke_width)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    return max(widths), sum(heights) + 8 * (len(lines) - 1)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, min_size: int = 34) -> ImageFont.FreeTypeFont:
    size = start_size
    while size >= min_size:
        candidate = font(size)
        width, _ = text_size(draw, text, candidate, 6)
        if width <= max_width:
            return candidate
        size -= 2
    return font(min_size)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    stroke_width: int = 6,
    line_spacing: int = 8,
) -> None:
    x, y = xy
    lines = text.split("\n")
    widths = []
    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=text_font, stroke_width=stroke_width)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    total_h = sum(heights) + line_spacing * (len(lines) - 1)
    cy = y - total_h // 2
    for line, width, height in zip(lines, widths, heights):
        draw.text(
            (x - width // 2, cy),
            line,
            font=text_font,
            fill=fill,
            stroke_fill=(0, 0, 0, 235),
            stroke_width=stroke_width,
        )
        cy += height + line_spacing


def make_overlay(spec: ShortSpec) -> Path:
    path = WORK_ROOT / spec.batch / f"{spec.filename_stem}_overlay.png"
    image = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    red = (232, 42, 47, 245)
    white = (255, 255, 255, 255)
    amber = (255, 210, 77, 255)
    panel = (0, 0, 0, 158)

    draw.rounded_rectangle((82, 64, 998, 164), radius=30, fill=panel, outline=red, width=3)
    centered_text(draw, (540, 104), "MRLLUMINATI GAMING", font(31), white, stroke_width=3)

    hook_font = fit_font(draw, spec.hook, 940, 86)
    centered_text(draw, (540, 290), spec.hook, hook_font, white, stroke_width=8, line_spacing=2)

    draw.rounded_rectangle((86, 1470, 994, 1610), radius=34, fill=panel, outline=red, width=4)
    payoff_font = fit_font(draw, spec.payoff, 820, 56)
    centered_text(draw, (540, 1530), spec.payoff, payoff_font, amber, stroke_width=5)

    centered_text(draw, (540, 1752), f"{spec.game.upper()} SHORTS V2", font(38), white, stroke_width=4)
    image.save(path)
    return path


def audio_filter(segment: Segment, duration: float) -> str:
    fade_out = max(0.1, duration - 0.28)
    if segment.echo_fix:
        return (
            "[0:a]aresample=48000,asplit=2[dry][echo];"
            "[echo]adelay=38|38,volume=-0.45[cancel];"
            "[dry][cancel]amix=inputs=2:normalize=0,highpass=f=55,"
            "acompressor=threshold=-18dB:ratio=2.2:attack=8:release=120,"
            f"volume=1.12,alimiter=limit=0.97,afade=t=in:st=0:d=0.06,afade=t=out:st={fade_out:.3f}:d=0.26[a]"
        )
    return (
        "[0:a]aresample=48000,highpass=f=65,acompressor=threshold=-18dB:ratio=2.4:attack=6:release=105,"
        f"volume=1.10,alimiter=limit=0.96,afade=t=in:st=0:d=0.06,afade=t=out:st={fade_out:.3f}:d=0.26[a]"
    )


def video_filter(segment: Segment, overlay: Path) -> str:
    source = "[0:v]crop=1080:608:0:656,split=2[bg][fg];" if segment.crop_center_gameplay else "[0:v]split=2[bg][fg];"
    return (
        source +
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=22,hue=s=0.74[bgv];"
        "[fg]scale=1080:1920:force_original_aspect_ratio=decrease,hue=s=1.08,unsharp=5:5:0.62:3:3:0.22[fgv];"
        "[bgv][fgv]overlay=(W-w)/2:(H-h)/2[base];"
        "[base][1:v]overlay=0:0,format=yuv420p,setsar=1,fps=60[v];"
    )


def render_segment(spec: ShortSpec, segment: Segment, index: int, overlay: Path) -> Path:
    out = WORK_ROOT / spec.batch / f"{spec.filename_stem}_segment_{index:02d}.mp4"
    filters = video_filter(segment, overlay) + audio_filter(segment, segment.duration)
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-ss",
            f"{segment.start:.3f}",
            "-t",
            f"{segment.duration:.3f}",
            "-i",
            segment.source,
            "-loop",
            "1",
            "-t",
            f"{segment.duration:.3f}",
            "-i",
            overlay,
            "-filter_complex",
            filters,
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


def concat_segments(spec: ShortSpec, parts: list[Path]) -> Path:
    output = SHORT_ROOT / spec.batch / f"{spec.filename_stem}.mp4"
    if len(parts) == 1:
        run([FFMPEG, "-y", "-hide_banner", "-i", parts[0], "-c", "copy", "-movflags", "+faststart", output])
        return output
    concat_file = WORK_ROOT / spec.batch / f"{spec.filename_stem}_concat.txt"
    concat_file.write_text("\n".join(f"file '{path.as_posix()}'" for path in parts), encoding="utf-8")
    run([FFMPEG, "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", "-movflags", "+faststart", output])
    return output


def review(spec: ShortSpec, output: Path) -> None:
    review_dir = REVIEW_ROOT / spec.batch / spec.filename_stem
    review_dir.mkdir(parents=True, exist_ok=True)
    points = {
        "frame_01_start.jpg": 0.45,
        "frame_02_action.jpg": max(0.7, spec.duration * 0.38),
        "frame_03_payoff.jpg": max(0.9, spec.duration * 0.72),
        "frame_04_end.jpg": max(0.5, spec.duration - 0.55),
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
                output,
                "-frames:v",
                "1",
                "-update",
                "1",
                "-q:v",
                "2",
                review_dir / name,
            ]
        )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-i",
            output,
            "-vf",
            "fps=1/2,scale=270:-1,tile=3x4:margin=8:padding=4",
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "3",
            review_dir / "contact_sheet.jpg",
        ]
    )


def verify(spec: ShortSpec, output: Path) -> str:
    review_dir = REVIEW_ROOT / spec.batch / spec.filename_stem
    result = run([FFMPEG, "-v", "error", "-i", output, "-f", "null", "-"])
    probe = run([FFMPEG, "-hide_banner", "-i", output, "-t", "0.1", "-f", "null", "-"]).stdout
    verify_text = f"decode_return={result.returncode}\n{probe}"
    (review_dir / "ffmpeg_probe.txt").write_text(verify_text, encoding="utf-8")
    return probe


def fmt_time(seconds: float) -> str:
    millis = int(round((seconds - int(seconds)) * 1000))
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def write_metadata(spec: ShortSpec, output: Path) -> None:
    meta_dir = META_ROOT / spec.batch
    meta_dir.mkdir(parents=True, exist_ok=True)
    metadata = meta_dir / f"short_{PY_DATE}_{spec.game}_{spec.topic}_metadata.txt"
    notes = meta_dir / f"short_{PY_DATE}_{spec.game}_{spec.topic}_notes.txt"

    metadata.write_text(
        "\n".join(
            [
                "TITLE",
                spec.title,
                "",
                "ALTERNATIVE TITLES",
                *[f"{i}. {title}" for i, title in enumerate(spec.alternatives, start=1)],
                "",
                "DESCRIPTION",
                spec.description,
                "",
                "SHORT DESCRIPTION",
                spec.short_description,
                "",
                "TAGS",
                ", ".join(spec.tags),
                "",
                "TARGETED HASHTAGS",
                " ".join(spec.targeted_hashtags),
                "",
                "RECOMMENDED DESCRIPTION HASHTAGS",
                " ".join(spec.recommended_hashtags),
                "",
                "THUMBNAIL / ON-SCREEN HOOK TEXT",
                *[f"- {hook}" for hook in spec.hook_options],
                "",
                "PINNED COMMENT",
                spec.pinned_comment,
                "",
                "OUTPUT FILE",
                str(output),
            ]
        ),
        encoding="utf-8",
    )

    segment_lines = []
    for segment in spec.segments:
        segment_lines.append(
            f"- {segment.label}: {segment.source} | {fmt_time(segment.start)} to {fmt_time(segment.start + segment.duration)} "
            f"({segment.duration:.2f}s) | {segment.source_note}"
        )
        if segment.crop_center_gameplay:
            segment_lines.append("  Gameplay crop used from old vertical Short: 1080x608 at y=656.")

    notes.write_text(
        "\n".join(
            [
                "WHY THIS MOMENT WAS SELECTED",
                spec.selection_reason,
                "",
                "EXACT START AND END TIMESTAMPS",
                *segment_lines,
                "",
                "HOOK USED",
                spec.hook.replace("\n", " "),
                "",
                "WHY THE FIRST SECOND SHOULD STOP VIEWERS FROM SWIPING",
                spec.first_second_reason,
                "",
                "SUGGESTED MUSIC STYLE",
                spec.music_style,
                "",
                "POSTING CATEGORY",
                spec.content_type,
                "",
                "STRATEGY CHECK",
                f"- Duration target: {spec.duration:.2f}s, within 8-22s.",
                "- First-frame hook added.",
                "- No external copyrighted music baked in.",
                "- Title and hashtags are specific to the video.",
                "- Clip ends quickly after the payoff.",
            ]
        ),
        encoding="utf-8",
    )


def write_manifest(outputs: list[tuple[ShortSpec, Path, str]]) -> None:
    manifest_dir = META_ROOT / "mrlluminati_strategy_v2_20260614"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# MrLluminati Gaming Strategy V2 Rework Manifest",
        "",
        "Default strategy applied: 10-18s preferred, 8-22s accepted, emotion-first hooks, accurate metadata, no external music baked in.",
        "",
        "| Batch | Output | Duration Target | Title | Source Mode |",
        "|---|---|---:|---|---|",
    ]
    for spec, output, source_mode in outputs:
        safe_title = spec.title.replace("|", "\\|")
        lines.append(f"| {spec.batch} | `{output.name}` | {spec.duration:.2f}s | {safe_title} | {source_mode} |")
    lines.extend(
        [
            "",
            "GTA note: original raw GTA downloads were not present at the old script paths, so GTA v2 cuts were made from the old local Shorts outputs with the gameplay area cropped back out.",
        ]
    )
    (manifest_dir / "strategy_v2_manifest.md").write_text("\n".join(lines), encoding="utf-8")


def source_mode(spec: ShortSpec) -> str:
    if any(segment.crop_center_gameplay for segment in spec.segments):
        return "Fallback from old local Short"
    return "Raw recording"


def main() -> None:
    if not FFMPEG.exists():
        raise FileNotFoundError(FFMPEG)
    missing = sorted({str(segment.source) for spec in SPECS for segment in spec.segments if not segment.source.exists()})
    if missing:
        raise FileNotFoundError("Missing sources:\n" + "\n".join(missing))
    ensure_dirs()

    outputs: list[tuple[ShortSpec, Path, str]] = []
    for spec in SPECS:
        print(f"\n=== Rendering {spec.filename_stem} ({spec.duration:.2f}s) ===")
        overlay = make_overlay(spec)
        parts = [render_segment(spec, segment, index, overlay) for index, segment in enumerate(spec.segments, start=1)]
        output = concat_segments(spec, parts)
        review(spec, output)
        probe = verify(spec, output)
        write_metadata(spec, output)
        outputs.append((spec, output, source_mode(spec)))
        print(probe)

    write_manifest(outputs)
    print("\nCreated strategy v2 rework outputs:")
    for spec, output, mode in outputs:
        print(f"- {spec.batch}: {output} ({spec.duration:.2f}s, {mode})")


if __name__ == "__main__":
    main()
