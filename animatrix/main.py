"""
main.py
-------
FastAPI backend that wraps generate_scene.py.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from generate_scene import generate_animation_video

# ---------------------------------------------------------------------------
# Checkpoint 1 — App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="Prompt-to-Animation API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Prompt-to-Animation API is running."}


# ---------------------------------------------------------------------------
# Checkpoint 2 — Define the request shape
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Plain-English description of the animation to generate.",
    )


# ---------------------------------------------------------------------------
# Checkpoint 4 (part 1) — CORS middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Checkpoint 4 (part 2) — Ensure output folder exists, mount as static route
# ---------------------------------------------------------------------------

MEDIA_DIR = Path(os.getenv("MANIM_OUTPUT_DIR", "generated"))
MEDIA_DIR.mkdir(exist_ok=True)

app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


# ---------------------------------------------------------------------------
# Checkpoint 3 — Wire up the real logic
# Checkpoint 5 — Error handling
# ---------------------------------------------------------------------------

@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        video_path = generate_animation_video(request.prompt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    rel_path = Path(video_path).resolve().relative_to(MEDIA_DIR.resolve())
    video_url = f"/media/{rel_path.as_posix()}"

    return {"video_url": video_url}


# ---------------------------------------------------------------------------
# Checkpoint 6 — Run the server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)