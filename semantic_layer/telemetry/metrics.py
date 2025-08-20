class MetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def record(self, metric_name: str, value: float):
        self.metrics[metric_name] = value
