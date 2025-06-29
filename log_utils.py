import os
import logging

# Ensure the logs folder exists
os.makedirs("logs", exist_ok=True)

# Set up the logger
logger = logging.getLogger("supportplaymaker")
logger.setLevel(logging.INFO)

# Create a file handler for writing logs
handler = logging.FileHandler("logs/interactions.log")
formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ✅ Unified logging function (update main.py to call this)
def log_interaction(user_id, message, response, metadata=None, latency_ms=None):
    log_msg = f"User: {user_id}\nMessage: {message}\nResponse: {response}"
    if metadata:
        log_msg += f"\nMetadata: {metadata}"
    if latency_ms:
        log_msg += f"\nLatency: {latency_ms}ms"
    log_msg += "\n" + "-" * 40
    logger.info(log_msg)

# ✅ Separate latency-only logging (optional)
def log_latency(latency_ms):
    with open("logs/latency.log", "a") as f:
        f.write(f"{latency_ms}\n")
