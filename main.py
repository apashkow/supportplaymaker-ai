from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from agent import run_agent
from stats import router as stats_router

app = FastAPI()

# ✅ Mount frontend at /ui instead of /
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

# ✅ Add /stats endpoint
app.include_router(stats_router)

# ✅ Define expected input for /chat
class ChatRequest(BaseModel):
    user_id: str
    message: str
    metadata: dict = {}

# ✅ /chat endpoint with debug-friendly error handler
@app.post("/chat")
def chat(request: ChatRequest):
    import time
    start = time.time()

    try:
        response_text = run_agent(request.user_id, request.message, request.metadata)
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print("[ERROR]", error_msg)
        response_text = f"[ERROR]\n{error_msg}"

    latency_ms = round((time.time() - start) * 1000)

    return {
        "response": response_text,
        "latency_ms": latency_ms,
        "metadata": {}
    }
