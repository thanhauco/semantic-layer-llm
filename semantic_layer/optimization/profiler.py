import time
from contextlib import contextmanager

class QueryProfiler:
    def __init__(self):
        self.profiles = []
    
    @contextmanager
    def profile(self, query_id: str):
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            self.profiles.append({
                "query_id": query_id,
                "duration_ms": duration * 1000,
                "timestamp": time.time()
            })
    
    def get_slow_queries(self, threshold_ms: float = 1000):
        return [p for p in self.profiles if p["duration_ms"] > threshold_ms]
    
    def get_stats(self):
        if not self.profiles:
            return {}
        durations = [p["duration_ms"] for p in self.profiles]
        return {
            "avg_ms": sum(durations) / len(durations),
            "max_ms": max(durations),
            "min_ms": min(durations),
            "total_queries": len(self.profiles)
        }
