from typing import Dict, Any, Callable
import requests

class ActionTrigger:
    """
    Defines operational actions triggered by metric conditions.
    Turns the semantic layer into an active automation engine.
    """
    
    def __init__(self):
        self.triggers = []

    def register_trigger(self, metric: str, condition: str, action_config: Dict):
        """
        Register a new action trigger.
        Example: If 'churn_rate' > 0.05, call 'webhook_url'
        """
        self.triggers.append({
            "metric": metric,
            "condition": condition,
            "config": action_config
        })

    def evaluate(self, metric_values: Dict[str, Any]):
        for trigger in self.triggers:
            val = metric_values.get(trigger["metric"])
            if val is not None and self._check_condition(val, trigger["condition"]):
                self._execute_action(trigger["config"], val)

    def _check_condition(self, value, condition: str) -> bool:
        # Simple eval (in prod use AST or safe eval)
        # e.g. "> 5"
        op, threshold = condition.split()
        threshold = float(threshold)
        if op == ">": return value > threshold
        if op == "<": return value < threshold
        return False

    def _execute_action(self, config: Dict, value):
        action_type = config.get("type")
        if action_type == "webhook":
            requests.post(config["url"], json={
                "alert": "Metric Threshold Breached",
                "value": value,
                "payload": config.get("payload")
            })
            print(f"Triggered webhook for value {value}")
