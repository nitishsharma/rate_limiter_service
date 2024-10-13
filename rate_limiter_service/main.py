from fastapi import FastAPI, Depends, HTTPException
from .models import RateLimitRequest, RateLimitResponse
from .services.rate_limiter import RedisRateLimiter

app = FastAPI()

# Initialize rate limiter with Redis
rate_limiter = RedisRateLimiter()

@app.post("/check_rate_limit", response_model=RateLimitResponse)
async def check_rate_limit(request: RateLimitRequest):
    client_id = request.client_id

    # Check if the client is allowed to make a request
    if rate_limiter.is_allowed(client_id):
        return RateLimitResponse(allowed=True, message="Request allowed")
    else:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
