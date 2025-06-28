import json
from collections import Counter
from fastapi import APIRouter

router = APIRouter()

def parse_log(log_path="logs/interactions.log"):
    total_requests = 0
    total_latency = 0
    intents = []
    models = []
    users = set()

    try:
        with open(log_path, "r") as f:
            for line in f:
                try:
                    log = json.loads(line)
                    latency = float(log.get("latency_ms", 0))
                    intent = log.get("intent")
                    model = log.get("model")
                    user = log.get("user_id")

                    if latency > 0:
                        total_requests += 1
                        total_latency += latency
                        if intent:
                            intents.append(intent)
                        if model:
                            models.append(model)
                        if user:
                            users.add(user)
                except (ValueError, json.JSONDecodeError, TypeError):
                    continue
    except FileNotFoundError:
        return {
            "total_requests": 0,
            "avg_latency_ms": 0.0,
            "most_common_intent": None,
            "most_common_model": None,
            "unique_user_count": 0
        }

    avg_latency = round(total_latency / total_requests, 2) if total_requests else 0.0

    return {
        "total_requests": total_requests,
        "avg_latency_ms": avg_latency,
        "most_common_intent": Counter(intents).most_common(1)[0][0] if intents else None,
        "most_common_model": Counter(models).most_common(1)[0][0] if models else None,
        "unique_user_count": len(users)
    }

@router.get("/stats")
def get_stats():
    return parse_log()
