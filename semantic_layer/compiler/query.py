from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    metrics: List[str]
    dimensions: List[str] = []
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = None
