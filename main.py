from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from log_utils import log_interaction, log_latency
from stats import parse_log
import time

app = FastAPI()

# CORS for frontend JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "unknown")
    message = data.get("message", "")
    metadata = data.get("metadata", {})

    start = time.time()
    try:
        reply = run_agent(message)
    except Exception as e:
        reply = "Sorry, something went wrong."
    latency = round((time.time() - start) * 1000)

    log_interaction(user_id, message, reply, metadata, latency)
    log_latency(latency)

    return JSONResponse({"response": reply, "latency_ms": latency, "metadata": {}})

@app.get("/stats")
def get_stats():
    return parse_log()
