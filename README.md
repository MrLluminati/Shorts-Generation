# Shorts Generation

Reusable local pipeline for turning livestreams, gameplay recordings, and other source videos into upload-ready YouTube Shorts and story-first long-form edits.

## What This Repo Tracks

- Python build scripts in `scripts/`
- Live video workflow docs in `live_video_pipeline/`
- Metadata templates and reusable planning files

Generated videos, source media, review frames, contact sheets, subtitles, cached binaries, and private working files are ignored by Git.

## Current Pipelines

- `scripts/build_gta_grand_rp_shorts.py` - GTA V Grand RP Shorts pack
- `scripts/build_rdr2_live_outputs.py` - RDR2 Hindi story Shorts and long-form parts
- `scripts/build_rdr2_retention_fix_shorts.py` - corrected shorter RDR2 Shorts
- `scripts/build_re3_gameplay_outputs.py` - Resident Evil 3 gameplay outputs
- `scripts/build_shorts.py` and related scripts - movie/explainer Short builders

## Setup

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

The scripts also support the existing local `vendor/imageio_ffmpeg` runtime when present.

## Usage Example

```powershell
python scripts\build_gta_grand_rp_shorts.py --source "C:\path\to\source.mp4"
```

Outputs are written under `live_video_pipeline/`:

- `short_form/` - rendered Shorts
- `long_form/` - rendered long-form edits
- `metadata/` - upload metadata CSV/Markdown
- `review/` - review frames and contact sheets
- `work/` - generated subtitles and intermediate files

## Working Rule

Keep Git for the pipeline, not the media. Store large videos locally or in Drive, then commit only scripts, templates, metadata formats, and docs.
