#!/usr/bin/env python3
"""
Dynamic Reframe Director - Fincher Eye-Trace & Cinematic Framing Utility
Location: E:\\antigraviti\\tools\\video-editor\\dynamic_reframe_director.py

Capabilities:
1. Fincher-Style Micro Push-in: Smooth digital zoom (e.g. 1.0x to 1.05x) over clip duration to focus eye-trace.
2. Cinematic Scope (2.39:1 Anamorphic Letterbox): Clean organic matte overlays.
3. Aspect Ratio Translation: Intelligent crop from 16:9 to 9:16 (Shorts/Reels) with focal offset.
"""

import sys
import os
import argparse
import subprocess

def apply_fincher_pushin(input_file, output_file, zoom_factor=1.05, duration_seconds=5.0, fps=24):
    """
    Applies a subtle, elegant digital push-in over time using FFmpeg zoompan.
    zoom_factor: 1.05 = 5% push-in
    """
    total_frames = int(duration_seconds * fps)
    # zoompan filter: 'zoom+0.001' over duration
    zoom_increment = (zoom_factor - 1.0) / total_frames
    vf_filter = (
        f"zoompan=z='min(zoom+{zoom_increment:.6f},{zoom_factor})':"
        f"d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    )

    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", vf_filter,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-c:a", "copy",
        output_file
    ]
    print(f"[RUNNING Fincher Push-in]: {zoom_factor}x over {duration_seconds}s...")
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Push-in video created at: {output_file}")

def apply_cinematic_letterbox(input_file, output_file, aspect="2.39"):
    """
    Applies an authentic theatrical letterbox matte (2.39:1 anamorphic ratio).
    Standard 1920x1080 -> 1920x803 active picture with black bars.
    """
    # 1920 / 2.39 = 803.3 -> 804 height
    vf_filter = "crop=1920:804:0:138,pad=1920:1080:0:138:black"
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", vf_filter,
        "-c:v", "libx264", "-crf", "18",
        "-c:a", "copy",
        output_file
    ]
    print(f"[RUNNING Cinematic 2.39:1 Letterbox Matte]...")
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Letterboxed video created at: {output_file}")

def reframe_vertical_916(input_file, output_file, x_offset="center"):
    """
    Crops 1920x1080 landscape to 1080x1920 or 608x1080 vertical 9:16 for TikTok/Reels.
    """
    # 1080 * 9 / 16 = 607.5 -> 608
    if x_offset == "center":
        crop_x = "(iw-ow)/2"
    elif x_offset == "left":
        crop_x = "(iw-ow)/4"
    else: # right
        crop_x = "3*(iw-ow)/4"

    vf_filter = f"crop=608:1080:{crop_x}:0,scale=1080:1920"
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", vf_filter,
        "-c:v", "libx264", "-crf", "19",
        "-c:a", "copy",
        output_file
    ]
    print(f"[RUNNING 9:16 Vertical Reframe ({x_offset})]...")
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Vertical 9:16 video created at: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Reframe Director - Visual Attention Utility")
    subparsers = parser.add_subparsers(dest="mode")

    p_push = subparsers.add_parser("pushin")
    p_push.add_argument("input")
    p_push.add_argument("output")
    p_push.add_argument("--zoom", type=float, default=1.05)
    p_push.add_argument("--duration", type=float, default=5.0)

    p_scope = subparsers.add_parser("scope")
    p_scope.add_argument("input")
    p_scope.add_argument("output")

    p_vert = subparsers.add_parser("vertical")
    p_vert.add_argument("input")
    p_vert.add_argument("output")
    p_vert.add_argument("--align", default="center", choices=["center", "left", "right"])

    args = parser.parse_args()
    if args.mode == "pushin":
        apply_fincher_pushin(args.input, args.output, args.zoom, args.duration)
    elif args.mode == "scope":
        apply_cinematic_letterbox(args.input, args.output)
    elif args.mode == "vert":
        reframe_vertical_916(args.input, args.output, args.align)
    else:
        parser.print_help()
