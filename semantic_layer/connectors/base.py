from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd

class DataSourceAdapter(ABC):
    """Base class for data source adapters."""
    
    @abstractmethod
    def connect(self, connection_params: Dict[str, Any]):
        """Establish connection."""
        pass
    
    @abstractmethod
    def execute_query(self, sql: str) -> pd.DataFrame:
        """Execute SQL and return DataFrame."""
        pass
