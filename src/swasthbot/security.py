import time, jwt
from typing import Optional
from fastapi import HTTPException, status
from .settings import settings

def create_jwt(sub: str, ttl_seconds: int = 3600) -> str:
    now = int(time.time())
    payload = {
        'sub': sub,
        'iss': settings.jwt_issuer,
        'iat': now,
        'exp': now + ttl_seconds,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm='HS256')

def verify_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=['HS256'], options={'require': ['exp','iat','iss']})
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token')

def auth_required(token: Optional[str]) -> dict:
    if settings.auth_disabled:
        return {'sub': 'dev-user'}
    if not token or not token.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing Bearer token')
    raw = token.split(' ', 1)[1]
    return verify_jwt(raw)
