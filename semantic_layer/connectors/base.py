from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd

class DataSourceAdapter(ABC):
    """Abstract base class for data source adapters."""
    
    @abstractmethod
    def connect(self, connection_params: Dict[str, Any]):
        """Establish connection to the data source."""
        pass
        
    @abstractmethod
    def execute_query(self, sql: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        pass
        
    @abstractmethod
    def get_tables(self) -> List[str]:
        """List available tables in the data source."""
        pass
        
    @abstractmethod
    def get_schema(self, table_name: str) -> Dict[str, str]:
        """Get column names and types for a table."""
        pass

class PostgresAdapter(DataSourceAdapter):
    def __init__(self):
        self.connection = None
        
    def connect(self, connection_params: Dict[str, Any]):
        # Simulated connection for now
        print(f"Connecting to Postgres with {connection_params}")
        self.connection = "Connected"
        
    def execute_query(self, sql: str) -> pd.DataFrame:
        print(f"Executing Postgres SQL: {sql}")
        # Return dummy data
        return pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        
    def get_tables(self) -> List[str]:
        return ["users", "orders"]
        
    def get_schema(self, table_name: str) -> Dict[str, str]:
        return {"id": "integer", "name": "string"}

class DuckDBAdapter(DataSourceAdapter):
    def __init__(self):
        import duckdb
        self.conn = None
        
    def connect(self, connection_params: Dict[str, Any]):
        import duckdb
        db_path = connection_params.get("database", ":memory:")
        self.conn = duckdb.connect(db_path)
        
    def execute_query(self, sql: str) -> pd.DataFrame:
        return self.conn.execute(sql).df()
        
    def get_tables(self) -> List[str]:
        return [r[0] for r in self.conn.execute("SHOW TABLES").fetchall()]
        
    def get_schema(self, table_name: str) -> Dict[str, str]:
        # Simplified schema fetching
        return {}
