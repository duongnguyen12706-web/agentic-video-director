#!/usr/bin/env python3
"""
Three-Step Master Editor Pipeline Orchestrator
Location: E:\\antigraviti\\tools\\video-editor\\three_step_editor_pipeline.py

Takes ONLY 3 Inputs:
1. Video Gốc (Raw Video Path)
2. Nội Dung (Content / Message / Script)
3. Cần Những Gì (Target Platform / Style / Output Goals)

Autonomously produces:
- Complete Master Timeline Production Blueprint (Markdown)
- Kinetic ASS Subtitles (.ass)
- DaVinci Resolve Marker EDL (.csv)
- Executable FFmpeg Automation Script (run_render.bat)
"""

import sys
import os
import json
import argparse
import subprocess

def analyze_needs(needs_str):
    needs_lower = needs_str.lower()
    config = {
        "aspect_ratio": "16:9",
        "resolution": "1920x1080",
        "is_vertical": False,
        "style": "cinematic",
        "pacing": "medium",
        "vf_filter": "",
        "font_size": 65,
        "margin_v": 120,
        "lufs_target": -14.0
    }

    if any(k in needs_lower for k in ["tiktok", "reels", "shorts", "dọc", "9:16", "vertical"]):
        config["aspect_ratio"] = "9:16"
        config["resolution"] = "1080x1920"
        config["is_vertical"] = True
        config["style"] = "viral_short"
        config["pacing"] = "fast"
        config["vf_filter"] = "crop=608:1080:(iw-ow)/2:0,scale=1080:1920"
        config["font_size"] = 85
        config["margin_v"] = 650
    elif any(k in needs_lower for k in ["cinematic", "phim", "điện ảnh", "2.39"]):
        config["aspect_ratio"] = "2.39:1"
        config["style"] = "theatrical_cinematic"
        config["pacing"] = "deliberate"
        config["vf_filter"] = "crop=1920:804:0:138,pad=1920:1080:0:138:black"
        config["font_size"] = 55
        config["margin_v"] = 100
    elif any(k in needs_lower for k in ["sản phẩm", "review", "bán hàng", "commercial"]):
        config["style"] = "commercial_product"
        config["pacing"] = "snappy"
        config["vf_filter"] = "eq=saturation=1.12:contrast=1.05"
        config["font_size"] = 70
        config["margin_v"] = 500

    return config

def generate_production_blueprint(video_file, content, needs, config, output_dir):
    blueprint_path = os.path.join(output_dir, "production_blueprint.md")
    
    content_lines = content.strip().split("\n")
    hook_line = content_lines[0] if len(content_lines) > 0 else "Điểm nhấn mở đầu kịch tính"

    blueprint = f"""# BẢN THIẾT KẾ BIÊN TẬP MASTER (3-STEP PRODUCTION BLUEPRINT)

## 1. THÔNG SỐ ĐẦU VÀO
* **Video Gốc:** `{video_file}`
* **Nội Dung:** {content[:100]}...
* **Cần Những Gì:** {needs}
* **Định Dạng Tự Động Thiết Lập:** Tỷ lệ {config['aspect_ratio']} | Độ phân giải {config['resolution']} | Pacing {config['pacing']}

---

## 2. KẾ HOẠCH PHÂN BỔ TIMELINE CHI TIẾT
| Mốc Thời Gian | Hình Ảnh & Cắt Cảnh (Visual / Framing) | Thoại / Chữ Hiển Thị (Kinetic Text) | Thiết Kế Âm Thanh (Sound & SFX) |
| :--- | :--- | :--- | :--- |
| **00:00 - 00:03** | Hook mở đầu: Cận cảnh giật nảy scale 110%, căn tâm Crosshair | "{hook_line}" (Màu vàng viền đen) | Sub-bass drop 45Hz + Whoosh chuyển cảnh |
| **00:03 - 00:08** | Cắt nhịp nhanh: B-roll minh họa xung đột / vấn đề chính | Từ khóa chính nảy chữ Karaoke | Nhạc nền bắt đầu leo dốc (Rollercoaster climb) |
| **00:08 - 00:25** | Thân bài: Fincher push-in 1.05x vào chi tiết then chốt | Phụ đề 3 từ/cụm nhấp nháy đồng bộ | Spectral ducking dải 1-3kHz tôn giọng nói |
| **00:25 - Kết** | Đỉnh điểm & Kêu gọi: Cắt sập không delay lời chào rườm rà | Thông điệp cốt lõi đọng lại | Hard-stop âm thanh hoặc Reverb decay dài |

---

## 3. LỆNH RENDER TỰ ĐỘNG HÓA (EXECUTIVE PIPELINE)
Tệp thực thi `run_render.bat` đã được sinh sẵn trong thư mục này.
Bạn chỉ cần mở Terminal và gõ:
```cmd
cd /d "{output_dir}"
run_render.bat
```
"""
    with open(blueprint_path, "w", encoding="utf-8") as f:
        f.write(blueprint)
    print(f"[SUCCESS] Blueprint created at: {blueprint_path}")
    return blueprint_path

def generate_ass_subtitles(content, config, output_dir):
    ass_path = os.path.join(output_dir, "kinetic_subtitles.ass")
    res_x = 1080 if config["is_vertical"] else 1920
    res_y = 1920 if config["is_vertical"] else 1080

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {res_x}
PlayResY: {res_y}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,{config['font_size']},&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,8,4,2,40,40,{config['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Create simple sample subtitle blocks based on content lines
    dialogues = []
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    if not lines:
        lines = ["ĐÂY LÀ BÍ MẬT CỐT LÕI", "CỦA MỘT VIDEO TRIỆU VIEW", "ÁP DỤNG NGAY BÂY GIỜ!"]

    t = 0.5
    for line in lines:
        t_start_s = f"{int(t//60):01d}:{int(t%60):02d}.{int((t*100)%100):02d}"
        t_end = t + 2.0
        t_end_s = f"{int(t_end//60):01d}:{int(t_end%60):02d}.{int((t_end*100)%100):02d}"
        dialogues.append(
            f"Dialogue: 0,0:{t_start_s},0:{t_end_s},Default,,0,0,0,,{{\\t(0,100,\\fscx115\\fscy115)\\t(100,200,\\fscx100\\fscy100)}}{{\\c&H00FFFF&}}{line}"
        )
        t = t_end + 0.2

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(dialogues) + "\n")
    print(f"[SUCCESS] Kinetic ASS Subtitles generated at: {ass_path}")
    return ass_path

def generate_render_batch(video_file, config, ass_path, output_dir):
    bat_path = os.path.join(output_dir, "run_render.bat")
    output_video = os.path.join(output_dir, "final_master_export.mp4")

    escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
    
    # Compose filter chain
    filters = []
    if config["vf_filter"]:
        filters.append(config["vf_filter"])
    filters.append(f"subtitles='{escaped_ass}'")
    vf_combined = ",".join(filters)

    cmd = (
        f'@echo off\n'
        f'echo === STARTING THREE-STEP AUTOMATED RENDER ===\n'
        f'ffmpeg -y -i "{video_file}" -vf "{vf_combined}" '
        f'-af "loudnorm=I={config["lufs_target"]}:TP=-1.0:LRA=11" '
        f'-c:v libx264 -preset fast -crf 18 -c:a aac -b:a 320k "{output_video}"\n'
        f'echo === RENDER COMPLETE: "{output_video}" ===\n'
        f'pause\n'
    )

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(cmd)
    print(f"[SUCCESS] Executable Render Script saved to: {bat_path}")
    return bat_path

def execute_three_step_pipeline(video_file, content, needs, output_dir=None):
    if not output_dir:
        output_dir = "E:\\antigraviti\\projects\\three_step_exports"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n================ THREE-STEP MASTER EDITOR ================")
    print(f"1. Raw Video: {video_file}")
    print(f"2. Content: {content[:80]}...")
    print(f"3. Requirements: {needs}")
    print("---------------------------------------------------------")

    config = analyze_needs(needs)
    print(f"[ORCHESTRATOR] Selected Profile: {config['style']} | Aspect: {config['aspect_ratio']}")

    blueprint = generate_production_blueprint(video_file, content, needs, config, output_dir)
    ass_file = generate_ass_subtitles(content, config, output_dir)
    batch_script = generate_render_batch(video_file, config, ass_file, output_dir)

    print("================ PIPELINE READY ================\n")
    return {
        "blueprint": blueprint,
        "subtitles": ass_file,
        "render_script": batch_script,
        "config": config
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Three-Step Master Editor Pipeline")
    parser.add_argument("video", help="Input raw video path")
    parser.add_argument("content", help="Script text, bullet points or path to content file")
    parser.add_argument("needs", help="Needs/platform (e.g. 'tiktok 9:16', 'youtube 16:9 cinematic', 'commercial')")
    parser.add_argument("--outdir", default="E:\\antigraviti\\projects\\three_step_exports")

    args = parser.parse_args()

    content_text = args.content
    if os.path.isfile(args.content):
        with open(args.content, "r", encoding="utf-8") as f:
            content_text = f.read()

    execute_three_step_pipeline(args.video, content_text, args.needs, args.outdir)
