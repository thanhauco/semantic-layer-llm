from typing import List, Optional, Dict, Any
import numpy as np
# Assuming a vector store client is available
from semantic_layer.ml.vector_store import VectorStore 

class SemanticIntentCache:
    """
    Cache query results based on semantic intent rather than exact SQL match.
    Uses vector embeddings to determine if a new natural language query 
    is semantically equivalent to a cached one.
    """
    
    def __init__(self, vector_store: VectorStore, similarity_threshold: float = 0.95):
        self.vector_store = vector_store
        self.threshold = similarity_threshold
        self.cache_storage = {} # Map hash(intent_vector) -> result

    def get(self, query_embedding: np.ndarray) -> Optional[Dict[str, Any]]:
        """Retrieve cached result if a semantically similar query exists."""
        # Search vector store for nearest neighbor
        matches = self.vector_store.search(query_embedding, top_k=1)
        
        if not matches:
            return None
            
        best_match_key = matches[0]
        # In a real impl, we'd get the score. Assuming search returns (key, score) or we check distance
        # For this stub, we assume a hit implies similarity > threshold logic handled in store or here
        
        return self.cache_storage.get(best_match_key)

    def set(self, query_embedding: np.ndarray, result: Dict[str, Any]):
        """Cache the result keyed by the query embedding."""
        # Generate a consistent key for this embedding (e.g., hash or ID)
        key = str(hash(query_embedding.tobytes()))
        
        # Store vector for future lookups
        self.vector_store.add(key, query_embedding)
        
        # Store actual result
        self.cache_storage[key] = result
