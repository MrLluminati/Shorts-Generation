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

    tonight_short = builder.Short(
        slug="07_chainsaw_heart_contract",
        title="Heart Contract",
        start="00:25:56.500",
        duration=42.5,
        hook="WHY EVERY DEVIL\nWANTS HIS HEART",
        upload_title="Why Every Devil Wants Chainsaw's Heart | Chainsaw Man Decoded #shorts",
        description=(
            "This scene quietly explains the real engine of the Reze Arc: "
            "Chainsaw's heart is not just a power source, it is the prize every side is hunting. "
            "SceneCipher HQ decodes anime, movie, and series moments through silent explainers, hidden details, and scene logic."
        ),
        hashtags="#chainsawman #denji #reze #animeexplained #shorts",
    )

    entries = builder.parse_srt(builder.SRT)
    ass_path = builder.make_ass(tonight_short, entries)
    video_path = builder.render_short(tonight_short, ass_path)

    metadata = "\n".join(
        [
            "# Tonight Upload",
            "",
            f"- File: `{video_path.name}`",
            "- Source movie: `Chainsaw Man The Movie Reze Arc`",
            "- Source timestamp: `00:25:56.500` for `42.5s`",
            f"- Upload title: {tonight_short.upload_title}",
            f"- Description: {tonight_short.description}",
            f"- Hashtags: {tonight_short.hashtags}",
            "- Pinned comment: Would you risk everything for Chainsaw's heart?",
            "- Thumbnail text: THE HEART CONTRACT",
            "- First 2 seconds hook: WHY EVERY DEVIL WANTS HIS HEART",
            "- Upload action: Upload tonight as a public Short after checking copyright claim status in YouTube Studio.",
            "",
        ]
    )
    metadata_path = METADATA_DIR / "07_chainsaw_heart_contract.md"
    metadata_path.write_text(metadata, encoding="utf-8")

    print(video_path)
    print(metadata_path)


if __name__ == "__main__":
    main()
