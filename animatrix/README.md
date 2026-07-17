# Prompt-to-Animation Backend

Turns a plain-English prompt into a rendered Manim animation, served via a FastAPI backend.

## Files

- `generate_scene.py` — core engine: prompt → LLM → clean Manim code → rendered `.mp4`
- `main.py` — FastAPI backend that wraps the engine and exposes it over HTTP
- `.env.example` — template for required environment variables
- `requirements.txt` — Python dependencies

## Setup

1. **Install FFmpeg** (required by Manim to render video):
   - Windows: `choco install ffmpeg -y` (requires [Chocolatey](https://chocolatey.org/install), run as Administrator)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

   After installing, restart your terminal (or your PC on Windows) so the new PATH is picked up. Confirm with:
```bash
   ffmpeg -version
```

2. **Create a virtual environment and install Python dependencies:**
```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # macOS/Linux
   pip install -r requirements.txt
```

3. **Get a Gemini API key:**
   - Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   - Sign in, click **Create API key**, copy it

4. **Set up environment variables:**
```bash
   cp .env.example .env
```
   Then edit `.env` and paste in your real key:
   GEMINI_API_KEY=your_actual_key_here
MANIM_OUTPUT_DIR=generated
   5. **Run the backend:**
```bash
   python main.py
```
   The API will be live at `http://localhost:8000`.

## API

### `GET /`
Health check. Returns `{"status": "ok", ...}`.

### `POST /generate`
Request body:
```json
{ "prompt": "Animate a blue circle transforming into a red square." }
```

Success response:
```json
{ "video_url": "/media/media/videos/scene_ab12cd34/480p15/GeneratedScene.mp4" }
```

Fetch the actual video file from:
http://localhost:8000<video_url>
Error responses return an appropriate HTTP status code (`400` for bad
input/LLM output, `500` for rendering failures) with a `detail` message.

## Testing

- Interactive API docs: `http://localhost:8000/docs` — lets you test `/generate` directly in the browser without a frontend.
- Standalone test of just the LLM connection:
```bash
  python -c "from generate_scene import call_llm; print(call_llm('Say hello.'))"
```
- Standalone test of the full pipeline:
```bash
  python generate_scene.py
```

## Notes

- Rendered videos and generated scene scripts are stored under `generated/`
  (configurable via `MANIM_OUTPUT_DIR` in `.env`), which is mounted as a
  static route at `/media`.
- Uses Google Gemini via its OpenAI-compatible endpoint (the `openai`
  Python package, pointed at Google's `base_url`) — not OpenAI directly.
- CORS is open (`allow_origins=["*"]`) for local development with a
  frontend on a different port. Restrict this before any real deployment.
- `reload=True` in `main.py` is for local development only — disable it
  in production.