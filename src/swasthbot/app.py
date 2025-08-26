from fastapi import FastAPI, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time, uuid, asyncio
from typing import Optional
from .settings import settings
from .security import auth_required, create_jwt
from .schemas import HealthResponse, TriageRequest, TriageResponse, ChatRequest, ChatResponse
from .triage import triage, SUPPORTED
from .llm import LLMClient
from .redact import redact

app = FastAPI(title=settings.app_name, version='1.0.0')

# (Optional) CORS - keep strict by default; adjust as needed
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['https://yourdomain.com'],
#     allow_methods=['POST','GET'],
#     allow_headers=['Authorization','Content-Type'],
# )

# Simple in-memory token bucket per IP
RATE_BUCKET = {}
RATE_WINDOW = 60.0  # seconds

@app.middleware('http')
async def add_context_and_rate_limit(request: Request, call_next):
    rid = str(uuid.uuid4())
    request.state.request_id = rid

    # Rate limit by client host
    ip = request.client.host if request.client else 'unknown'
    now = time.time()
    bucket = RATE_BUCKET.get(ip, {'ts': now, 'count': 0})
    # reset window
    if now - bucket['ts'] >= RATE_WINDOW:
        bucket = {'ts': now, 'count': 0}
    bucket['count'] += 1
    RATE_BUCKET[ip] = bucket
    if bucket['count'] > settings.rate_limit_per_min:
        return JSONResponse(status_code=429, content={'detail': 'Rate limit exceeded'})

    # proceed
    resp = await call_next(request)
    resp.headers['X-Request-ID'] = rid
    return resp

@app.get('/health', response_model=HealthResponse)
def health():
    return HealthResponse(app=settings.app_name, env=settings.app_env)

@app.get('/token')
def token_dev(username: str = 'demo'):
    if not settings.auth_disabled:
        # Hide this in prod; included for demo convenience
        raise HTTPException(status_code=403, detail='Token endpoint disabled in this environment')
    return {'access_token': create_jwt(sub=username)}

@app.post('/v1/triage', response_model=TriageResponse)
def triage_endpoint(req: TriageRequest, authorization: Optional[str] = Header(default=None)):
    user = auth_required(authorization)
    result = triage(req.symptoms, age=req.age)
    return TriageResponse(**result)

@app.get('/v1/symptoms')
def symptoms_catalog(authorization: Optional[str] = Header(default=None)):
    user = auth_required(authorization)
    return sorted(list(SUPPORTED))

@app.get('/v1/faq')
def faq(authorization: Optional[str] = Header(default=None)):
    user = auth_required(authorization)
    return [
        {'q': 'Is this medical advice?', 'a': 'No. This is general information, not a diagnosis.'},
        {'q': 'Do you store my data?', 'a': 'No by default. This demo is stateless.'},
    ]

@app.post('/v1/chat', response_model=ChatResponse)
async def chat(req: ChatRequest, authorization: Optional[str] = Header(default=None)):
    user = auth_required(authorization)
    message = req.message.strip()
    safe_input = redact(message) if settings.redact_logs else message

    llm = LLMClient()
    system = 'You are a careful, helpful assistant for general health information. Avoid definitive diagnoses.'
    # Simulate a small delay to emulate IO-bounded LLM calls
    reply = await asyncio.to_thread(llm.complete, message, system)

    if settings.redact_logs:
        reply = redact(reply)
    return ChatResponse(reply=reply)
