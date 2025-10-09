import requests
from typing import List, Dict, Optional

class SemanticLayerClient:
    """Python SDK for Semantic Layer API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def query(self, metrics: List[str], dimensions: List[str] = None,
             filters: Dict = None, limit: int = None) -> Dict:
        """Execute a semantic query."""
        payload = {
            "metrics": metrics,
            "dimensions": dimensions or [],
            "filters": filters or {},
            "limit": limit
        }
        
        response = self.session.post(f"{self.base_url}/query", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_schema(self) -> Dict:
        """Get semantic model schema."""
        response = self.session.get(f"{self.base_url}/schema")
        response.raise_for_status()
        return response.json()
    
    def list_metrics(self) -> List[Dict]:
        """List all available metrics."""
        response = self.session.get(f"{self.base_url}/metrics")
        response.raise_for_status()
        return response.json()
    
    def natural_language_query(self, question: str) -> Dict:
        """Query using natural language."""
        payload = {"question": question}
        response = self.session.post(f"{self.base_url}/nl-query", json=payload)
        response.raise_for_status()
        return response.json()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.session.close()
