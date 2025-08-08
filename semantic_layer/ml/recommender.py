from typing import List, Dict

class MetricRecommender:
    def __init__(self):
        self.usage_history = []
    
    def track_query(self, metrics: List[str]):
        self.usage_history.append(metrics)
    
    def recommend(self, current_metric: str, top_k: int = 3) -> List[str]:
        # Simple co-occurrence based recommendation
        related = {}
        for query in self.usage_history:
            if current_metric in query:
                for m in query:
                    if m != current_metric:
                        related[m] = related.get(m, 0) + 1
        
        sorted_metrics = sorted(related.items(), key=lambda x: x[1], reverse=True)
        return [m[0] for m in sorted_metrics[:top_k]]
