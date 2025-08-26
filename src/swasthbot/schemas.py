from pydantic import BaseModel, Field, conlist
from typing import List, Optional

class HealthResponse(BaseModel):
    app: str
    env: str
    status: str = 'ok'

class TriageRequest(BaseModel):
    symptoms: conlist(str, min_length=1) = Field(..., description='List of symptoms in plain English')
    age: Optional[int] = Field(default=None, ge=0, le=120)

class TriageResponse(BaseModel):
    level: str
    reasons: List[str]
    unknown_symptoms: List[str]

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=2000)

class ChatResponse(BaseModel):
    reply: str
