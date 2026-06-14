# Scripts

This folder contains Python/FFmpeg builders and helper scripts for Shorts, long-form edits, metadata generation, review frames, and repair passes.

## Current Rule

Scripts should follow the strategy in `docs/SHORTS_STRATEGY.md`.

For MrLluminati Gaming Shorts:

- target 10-18 seconds
- accept 8-22 seconds when justified
- avoid 30+ seconds unless the story is unusually strong
- export vertical 1080x1920 when possible
- generate metadata and notes
- create review frames/contact sheets when possible
- do not overwrite old outputs

## Output Locations

Use organized batch folders:

- `live_video_pipeline/short_form/<batch_name>/`
- `live_video_pipeline/long_form/<batch_name>/`
- `live_video_pipeline/metadata/<batch_name>/`
- `live_video_pipeline/review/<batch_name>/`
- `live_video_pipeline/work/<batch_name>/`

## Raw Media

Do not commit raw media or rendered videos. Keep large files in local folders such as `C:\Users\abhik\Videos`, `C:\Users\abhik\Downloads`, or ignored pipeline folders.
