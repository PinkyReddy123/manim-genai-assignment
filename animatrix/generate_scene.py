"""
generate_scene.py
------------------
The core AI-to-animation engine.

Flow:  plain-English prompt -> LLM -> raw text -> clean Manim code
       -> saved .py file -> `manim` subprocess -> rendered .mp4 path

Using Google Gemini via its OpenAI-compatible endpoint, so we use the
`openai` Python package but point it at Google's base_url instead of
OpenAI's servers.
"""

import os
import re
import uuid
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI   # pip install openai

# ---------------------------------------------------------------------------
# Week 1 Checkpoint — Load API credentials securely from a .env file and
# send a prompt to the LLM, capturing the raw response.
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Create a .env file (see .env.example) "
        "and set your key there."
    )

# Gemini exposes an OpenAI-compatible endpoint, so we use the OpenAI SDK
# but point it at Google's base_url instead of OpenAI's servers.
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

OUTPUT_DIR = Path(os.getenv("MANIM_OUTPUT_DIR", "generated"))
OUTPUT_DIR.mkdir(exist_ok=True)


def call_llm(prompt: str) -> str:
    """Send the prompt to the LLM and return the RAW text response."""
    response = client.chat.completions.create(
       model="gemini-flash-latest",
        max_tokens=2000,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Week 2 Checkpoint — Prompt engineering so the LLM reliably returns
# valid Manim Python code.
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are an expert Manim (Community Edition) developer.

Given a plain-English description of an animation, respond with a SINGLE
complete, runnable Manim scene.

Strict rules:
- Output ONLY Python code. No explanations, no prose, no markdown headers.
- You MAY wrap the code in a single ```python ... ``` fenced block.
- Always import manim with `from manim import *`.
- Define exactly one class that subclasses `Scene`.
- Name the class `GeneratedScene` (main.py depends on this name).
- The class must implement a `construct(self)` method.
- Keep the animation self-contained: no external file/network/image loads.
- Prefer simple, robust Manim objects (Text, MathTex, Circle, Square,
  Create, Write, FadeIn/FadeOut, Transform) so the code reliably renders.
- If you use a rate_func, ONLY use these exact names, unprefixed:
  linear, smooth, there_and_back, rush_into, rush_from, double_smooth.
  Do NOT use names like ease_in_quad, ease_out_sine, etc. — they require
  a module prefix and will cause a NameError. When in doubt, omit
  rate_func entirely and let Manim use its default.

"""


# ---------------------------------------------------------------------------
# Week 3 Checkpoint — Parse the AI's response and extract ONLY the clean
# Manim Python code (strip markdown fences, explanations, etc).
# ---------------------------------------------------------------------------

def extract_code(raw_response: str) -> str:
    fence_match = re.search(r"```(?:python)?\s*\n(.*?)```", raw_response, re.DOTALL)
    if fence_match:
        code = fence_match.group(1)
    else:
        code = raw_response

    code = code.strip()

    if "class GeneratedScene" not in code:
        raise ValueError(
            "LLM response did not contain a `GeneratedScene` class. "
            "Cannot proceed with rendering."
        )

    return code


# ---------------------------------------------------------------------------
# Week 4 Checkpoint — Save the extracted code to a file and use subprocess
# to run Manim on it, rendering an .mp4.
# ---------------------------------------------------------------------------

def save_scene_file(code: str) -> Path:
    file_id = uuid.uuid4().hex[:8]
    scene_path = OUTPUT_DIR / f"scene_{file_id}.py"
    scene_path.write_text(code, encoding="utf-8")
    return scene_path


def render_scene(scene_path: Path) -> Path:
    cmd = [
        "manim",
        "-ql",
        "--media_dir", str(OUTPUT_DIR / "media"),
        str(scene_path),
        "GeneratedScene",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Manim rendering failed:\n{result.stderr[-2000:]}"
        )

    video_dir = OUTPUT_DIR / "media" / "videos" / scene_path.stem / "480p15"
    mp4_files = list(video_dir.glob("*.mp4"))
    if not mp4_files:
        raise RuntimeError("Manim reported success but no .mp4 was found.")

    return mp4_files[0]


# ---------------------------------------------------------------------------
# Week 5 Checkpoint — Wrap the full flow into a single function,
# handle failures gracefully, return the video path.
# ---------------------------------------------------------------------------

def generate_animation_video(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    raw_response = call_llm(prompt)
    code = extract_code(raw_response)
    scene_path = save_scene_file(code)
    video_path = render_scene(scene_path)

    return str(video_path)


if __name__ == "__main__":
    test_prompt = "Animate a blue circle transforming into a red square."
    try:
        path = generate_animation_video(test_prompt)
        print(f"Video rendered at: {path}")
    except Exception as e:
        print(f"Generation failed: {e}")