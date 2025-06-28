FAQ_KB = {
    "bonus_issue": "Bonuses may take up to 48 hours to appear after meeting the qualifying conditions.",
    "account_access": "If you're having trouble logging in, try resetting your password or contact support.",
    "bet_status": "Bets are settled shortly after the event ends. Check your bet history for confirmation.",
}

def retrieve_answer(intent):
    return FAQ_KB.get(intent, "No matching entry found. Please escalate.")
