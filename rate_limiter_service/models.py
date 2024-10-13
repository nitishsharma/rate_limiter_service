from pydantic import BaseModel

class RateLimitRequest(BaseModel):
    client_id: str

class RateLimitResponse(BaseModel):
    allowed: bool
    message: str
