# MrLluminati Gaming Shorts Workflow

This repository is the single source of truth for the MrLluminati Gaming YouTube Shorts production system. It stores the editing strategy, Codex instructions, content pillars, analytics findings, metadata format, upload checklist, and reusable prompts used to turn gameplay footage into upload-ready Shorts.

The current strategic focus is:

1. CS2 Shorts first.
2. Survival horror / zombie games second.
3. Minecraft clips and cinematic/action experiments as smaller supporting pillars.

## How To Use This Repo With Codex

Start every Shorts task by reading:

- `docs/SHORTS_STRATEGY.md`
- `docs/CONTENT_PILLARS.md`
- `docs/TITLE_AND_HOOK_LIBRARY.md`
- `docs/CODEX_WORKFLOW.md`
- `docs/UPLOAD_CHECKLIST.md`

For reusable requests, use the prompt files in `prompts/`. The master prompt is `prompts/CODEX_MASTER_SHORTS_PROMPT.md`.

## Repository Map

- `docs/` - channel strategy, analytics findings, editing rules, upload rules, and workflow docs.
- `prompts/` - reusable prompts for future Codex sessions.
- `templates/` - copy-paste metadata, notes, and upload package templates.
- `examples/` - example upload packages by content pillar.
- `scripts/` - Python/FFmpeg builders and helper scripts.
- `live_video_pipeline/` - local pipeline workspace for generated Shorts, metadata, reviews, and work files.

## Raw Footage

Keep raw footage out of Git. Use local paths such as:

- `C:\Users\abhik\Videos`
- `C:\Users\abhik\Downloads`
- an ignored local folder under `live_video_pipeline/input/`

Source media, rendered media, review images, and working files are ignored by `.gitignore`.

## Generated Outputs

Generated files should stay organized under `live_video_pipeline/`:

- `short_form/` - rendered Shorts.
- `long_form/` - rendered long-form edits.
- `metadata/` - upload titles, descriptions, tags, hashtags, pinned comments, and notes.
- `review/` - preview frames, contact sheets, and FFmpeg probe logs.
- `work/` - intermediate files, concat lists, extracted clips, subtitles, and temporary assets.

## Current Strategy

CS2 is the main growth engine. The strongest current themes are toxic teammates, solo queue chaos, team-kill attempts, timing mistakes, reload panic, multi-kill chains, clean reaction kills, and funny fails.

Recommended channel mix:

- 70% CS2 Shorts.
- 20% survival horror / zombie games.
- 10% Minecraft clips and cinematic/action experiments.

Minecraft wording rule: call it "Minecraft clips" unless the footage is clearly modded. Do not assume a clip is modded from old All The Mods references.

## Setup

Install Python dependencies when needed:

```powershell
python -m pip install -r requirements.txt
```

The scripts may also use the local `vendor/imageio_ffmpeg` runtime or a system/CapCut FFmpeg install when available.

## Working Rule

Keep Git for the strategy, scripts, templates, and docs. Do not commit raw footage, rendered videos, thumbnails, review frames, cached binaries, or private working exports.
