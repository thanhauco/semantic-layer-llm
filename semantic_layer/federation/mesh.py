from typing import Dict, Any
import requests

class DataMeshNode:
    """
    Protocol for federated Semantic Layers.
    Allows nodes to subscribe to metrics from other domains (Marketing, Finance).
    """
    
    def __init__(self, domain_name: str, registry_url: str):
        self.domain = domain_name
        self.registry = registry_url
        self.peers = {}

    def register_peer(self, domain: str, url: str):
        """Connect to another Semantic Layer node."""
        self.peers[domain] = url

    def fetch_remote_metric(self, domain: str, metric_name: str) -> Dict[str, Any]:
        """Query a metric from a peer node."""
        if domain not in self.peers:
            raise ValueError(f"Unknown domain: {domain}")
            
        url = self.peers[domain]
        # Call remote Semantic Layer API
        response = requests.post(f"{url}/query", json={
            "metrics": [metric_name],
            "federated_from": self.domain
        })
        return response.json()

    def publish_catalog(self):
        """Publish available metrics to the central mesh registry."""
        pass
