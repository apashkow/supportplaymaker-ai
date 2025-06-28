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

# ✅ Function to log every interaction
def log_interaction(user_id, message, intent, confidence, latency_ms, model_used, response):
    log_msg = (
        f"USER: {user_id} | Intent: {intent} ({confidence}) | Latency: {latency_ms}ms | Model: {model_used}\n"
        f"Message: {message}\n"
        f"Response: {response}\n"
    )
    logger.info(log_msg)
