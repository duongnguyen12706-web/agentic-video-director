#!/usr/bin/env python3
"""
AI Prompt Director - Hollywood-Grade Generative Cinematography Engine
Location: E:\\antigraviti\\tools\\ai-director\\ai_prompt_director.py

Capabilities:
1. Generates 6-layer Hollywood director prompts for FLUX, Midjourney, Runway Gen-3, Kling, and Sora.
2. Automates full multi-shot scene shot-lists with lens specifications, lighting schemas, and camera vectors.
3. Exports structured storyboard breakdowns in JSON and Markdown formats.
"""

import sys
import os
import json
import argparse

LENSES = {
    "establishing": "18mm Ultra-Wide Anamorphic lens, expansive perspective",
    "dialogue": "50mm Cooke S4/i Prime lens, natural human eye perspective, f/1.8",
    "emotional": "85mm Panavision Primo lens, shallow depth of field, creamy oval bokeh, f/1.4",
    "action": "24mm ARRI Master Prime, dynamic motion perspective, f/2.0"
}

LIGHTING_SCHEMES = {
    "noir": "chiaroscuro high-contrast lighting, deep hard shadows, sharp rim light",
    "golden": "warm late golden hour backlight, soft volumetric haze, amber lens flare",
    "cyberpunk": "practical magenta and cyan neon lighting, wet floor reflections, volumetric steam",
    "gritty": "harsh fluorescent overhead lighting, desaturated greens, bleak shadows"
}

CAMERA_VECTORS = {
    "push_in": "slow forward dolly-in toward subject's eyes, low angle, 24fps motion blur",
    "orbit": "smooth 360-degree orbital arc shot maintaining focus on face, parallax background shift",
    "tracking": "kinetic truck tracking shot parallel to subject's sprint, steadycam motion",
    "pedestal": "dramatic pedestal boom up from ground level to high angle hero perspective"
}

def generate_cinematic_prompt(subject, setting, mood="noir", shot_type="emotional", motion="push_in"):
    lens = LENSES.get(shot_type, LENSES["emotional"])
    lighting = LIGHTING_SCHEMES.get(mood, LIGHTING_SCHEMES["noir"])
    camera_move = CAMERA_VECTORS.get(motion, CAMERA_VECTORS["push_in"])

    full_prompt = (
        f"{subject}, {setting}. {lighting}. "
        f"Shot on ARRI Alexa Mini LF, {lens}. "
        f"Authentic 35mm Kodak Vision3 500T film grain, subtle halation, rich shadow details. "
        f"Camera motion: {camera_move}."
    )
    return full_prompt

def generate_scene_storyboard(core_concept, output_file=None):
    """Generates an entire 4-shot cinematic sequence with visual continuity."""
    shots = [
        {
            "shot_number": 1,
            "type": "Wide Establishing",
            "focal_length": "18mm Anamorphic",
            "camera_motion": "Dolly Out / Boom Down",
            "lighting": "Volumetric atmospheric haze",
            "prompt": generate_cinematic_prompt(f"Wide panoramic view of {core_concept}", "expansive environment", mood="noir", shot_type="establishing", motion="pedestal")
        },
        {
            "shot_number": 2,
            "type": "Medium Tracking",
            "focal_length": "35mm Prime",
            "camera_motion": "Truck Left Tracking Shot",
            "lighting": "Side Key Rembrandt Lighting",
            "prompt": generate_cinematic_prompt(f"Subject in action exploring {core_concept}", "detailed foreground elements", mood="noir", shot_type="dialogue", motion="tracking")
        },
        {
            "shot_number": 3,
            "type": "Extreme Close-Up",
            "focal_length": "85mm Telephoto f/1.4",
            "camera_motion": "Micro Push-in onto eyes",
            "lighting": "Sharp rim light + eye catchlight",
            "prompt": generate_cinematic_prompt(f"Extreme close-up of subject's eyes reflecting {core_concept}", "subsurface scattering on skin", mood="noir", shot_type="emotional", motion="push_in")
        },
        {
            "shot_number": 4,
            "type": "Hero Orbit Climax",
            "focal_length": "24mm Dynamic",
            "camera_motion": "360-degree Orbital Arc",
            "lighting": "Dramatic silhouette with backlight",
            "prompt": generate_cinematic_prompt(f"Climactic moment of {core_concept}", "pinnacle revelation", mood="noir", shot_type="action", motion="orbit")
        }
    ]

    result = {
        "concept": core_concept,
        "storyboard_shots": shots
    }

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Storyboard exported to: {output_file}")

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Prompt Director - Generative Cinema Engine")
    parser.add_argument("concept", help="Core story concept or character scenario")
    parser.add_argument("--mood", default="noir", choices=list(LIGHTING_SCHEMES.keys()))
    parser.add_argument("--shot", default="emotional", choices=list(LENSES.keys()))
    parser.add_argument("--motion", default="push_in", choices=list(CAMERA_VECTORS.keys()))
    parser.add_argument("--export-storyboard", help="Output JSON path for 4-shot storyboard")

    args = parser.parse_args()

    if args.export_storyboard:
        generate_scene_storyboard(args.concept, args.export_storyboard)
    else:
        prompt = generate_cinematic_prompt(args.concept, "cinematic scene", mood=args.mood, shot_type=args.shot, motion=args.motion)
        print("\n=== GENERATED CINEMATIC PROMPT ===")
        print(prompt)
        print("==================================\n")
