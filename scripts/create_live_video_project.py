from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "live_video_pipeline"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "live_video"


def write_once(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a workspace for one YouTube live edit.")
    parser.add_argument("name", help="Project name, for example gta_rp_arrest_live")
    parser.add_argument("--url", default="", help="YouTube live URL")
    parser.add_argument("--file", default="", help="Local source file path")
    parser.add_argument("--game", default="", help="Game name")
    parser.add_argument("--language", default="Hindi/English", help="Primary language")
    args = parser.parse_args()

    slug = slugify(args.name)
    project = PIPELINE / "work" / slug
    project.mkdir(parents=True, exist_ok=True)

    write_once(
        project / "source.md",
        "\n".join(
            [
                f"# {args.name}",
                "",
                f"- Created: {date.today().isoformat()}",
                f"- YouTube URL: {args.url}",
                f"- Local file: {args.file}",
                f"- Game: {args.game}",
                f"- Language: {args.language}",
                "",
                "## Notes",
                "",
                "- Must-keep moments:",
                "- Parts to avoid:",
                "- Copyright-sensitive music sections:",
                "- Personal info to remove:",
                "",
            ]
        ),
    )
    write_once(
        project / "shorts_plan.csv",
        "slug,start,duration,hook,title,description_lead,hashtags,tags,pinned_comment,upload_order\n",
    )
    write_once(
        project / "long_form_segments.csv",
        "segment_order,start,end,label,keep_reason\n",
    )
    write_once(
        project / "review_checklist.md",
        "\n".join(
            [
                "# Review Checklist",
                "",
                "- Shorts are 1080x1920 and under 60 seconds.",
                "- Long form is 1920x1080 and has no dead air at the start.",
                "- Audio is clear and not clipping.",
                "- Captions do not cover important UI/action.",
                "- No private info, music issues, or accidental desktop exposure.",
                "- Metadata is ready before upload.",
                "",
            ]
        ),
    )

    for folder in ("short_form", "long_form", "metadata", "review"):
        (PIPELINE / folder / slug).mkdir(parents=True, exist_ok=True)

    print(project)


if __name__ == "__main__":
    main()
