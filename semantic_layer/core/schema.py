from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIMESTAMP = "timestamp"

class AggregationType(str, Enum):
    SUM = "sum"
    COUNT = "count"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT_DISTINCT = "count_distinct"

class Dimension(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataType
    sql: str  # The SQL expression for this dimension
    is_partition: bool = False
    
class Metric(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataType
    aggregation: AggregationType
    sql: str  # The SQL expression to aggregate
    
class Table(BaseModel):
    name: str
    schema_name: str = "public"
    description: Optional[str] = None
    sql_table_name: str
    dimensions: List[Dimension] = []
    metrics: List[Metric] = []
    
    @validator("dimensions")
    def validate_unique_dimensions(cls, v):
        names = [d.name for d in v]
        if len(names) != len(set(names)):
            raise ValueError("Dimension names must be unique within a table")
        return v

class JoinType(str, Enum):
    LEFT = "left"
    INNER = "inner"
    FULL = "full"

class Join(BaseModel):
    to_table: str
    type: JoinType
    sql_on: str

class SemanticModel(BaseModel):
    name: str
    tables: List[Table]
    joins: List[Join] = []
