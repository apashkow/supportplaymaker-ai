from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from agent import run_agent
from stats import parse_log
import time
import logging
import os

app = FastAPI()

# Allow CORS from any origin (for local + Render frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(filename="logs/interactions.log", level=logging.INFO)

@app.post("/chat")
async def chat(req: Request):
    t0 = time.time()
    data = await req.json()
    user_id = data.get("user_id", "unknown")
    message = data.get("message", "")
    metadata = data.get("metadata", {})

    response = run_agent(message, user_id, metadata)
    latency_ms = int((time.time() - t0) * 1000)

    log_entry = {
        "user_id": user_id,
        "message": message,
        "response": response,
        "latency_ms": latency_ms,
        "metadata": metadata,
    }
    logging.info(log_entry)

    return {"response": response, "latency_ms": latency_ms, "metadata": {}}

@app.get("/stats")
async def stats():
    return parse_log()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/ui/{path:path}")
async def static_files(path: str):
    file_path = f"frontend/{path}"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="Not found", status_code=404)