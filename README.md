# Agentic Video Director & Ghost Editor Suite

An autonomous AI video editing and cinematography pipeline designed for coding agents, inspired by `browser-use/video-use` and `kurbaitaev/ghost-editor`.

## ⚡ Core Engines Included

1. **`three_step_editor_pipeline.py` (The 3-Step Master Director)**:
   - Input: `[Raw Video] + [Content / Script] + [Requirements / Style]`
   - Output: Automated production blueprint, kinetic ASS subtitles, and one-click render batch.
2. **`ghost_agent_editor.py` (Ghost Agent Editor)**:
   - Word-level text-first segment splicing.
   - 30ms audio micro-fades at every cut boundary (eliminates 100% audio pops).
   - Face-safe dynamic subtitle rendering (prevents obscuring speaker faces).
   - 7 built-in aesthetic presets (`clean`, `kinetic`, `cinematic`, `editorial`, `meme`, `launch`, `pop`).
   - Self-evaluation loop via `ffprobe` (stream integrity and audio-sync validation).
3. **`beat_sync_engine.py`**: Automated audio transient detection and DaVinci / Premiere marker export.
4. **`dynamic_reframe_director.py`**: Cinematic push-ins (David Fincher style), letterboxing (2.39:1), and vertical 9:16 re-framing.
5. **`subtitle_burn_engine.py`**: Kinetic karaoke-style word highlighting subtitles (.ass).
6. **`script_retention_auditor.py`**: Retention psychology analyzer (Dan Harmon circle, open loops, death-phrase detection).
7. **`ai_prompt_director.py`**: 6-layer optical cinematography prompt generator for AI video tools.

## Quick Start
```bash
# Execute 3-step pipeline
python three_step_editor_pipeline.py raw.mp4 "My video script" "TikTok 9:16 kinetic"

# Run ghost editor with 30ms micro-fades
python ghost_agent_editor.py raw.mp4 final.mp4 --style kinetic
```
