"""
Semantic Layer for LLM

A robust semantic layer bridging data warehouses and Large Language Models.
"""

__version__ = "0.1.0"
__author__ = "Semantic Layer Contributors"

from .core.schema import (
    Dimension,
    Metric,
    Table,
    SemanticModel,
    DataType,
    AggregationType
)
from .compiler.sql_compiler import SqlCompiler
from .compiler.query import QueryRequest

__all__ = [
    "Dimension",
    "Metric",
    "Table",
    "SemanticModel",
    "DataType",
    "AggregationType",
    "SqlCompiler",
    "QueryRequest",
]
