class MetricAlerts:
    def __init__(self):
        self.alerts = []
    
    def create_alert(self, metric: str, condition: str, threshold: float):
        self.alerts.append({
            "metric": metric,
            "condition": condition,
            "threshold": threshold,
            "enabled": True
        })
    
    def check_alerts(self, metric_values: dict) -> list:
        triggered = []
        for alert in self.alerts:
            if alert["enabled"]:
                value = metric_values.get(alert["metric"])
                if value and self._evaluate_condition(value, alert):
                    triggered.append(alert)
        return triggered
    
    def _evaluate_condition(self, value, alert):
        if alert["condition"] == ">":
            return value > alert["threshold"]
        elif alert["condition"] == "<":
            return value < alert["threshold"]
        return False
