from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QueryResponse(BaseModel):
    sql: str
    data: List[Dict[str, Any]]
    row_count: int
