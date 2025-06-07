import pandas as pd
import numpy as np
from typing import List, Dict

class AnomalyDetector:
    def __init__(self, model_type: str = "isolation_forest"):
        self.model_type = model_type
        self.model = None
        
    def fit(self, data: pd.DataFrame, metric_col: str):
        """
        Fits an anomaly detection model on the given metric history.
        """
        from sklearn.ensemble import IsolationForest
        
        X = data[[metric_col]].values
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(X)
        
    def detect(self, data: pd.DataFrame, metric_col: str) -> List[bool]:
        """
        Returns a boolean list indicating if each point is an anomaly.
        """
        if not self.model:
            raise ValueError("Model not fitted")
            
        X = data[[metric_col]].values
        preds = self.model.predict(X)
        # -1 is anomaly, 1 is normal
        return [p == -1 for p in preds]

class Recommender:
    def suggest_related_metrics(self, current_metric: str, usage_history: List[Dict]) -> List[str]:
        """
        Suggests metrics that are often queried together with the current metric.
        """
        # Simple co-occurrence logic
        related = {}
        for query in usage_history:
            metrics = query.get("metrics", [])
            if current_metric in metrics:
                for m in metrics:
                    if m != current_metric:
                        related[m] = related.get(m, 0) + 1
                        
        sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)
        return [x[0] for x in sorted_related[:3]]
