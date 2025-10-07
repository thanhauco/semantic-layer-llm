from typing import Callable, Dict, Any
import asyncio

class RealtimeMetrics:
    """Real-time metric computation from streaming data."""
    
    def __init__(self):
        self.subscribers = {}
        self.aggregations = {}
    
    async def subscribe(self, metric_name: str, callback: Callable):
        """Subscribe to real-time metric updates."""
        if metric_name not in self.subscribers:
            self.subscribers[metric_name] = []
        self.subscribers[metric_name].append(callback)
    
    async def process_event(self, event: Dict[str, Any]):
        """Process incoming event and update metrics."""
        # Update aggregations
        for metric_name in self.subscribers:
            if metric_name in self.aggregations:
                self.aggregations[metric_name] = self._update_aggregation(
                    self.aggregations[metric_name], event
                )
                # Notify subscribers
                for callback in self.subscribers[metric_name]:
                    await callback(self.aggregations[metric_name])
    
    def _update_aggregation(self, current_value: Any, event: Dict) -> Any:
        """Update aggregation with new event."""
        # Implement sliding window aggregation
        return current_value + event.get("value", 0)
    
    async def get_current_value(self, metric_name: str) -> Any:
        """Get current real-time value of metric."""
        return self.aggregations.get(metric_name, 0)
