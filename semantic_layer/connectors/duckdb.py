from .base import DataSourceAdapter
from typing import Dict, Any
import pandas as pd
import duckdb

class DuckDBAdapter(DataSourceAdapter):
    def __init__(self):
        self.conn = None
    
    def connect(self, connection_params: Dict[str, Any]):
        db_path = connection_params.get("database", ":memory:")
        self.conn = duckdb.connect(db_path)
    
    def execute_query(self, sql: str) -> pd.DataFrame:
        return self.conn.execute(sql).df()
