import redis
import time

class RedisRateLimiter:
    def __init__(self, redis_host='localhost', redis_port=6379, bucket_capacity=100, refill_rate=10):
        # Initialize Redis client and rate limiting configuration
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.bucket_capacity = bucket_capacity  # Max number of tokens
        self.refill_rate = refill_rate  # Tokens refilled per second

    def is_allowed(self, client_id: str) -> bool:
        # Current timestamp in seconds
        current_time = int(time.time())

        # Get client's token bucket from Redis
        bucket = self.redis.hgetall(client_id)

        # If no bucket exists, create a new one with full capacity
        if not bucket:
            self.redis.hset(client_id, mapping={"tokens": self.bucket_capacity, "last_refill": current_time})
            return True

        tokens = int(bucket.get(b"tokens", 0))
        last_refill = int(bucket.get(b"last_refill", 0))

        # Calculate the time elapsed since the last refill
        elapsed_time = current_time - last_refill

        # Refill the tokens based on the elapsed time
        new_tokens = min(self.bucket_capacity, tokens + elapsed_time * self.refill_rate)

        # If tokens are available, allow the request and decrement a token
        if new_tokens > 0:
            self.redis.hset(client_id, mapping={"tokens": new_tokens - 1, "last_refill": current_time})
            return True
        else:
            # Otherwise, deny the request
            return False

    def reset_client(self, client_id: str):
        # Reset client's token bucket (optional)
        self.redis.delete(client_id)
