import pytest
from semantic_layer.core.schema import *
from semantic_layer.compiler.sql_compiler import SqlCompiler
from semantic_layer.compiler.query import QueryRequest

def test_basic_query():
    table = Table(
        name="users",
        sql_table_name="users",
        dimensions=[Dimension(name="country", type=DataType.STRING, sql="country")],
        metrics=[Metric(name="count", type=DataType.INTEGER, aggregation=AggregationType.COUNT, sql="id")]
    )
    model = SemanticModel(name="test", tables=[table])
    compiler = SqlCompiler(model)
    
    request = QueryRequest(metrics=["count"], dimensions=["country"])
    sql = compiler.compile(request)
    
    assert "SELECT" in sql
    assert "GROUP BY" in sql
