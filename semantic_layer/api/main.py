from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from semantic_layer.core.schema import SemanticModel, Table, Dimension, Metric, DataType, AggregationType
from semantic_layer.compiler.query_compiler import SqlCompiler, QueryRequest

app = FastAPI(title="Semantic Layer API", version="0.1.0")

# Dummy Model for testing
def get_dummy_model():
    users_table = Table(
        name="users",
        sql_table_name="users",
        dimensions=[
            Dimension(name="user_id", type=DataType.INTEGER, sql="users.id"),
            Dimension(name="country", type=DataType.STRING, sql="users.country")
        ],
        metrics=[
            Metric(name="total_users", type=DataType.INTEGER, aggregation=AggregationType.COUNT, sql="users.id")
        ]
    )
    return SemanticModel(name="ecommerce", tables=[users_table])

model = get_dummy_model()
compiler = SqlCompiler(model)

class QueryPayload(BaseModel):
    metrics: List[str]
    dimensions: List[str] = []
    filters: Optional[dict] = None

@app.get("/")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/query")
def run_query(payload: QueryPayload):
    try:
        request = QueryRequest(metrics=payload.metrics, dimensions=payload.dimensions, filters=payload.filters)
        sql = compiler.compile(request)
        # In a real app, we would execute this SQL against the adapter
        return {"sql": sql, "data": []}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
