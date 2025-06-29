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

# ✅ Updated function to log interaction with full details
def log_interaction(user_id, message, response, metadata, latency):
    log_msg = (
        f"USER: {user_id} | Latency: {latency}ms\n"
        f"Message: {message}\n"
        f"Response: {response}\n"
        f"Metadata: {metadata}\n"
    )
    logger.info(log_msg)

# ✅ Existing latency logging
def log_latency(latency_ms):
    with open("logs/latency.log", "a") as f:
        f.write(f"{latency_ms}\n")
