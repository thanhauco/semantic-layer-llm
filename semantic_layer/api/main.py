from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI(title="Semantic Layer API")

class QueryPayload(BaseModel):
    metrics: List[str]
    dimensions: List[str] = []
    filters: Optional[Dict[str, Any]] = None

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/query")
def execute_query(payload: QueryPayload):
    # TODO: Integrate with compiler
    return {"sql": "SELECT 1", "data": []}
