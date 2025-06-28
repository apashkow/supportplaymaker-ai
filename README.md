# SupportPlaymaker.AI

Conversational AI assistant demo for Fanatics-style support workflows.

## Features
- Intent classification (bonus, login, bets)
- FAQ retrieval (RAG-like)
- GPT-4 Turbo LLM response
- FastAPI JSON endpoint
- Docker-ready

## Run Locally
```bash
docker build -t supportplaymaker .
docker run -p 8000:8000 supportplaymaker
```

## Test Endpoint
POST `/chat`
```json
{
  "user_id": "123",
  "message": "Where’s my bonus?",
  "metadata": {}
}
```
