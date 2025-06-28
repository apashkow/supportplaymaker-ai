import os
from retriever import retrieve_answer
from classifier import classify_intent
from openai import OpenAI
from dotenv import load_dotenv
from log_utils import log_interaction  # ✅ New: logging support

# Load .env vars
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# LLM system prompt
SYSTEM_PROMPT = """
You are SupportPlaymaker.AI – a fast, helpful, fan-friendly assistant for customer support agents at a sports betting platform.
Always use a friendly tone. Escalate unclear cases to a human.
"""

# Main agent runner
def run_agent(user_id: str, message: str, metadata: dict):
    intent, confidence = classify_intent(message)

    if confidence < 0.7:
        return "I'm not 100% sure – flagging this for a human agent to review."

    context_snippet = retrieve_answer(intent)

    prompt = f"""{SYSTEM_PROMPT}

User message: {message}
Intent: {intent}
Context: {context_snippet}
Response:"""

    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = result.choices[0].message.content.strip()

    # ✅ Debug output in terminal
    print(f"[DEBUG] Model used: gpt-3.5-turbo | Intent: {intent} | Confidence: {confidence}")

    # ✅ Log to file
    log_interaction(
        user_id=user_id,
        message=message,
        intent=intent,
        confidence=confidence,
        latency_ms=metadata.get("latency_ms", 0),
        model_used="gpt-3.5-turbo",
        response=response_text
    )

    return response_text
