/**
 * script.js
 * ---------
 * Wires up the Animatrix UI to the FastAPI backend from Assignment 3.
 *
 * Flow: user types prompt -> clicks Generate! -> POST /api/generate
 *       -> backend renders video -> we play it in <video>
 */

// ---------------------------------------------------------------------------
// Checkpoint 1 — Grab the DOM elements
// ---------------------------------------------------------------------------

const promptInput = document.getElementById("prompt-input");
const generateBtn = document.getElementById("generate-btn");
const statusText = document.getElementById("status-text");
const resultVideo = document.getElementById("result-video");

// Base URL of the FastAPI backend from Assignment 3.
// Change this if your backend runs on a different host/port.
const API_BASE_URL = "http://localhost:8000";

// ---------------------------------------------------------------------------
// Checkpoint 2 — Wire up the click listener
// ---------------------------------------------------------------------------

generateBtn.addEventListener("click", () => {
  const prompt = promptInput.value.trim();

  if (!prompt) {
    setStatus("Please enter a prompt before generating.", true);
    return;
  }

  generateAnimation(prompt);
});

// ---------------------------------------------------------------------------
// Checkpoint 3 — Build and send the request
// Checkpoint 4 — Handle the response
// Checkpoint 5 — Handle failures
// ---------------------------------------------------------------------------

async function generateAnimation(prompt) {
  // Disable the button + reset UI while the request is in flight.
  generateBtn.disabled = true;
  resultVideo.style.display = "none";
  setStatus("Generating... this can take up to a minute.");

  try {
    const response = await fetch(`${API_BASE_URL}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      // Server responded, but with an error status (400/500/etc).
      // FastAPI's HTTPException puts the message in `detail`.
      let message = `Request failed (status ${response.status}).`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          message = errorData.detail;
        }
      } catch {
        // Response wasn't valid JSON; fall back to the generic message.
      }
      setStatus(message, true);
      return;
    }

    const data = await response.json();

    // video_url is already a full path from the backend — don't prepend
    // anything extra beyond the API host.
    resultVideo.src = `${API_BASE_URL}${data.video_url}`;
    resultVideo.style.display = "block";
    setStatus("Done! Your animation is ready.");
  } catch (err) {
    // fetch() itself threw — usually means the server is unreachable
    // (not running, wrong port, network error, CORS misconfiguration).
    setStatus(
      "Could not reach the server. Is the backend running on " +
        API_BASE_URL +
        "?",
      true
    );
  } finally {
    generateBtn.disabled = false;
  }
}

// ---------------------------------------------------------------------------
// Small helper to update the status text and its error styling.
// ---------------------------------------------------------------------------

function setStatus(message, isError = false) {
  statusText.textContent = message;
  statusText.classList.toggle("error", isError);
}