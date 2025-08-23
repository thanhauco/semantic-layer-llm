import hashlib
import json

class RedisCache:
    def __init__(self):
        self.cache = {}  # Mock in-memory cache
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value, ttl: int = 3600):
        self.cache[key] = value
    
    def generate_key(self, query_dict: dict) -> str:
        query_str = json.dumps(query_dict, sort_keys=True)
        return hashlib.md5(query_str.encode()).hexdigest()
