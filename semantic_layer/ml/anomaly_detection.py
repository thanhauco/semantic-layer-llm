import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
    
    def fit(self, data: pd.DataFrame, metric_col: str):
        X = data[[metric_col]].values
        self.model.fit(X)
    
    def detect(self, data: pd.DataFrame, metric_col: str) -> list:
        X = data[[metric_col]].values
        predictions = self.model.predict(X)
        return [p == -1 for p in predictions]
