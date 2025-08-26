# SwasthBot 🩺

A lightweight, **privacy-aware healthcare assistant** built with **FastAPI**.  
SwasthBot provides:
- Symptom triage (rule-based) with transparent reasoning
- Chat endpoint with **LLM adapter** (plug in your provider or use offline fallback)
- PII redaction utilities (logs & outputs)
- JWT auth, simple in-memory rate limiting, request IDs
- Clean, testable architecture & Docker setup

> ⚠️ **Disclaimer**: SwasthBot does **not** provide medical diagnosis. It offers information & triage suggestions only. Always consult a qualified clinician for medical decisions.

---

## Quickstart

### 1) Environment
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# (Optional) Add your LLM provider keys in .env
```

### 2) Run
```bash
uvicorn swasthbot.app:app --reload
```
Open docs at: http://127.0.0.1:8000/docs

### 3) Docker
```bash
docker build -t swasthbot:latest .
docker run -p 8000:8000 --env-file .env swasthbot:latest
```

---

## Endpoints (summary)

- `GET /health` – liveness & environment info (non-sensitive)
- `POST /v1/triage` – rule-based symptom triage
- `POST /v1/chat` – chat with LLM adapter (redacts PII in logs)
- `GET /v1/symptoms` – supported symptoms catalog
- `GET /v1/faq` – static FAQ

All `/v1/*` endpoints require **Bearer JWT** unless you set `AUTH_DISABLED=true` in `.env` (dev only).

---

## Configuration

Environment variables (`.env`):
```
APP_NAME=SwasthBot
APP_ENV=dev
AUTH_DISABLED=true
JWT_SECRET=change-me
JWT_ISSUER=swasthbot
RATE_LIMIT_PER_MIN=60

LLM_PROVIDER=offline           # 'offline' (default) or 'openai'
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

REDACT_LOGS=true
```

---

## Project Structure

```
SwasthBot/
├─ src/swasthbot/
│  ├─ app.py            # FastAPI app + routers
│  ├─ settings.py       # pydantic settings
│  ├─ security.py       # JWT helpers
│  ├─ llm.py            # LLM adapter (offline + OpenAI-ready)
│  ├─ redact.py         # PII redaction helpers
│  ├─ triage.py         # Rule-based triage
│  └─ schemas.py        # Pydantic models
├─ tests/
│  └─ test_triage.py
├─ requirements.txt
├─ Dockerfile
├─ .env.example
├─ LICENSE
└─ README.md
```

---

## Security & Privacy

- PII redaction for logs (emails, phones, MRN-like IDs)
- JWT authentication (opt-out in dev with `AUTH_DISABLED=true`)
- CORS disabled by default; configure for your domain
- No data stored server-side by default (stateless). Add your own persistence with caution.

---

## Extending

- Add providers in `llm.py` (Anthropic, Azure OpenAI, etc.)
- Wire external observability (OpenTelemetry, Prometheus) in `app.py`
- Replace in-memory rate limiter with Redis for production

---

## Tests
```bash
pytest -q
```

---

## License
[MIT](./LICENSE)
