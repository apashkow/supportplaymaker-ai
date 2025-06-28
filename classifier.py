def classify_intent(message: str):
    message = message.lower()
    if "bonus" in message:
        return "bonus_issue", 0.9
    if "login" in message or "account" in message:
        return "account_access", 0.85
    if "bet" in message:
        return "bet_status", 0.8
    return "unknown", 0.5
