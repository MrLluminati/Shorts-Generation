from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOVIE_DIR = ROOT / "movies" / "Chainsaw Man Reze Arc"
SHORTS_DIR = MOVIE_DIR / "shorts"
METADATA_DIR = MOVIE_DIR / "metadata"
WORK_DIR = MOVIE_DIR / "work"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_shorts", ROOT / "scripts" / "build_shorts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load build_shorts.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    builder = load_builder()

    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    (WORK_DIR / "subtitles").mkdir(parents=True, exist_ok=True)

    builder.OUTPUT_DIR = SHORTS_DIR
    builder.SUBTITLE_DIR = WORK_DIR / "subtitles"

    smooth_short = builder.Short(
        slug="09_denji_heart_smooth",
        title="Denji's Heart",
        start="01:02:17.300",
        duration=23.1,
        hook="THE JOKE\nACTUALLY HURTS",
        upload_title="Denji's Heart Line Actually Hurts | Chainsaw Man #shorts",
        description=(
            "This moment works because Denji starts like he is joking, then says the sad part out loud. "
            "Everyone wants Chainsaw's heart, but Denji wants someone to want him. "
            "SceneCipher HQ decodes anime, movie, and series moments through silent explainers, hidden details, and scene logic."
        ),
        hashtags="#chainsawman #denji #reze #pochita #rezearc #animeexplained #animeedit #sceneexplained #shorts",
    )

    entries = builder.parse_srt(builder.SRT)
    ass_path = builder.make_ass(smooth_short, entries)
    video_path = builder.render_short(smooth_short, ass_path)

    metadata = "\n".join(
        [
            "# Smooth Viral Test Upload",
            "",
            f"- File: `{video_path.name}`",
            "- Source movie: `Chainsaw Man The Movie Reze Arc`",
            "- Source timestamp: `01:02:17.300` for `23.1s`",
            "- Edit note: continuous scene, no hard jump cuts, no mid-dialogue cuts.",
            f"- Upload title: {smooth_short.upload_title}",
            f"- Description: {smooth_short.description}",
            f"- Hashtags: {smooth_short.hashtags}",
            "- Tags: chainsaw man, denji, denji heart, denji heart line, chainsaw man reze arc, chainsaw man movie, reze, pochita, chainsaw heart, everyone wants chainsaw heart, anime explained, anime shorts, scene decoded, sad anime scene, scenecipher hq",
            "- Pinned comment: Did this line feel funny first or sad first?",
            "- Thumbnail text: THE JOKE HURTS",
            "- First 2 seconds hook: THE JOKE ACTUALLY HURTS",
            "- Upload action: Use this smoother version instead of the abrupt 08 jump-cut test.",
            "",
        ]
    )
    metadata_path = METADATA_DIR / "09_denji_heart_smooth.md"
    metadata_path.write_text(metadata, encoding="utf-8")

    print(video_path)
    print(metadata_path)


if __name__ == "__main__":
    main()
