#!/usr/bin/env python3
"""
100% Automated Step 4 (Google Veo 3 Image-to-Video Batch Runner) + Step 5 Re-Assembler.
Supports:
  Mode A: Google Gemini / Vertex AI Veo API (`GEMINI_API_KEY` in `.env` or environment)
  Mode B: Local FFmpeg High-FPS Motion Engine (0-cost instant fallback when API key is not set)
"""
import os
import sys
import time
import json
import argparse
import subprocess

SCENES_CONFIG = [
    {
        "id": 1,
        "image": "scene_01_hook.jpg",
        "duration": 2.80,
        "prompt": "Continuous vertical 9:16 shot. Subtle camera push-in. The young Vietnamese woman in the pastel sky-blue knitted polo top looks flustered from the heat, fanning her face with her right hand and speaking Vietnamese to camera with expressive lip-sync. No on-screen text."
    },
    {
        "id": 2,
        "image": "scene_02_pain.jpg",
        "duration": 4.60,
        "prompt": "Continuous vertical 9:16 shot. Sitting at a sunlit cafe table, the woman holds the old plastic fan, shakes her head with a tired sigh, and speaks Vietnamese to camera with natural lip-sync. No on-screen text."
    },
    {
        "id": 3,
        "image": "scene_03_hero_anchor.jpg",
        "duration": 5.31,
        "prompt": "Continuous vertical 9:16 shot. Bright refreshing daylight. The woman smiles radiantly while holding the champagne-silver iMI handheld turbo fan in her right hand and speaks Vietnamese to camera with accurate lip-sync. Rigid product geometry, zero morphing, no extra text."
    },
    {
        "id": 4,
        "image": "scene_04_broll_hair_wind.jpg",
        "duration": 4.78,
        "prompt": "Vertical 9:16 close-up B-Roll shot. The woman holds the champagne-silver iMI handheld fan near her cheek as a powerful stream of cool air blows her long wavy dark brown hair back smoothly in slow motion while she smiles refreshed. Rigid product geometry, zero morphing."
    },
    {
        "id": 5,
        "image": "scene_05_broll_macro_turbine.jpg",
        "duration": 5.24,
        "prompt": "Vertical 9:16 extreme macro product shot. Slow cinematic camera pan across the champagne-silver iMI handheld fan standing on a sunlit wooden table, showcasing the spinning turbine blades inside the glowing blue LED ring and the crisp 120 LED display. Rigid product geometry, zero morphing."
    },
    {
        "id": 6,
        "image": "scene_06_broll_finger_touch.jpg",
        "duration": 5.36,
        "prompt": "Vertical 9:16 macro shot. A slender female hand holds the champagne-silver iMI handheld fan; her thumb gently presses the pill-shaped button below the 120 LED display twice with realistic micro-movement. Rigid product geometry, zero morphing, no extra text."
    },
    {
        "id": 7,
        "image": "scene_07_broll_trust_hero.jpg",
        "duration": 5.34,
        "prompt": "Vertical 9:16 commercial hero shot. Slow smooth dolly push-in on the champagne-silver iMI handheld fan standing upright on the left-center of a clean white table with a soft-focus power bank and USB-C cable behind it. Rigid product geometry, zero morphing."
    },
    {
        "id": 8,
        "image": "scene_08_payoff_cta.jpg",
        "duration": 6.49,
        "prompt": "Continuous vertical 9:16 shot. The woman smiles brightly with her hair gently moving in the breeze, holding the champagne-silver iMI fan in her right hand, pointing downward-left toward the shopping cart with her left index finger while speaking Vietnamese to camera. Rigid product geometry."
    },
]

def run_veo_api(campaign_dir: str, api_key: str, model_name: str = "veo-2.0-generate-001"):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    kf_dir = os.path.join(campaign_dir, "keyframes_v1")
    out_dir = os.path.join(campaign_dir, "raw_scenes_veo")
    os.makedirs(out_dir, exist_ok=True)

    for sc in SCENES_CONFIG:
        img_path = os.path.join(kf_dir, sc["image"])
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        print(f"[Veo API] Submitting Scene {sc['id']}: {sc['image']}...")
        operation = client.models.generate_videos(
            model=model_name,
            prompt=sc["prompt"],
            image=types.Image(image_bytes=img_bytes, mime_type="image/jpeg"),
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                number_of_videos=1,
            ),
        )
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        video_obj = operation.response.generated_videos[0].video
        out_file = os.path.join(out_dir, f"scene_{sc['id']:02d}.mp4")
        client.files.download(file=video_obj)
        video_obj.save(out_file)
        print(f"[Veo API] Saved Scene {sc['id']} -> {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-dir", default=r"f:\Ai Agent Setup\SubAgent\Subagent\campaigns\2026-10-21\quat-cam-tay-imi-5000mah")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY", ""))
    args = parser.parse_args()

    if args.api_key:
        run_veo_api(args.campaign_dir, args.api_key)
    else:
        print("No GEMINI_API_KEY detected in environment; running local automated Step 4+5 engine...")
        subprocess.run([sys.executable, os.path.join(args.campaign_dir, "build_step4_step5_auto.py")], check=True)
