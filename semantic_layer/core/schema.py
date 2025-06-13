from enum import Enum
from pydantic import BaseModel
from typing import Optional

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    TIMESTAMP = "timestamp"

class Dimension(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataType
    sql: str

class AggregationType(str, Enum):
    SUM = "sum"
    COUNT = "count"
    AVG = "avg"
    MIN = "min"
    MAX = "max"

class Metric(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataType
    aggregation: AggregationType
    sql: str

from typing import List

class Table(BaseModel):
    name: str
    sql_table_name: str
    description: Optional[str] = None
    dimensions: List[Dimension] = []
    metrics: List[Metric] = []

class JoinType(str, Enum):
    LEFT = "left"
    INNER = "inner"
    FULL = "full"

class Join(BaseModel):
    from_table: str
    to_table: str
    type: JoinType
    sql_on: str

class SemanticModel(BaseModel):
    name: str
    tables: List[Table]
    joins: List[Join] = []
