import hashlib
import json
import time
from typing import Optional, Dict, Any

class SmartCache:
    """Intelligent caching with TTL and dependency tracking."""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache = {}
        self.default_ttl = default_ttl
        self.dependencies = {}  # Track metric dependencies
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry["expires_at"]:
                entry["hits"] += 1
                return entry["value"]
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expires_at = time.time() + (ttl or self.default_ttl)
        self.cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": time.time(),
            "hits": 0
        }
    
    def invalidate_by_table(self, table_name: str):
        """Invalidate all cached queries that depend on a table."""
        keys_to_delete = []
        for key, entry in self.cache.items():
            if table_name in entry.get("dependencies", []):
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.cache[key]
        
        return len(keys_to_delete)
    
    def get_stats(self) -> Dict:
        total_hits = sum(e["hits"] for e in self.cache.values())
        return {
            "total_entries": len(self.cache),
            "total_hits": total_hits,
            "cache_size_mb": sum(len(str(e["value"])) for e in self.cache.values()) / 1024 / 1024
        }
