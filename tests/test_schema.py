import pytest
from semantic_layer.core.schema import (
    Dimension, Metric, Table, DataType, AggregationType
)

def test_dimension_creation():
    dim = Dimension(
        name="user_id",
        type=DataType.INTEGER,
        sql="users.id"
    )
    assert dim.name == "user_id"
    assert dim.type == DataType.INTEGER

def test_metric_creation():
    metric = Metric(
        name="total_users",
        type=DataType.INTEGER,
        aggregation=AggregationType.COUNT,
        sql="users.id"
    )
    assert metric.aggregation == AggregationType.COUNT

def test_table_with_dimensions_and_metrics():
    dim = Dimension(name="country", type=DataType.STRING, sql="users.country")
    metric = Metric(name="user_count", type=DataType.INTEGER, 
                   aggregation=AggregationType.COUNT, sql="users.id")
    
    table = Table(
        name="users",
        sql_table_name="public.users",
        dimensions=[dim],
        metrics=[metric]
    )
    assert len(table.dimensions) == 1
    assert len(table.metrics) == 1
