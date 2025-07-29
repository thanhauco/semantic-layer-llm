from typing import Dict, List
import os

class LLMInterface:
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def text_to_query(self, text: str, schema_context: Dict) -> Dict:
        # Mock implementation
        return {"metrics": [], "dimensions": []}
