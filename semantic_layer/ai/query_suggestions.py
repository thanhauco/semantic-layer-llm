from typing import List, Dict
import re

class QuerySuggestions:
    """AI-powered query suggestions based on usage patterns."""
    
    def __init__(self):
        self.query_history = []
        self.popular_combinations = {}
    
    def track_query(self, metrics: List[str], dimensions: List[str]):
        """Track query for pattern learning."""
        self.query_history.append({
            "metrics": metrics,
            "dimensions": dimensions
        })
        
        # Update popular combinations
        key = tuple(sorted(metrics + dimensions))
        self.popular_combinations[key] = self.popular_combinations.get(key, 0) + 1
    
    def suggest_next_dimension(self, current_metrics: List[str]) -> List[str]:
        """Suggest dimensions based on current metrics."""
        suggestions = {}
        
        for query in self.query_history:
            if any(m in query["metrics"] for m in current_metrics):
                for dim in query["dimensions"]:
                    suggestions[dim] = suggestions.get(dim, 0) + 1
        
        # Return top 3 suggestions
        sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_suggestions[:3]]
    
    def suggest_related_metrics(self, current_metric: str) -> List[str]:
        """Suggest related metrics often queried together."""
        related = {}
        
        for query in self.query_history:
            if current_metric in query["metrics"]:
                for metric in query["metrics"]:
                    if metric != current_metric:
                        related[metric] = related.get(metric, 0) + 1
        
        sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)
        return [r[0] for r in sorted_related[:5]]
    
    def detect_query_patterns(self) -> List[Dict]:
        """Detect common query patterns for optimization."""
        patterns = []
        
        # Find most popular combinations
        for combo, count in sorted(self.popular_combinations.items(), 
                                   key=lambda x: x[1], reverse=True)[:5]:
            patterns.append({
                "fields": list(combo),
                "frequency": count,
                "suggestion": "Consider creating a materialized view"
            })
        
        return patterns
