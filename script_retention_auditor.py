#!/usr/bin/env python3
"""
Script Retention Auditor - Psychological Scriptwriting Analyzer
Location: E:\\antigraviti\\tools\\narrative-engineer\\script_retention_auditor.py

Capabilities:
1. Calculates word counts, speaking durations, and pacing tempo (words per minute).
2. Audits First-15-Seconds Hook vitality against forbidden boring phrases.
3. Detects premature ending triggers and calculates overall Retention Health Score.
"""

import sys
import os
import re
import argparse

FORBIDDEN_INTRO_WORDS = [
    "chào mừng các bạn", "chào mừng quay trở lại", "hôm nay mình sẽ",
    "trong video này tôi sẽ", "hãy nhớ like và subscribe", "đừng quên bấm chuông",
    "xin chào mọi người", "welcome back to my channel", "in this video today"
]

FORBIDDEN_OUTRO_WORDS = [
    "tóm lại là", "kết luận là", "và đó là tất cả", "cảm ơn các bạn đã xem",
    "hẹn gặp lại ở video sau", "to sum up", "in conclusion", "thanks for watching"
]

STAKE_POWER_WORDS = [
    "bí mật", "thảm họa", "nguy hiểm", "cháy", "mất", "chết", "nghịch lý",
    "khẩn cấp", "cảnh báo", "sai lầm", "tại sao", "nhưng", "đột ngột", "thách thức"
]

def audit_script(script_text):
    words = script_text.split()
    total_words = len(words)
    estimated_seconds = (total_words / 150.0) * 60.0 # 150 WPM standard
    
    # Analyze Hook (first 40 words ~ 15 seconds)
    hook_words = words[:40]
    hook_text = " ".join(hook_words).lower()

    intro_penalties = []
    for phrase in FORBIDDEN_INTRO_WORDS:
        if phrase in hook_text:
            intro_penalties.append(f"Forbidden intro cliché detected: '{phrase}'")

    has_stake_words = any(w in hook_text for w in STAKE_POWER_WORDS)

    # Analyze Outro (last 40 words)
    outro_words = words[-40:] if len(words) > 40 else words
    outro_text = " ".join(outro_words).lower()

    outro_penalties = []
    for phrase in FORBIDDEN_OUTRO_WORDS:
        if phrase in outro_text:
            outro_penalties.append(f"Premature ending trigger detected: '{phrase}' (Causes sudden audience drop-off)")

    # Score calculation (Start at 100)
    score = 100
    score -= len(intro_penalties) * 25
    if not has_stake_words:
        score -= 20
        intro_penalties.append("Missing high-stakes power word in the first 15 seconds.")
    score -= len(outro_penalties) * 20

    score = max(0, min(100, score))

    report = {
        "total_words": total_words,
        "estimated_duration_minutes": round(estimated_seconds / 60.0, 2),
        "estimated_duration_seconds": round(estimated_seconds, 1),
        "retention_health_score": score,
        "intro_issues": intro_penalties,
        "outro_issues": outro_penalties,
        "recommendations": []
    }

    if score >= 85:
        report["verdict"] = "EXCELLENT (High-Retention Ready)"
    elif score >= 60:
        report["verdict"] = "AVERAGE (Needs Hook & Pacing Tightening)"
    else:
        report["verdict"] = "CRITICAL (High Risk of Immediate Viewer Drop-off)"

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script Retention Auditor - Psychological Script Analyzer")
    parser.add_argument("script_file", help="Path to text/markdown script file")

    args = parser.parse_args()

    if not os.path.exists(args.script_file):
        print(f"[ERROR] File not found: {args.script_file}")
        sys.exit(1)

    with open(args.script_file, "r", encoding="utf-8") as f:
        content = f.read()

    result = audit_script(content)

    print("\n================ RETENTION AUDIT REPORT ================")
    print(f"Total Words: {result['total_words']}")
    print(f"Estimated Video Length: {result['estimated_duration_minutes']} minutes ({result['estimated_duration_seconds']}s)")
    print(f"Retention Health Score: {result['retention_health_score']}/100 -> {result['verdict']}")
    print("-------------------------------------------------------")
    if result["intro_issues"]:
        print("[HOOK WARNINGS]:")
        for issue in result["intro_issues"]:
            print(f"  * {issue}")
    else:
        print("[HOOK STATUS]: Clean, aggressive start without intro fluff!")

    if result["outro_issues"]:
        print("[OUTRO WARNINGS]:")
        for issue in result["outro_issues"]:
            print(f"  * {issue}")
    else:
        print("[OUTRO STATUS]: Clean cut without premature goodbye triggers!")
    print("=======================================================\n")
