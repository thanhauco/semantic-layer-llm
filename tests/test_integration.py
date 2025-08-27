import pytest
from semantic_layer.core.schema import *
from semantic_layer.compiler.sql_compiler import SqlCompiler
from semantic_layer.compiler.query import QueryRequest

def test_end_to_end_query_execution():
    # Setup model
    table = Table(
        name="users",
        sql_table_name="users",
        dimensions=[
            Dimension(name="country", type=DataType.STRING, sql="country"),
            Dimension(name="age_group", type=DataType.STRING, sql="age_group")
        ],
        metrics=[
            Metric(name="user_count", type=DataType.INTEGER, 
                   aggregation=AggregationType.COUNT, sql="id")
        ]
    )
    model = SemanticModel(name="test", tables=[table])
    
    # Compile query
    compiler = SqlCompiler(model)
    request = QueryRequest(
        metrics=["user_count"],
        dimensions=["country"],
        filters={"age_group": "18-25"}
    )
    
    sql = compiler.compile(request)
    
    assert "SELECT" in sql
    assert "country" in sql
    assert "COUNT" in sql
    assert "GROUP BY" in sql

def test_multi_metric_query():
    table = Table(
        name="orders",
        sql_table_name="orders",
        dimensions=[Dimension(name="date", type=DataType.DATE, sql="order_date")],
        metrics=[
            Metric(name="order_count", type=DataType.INTEGER, 
                   aggregation=AggregationType.COUNT, sql="id"),
            Metric(name="revenue", type=DataType.FLOAT, 
                   aggregation=AggregationType.SUM, sql="amount")
        ]
    )
    model = SemanticModel(name="test", tables=[table])
    compiler = SqlCompiler(model)
    
    request = QueryRequest(
        metrics=["order_count", "revenue"],
        dimensions=["date"]
    )
    
    sql = compiler.compile(request)
    assert "COUNT" in sql
    assert "SUM" in sql
