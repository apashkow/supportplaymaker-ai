from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from agent import run_agent
from stats import parse_log  # ✅ Add this for /stats endpoint

app = FastAPI()

# Allow frontend tools like Postman to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = body.get("user_id")
    message = body.get("message")
    metadata = body.get("metadata", {})

    start_time = time.time()
    metadata["latency_ms"] = 0  # Default fallback

    response = run_agent(user_id, message, metadata)

    latency = round((time.time() - start_time) * 1000)
    metadata["latency_ms"] = latency

    return {
        "response": response,
        "latency_ms": latency,
        "metadata": metadata
    }

# ✅ Add this new route for live stats
@app.get("/stats")
def get_stats():
    return parse_log()
