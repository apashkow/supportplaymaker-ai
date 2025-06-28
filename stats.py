import os
import re
from collections import defaultdict

LOG_PATH = "logs/interactions.log"

def parse_log():
    stats = {
        "total_requests": 0,
        "total_latency_ms": 0,
        "intent_counts": defaultdict(int),
        "model_counts": defaultdict(int),
        "unique_users": set()
    }

    if not os.path.exists(LOG_PATH):
        return {
            "total_requests": 0,
            "avg_latency_ms": 0,
            "most_common_intent": None,
            "most_common_model": None,
            "unique_user_count": 0
        }

    with open(LOG_PATH, "r") as log_file:
        lines = log_file.readlines()

    for i in range(0, len(lines), 4):  # each log block is 4 lines
        if i + 3 >= len(lines):
            continue  # skip incomplete

        meta = lines[i].strip()
        match = re.search(r"USER: (.*?) \| Intent: (.*?) \((.*?)\) \| Latency: (\d+)ms \| Model: (.*)", meta)
        if match:
            user_id, intent, confidence, latency_ms, model = match.groups()
            stats["total_requests"] += 1
            stats["total_latency_ms"] += int(latency_ms)
            stats["intent_counts"][intent] += 1
            stats["model_counts"][model] += 1
            stats["unique_users"].add(user_id)

    avg_latency = stats["total_latency_ms"] / stats["total_requests"] if stats["total_requests"] else 0
    most_common_intent = max(stats["intent_counts"], key=stats["intent_counts"].get, default=None)
    most_common_model = max(stats["model_counts"], key=stats["model_counts"].get, default=None)

    return {
        "total_requests": stats["total_requests"],
        "avg_latency_ms": round(avg_latency, 2),
        "most_common_intent": most_common_intent,
        "most_common_model": most_common_model,
        "unique_user_count": len(stats["unique_users"])
    }
