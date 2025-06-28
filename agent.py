import os

# Load .env in dev; no effect on Render
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not set. Add to .env or Render env vars.")

# Set up OpenAI client
from openai import OpenAI
client = OpenAI(api_key=openai_api_key)

# Internal tools
from classifier import classify_intent
from retriever import retrieve_answer
from log_utils import log_interaction

# System behavior prompt
SYSTEM_PROMPT = """
You are SupportPlaymaker.AI – a fast, helpful, fan-friendly assistant for customer support agents at a sports betting platform.
Always use a friendly tone. Escalate unclear cases to a human.
"""

def run_agent(user_id: str, message: str, metadata: dict):
    intent, confidence = classify_intent(message)
    model_used = "gpt-3.5-turbo"

    if confidence < 0.7:
        response_text = "I'm not 100% sure how to help – flagging this for a human agent to review!"
        latency_ms = 0
        log_interaction(user_id, message, response_text, latency_ms, model_used, intent, confidence)
        return response_text

    context_snippet = retrieve_answer(intent)

    prompt = f"""{SYSTEM_PROMPT}

User message: {message}
Intent: {intent}
Context: {context_snippet}
Response:"""

    # Call OpenAI ChatCompletion
    import time
    start = time.time()
    result = client.chat.completions.create(
        model=model_used,
        messages=[{"role": "user", "content": prompt}]
    )
    latency_ms = int((time.time() - start) * 1000)

    response_text = result.choices[0].message.content.strip()

    # Log for stats
    log_interaction(user_id, message, response_text, latency_ms, model_used, intent, confidence)

    return response_text
