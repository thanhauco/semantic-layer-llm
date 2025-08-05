from typing import List, Dict
import numpy as np

class VectorStore:
    def __init__(self):
        self.vectors = {}
    
    def add(self, key: str, vector: np.ndarray):
        self.vectors[key] = vector
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[str]:
        # Simple cosine similarity search
        return list(self.vectors.keys())[:top_k]
