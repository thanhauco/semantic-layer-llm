from typing import List, Optional, Dict
from semantic_layer.core.schema import SemanticModel, Metric, Dimension, Table, Join

class QueryRequest:
    def __init__(self, metrics: List[str], dimensions: List[str], filters: Optional[Dict] = None):
        self.metrics = metrics
        self.dimensions = dimensions
        self.filters = filters or {}

class SqlCompiler:
    def __init__(self, model: SemanticModel):
        self.model = model
        
    def compile(self, request: QueryRequest) -> str:
        """
        Compiles a semantic query into a SQL statement.
        """
        # 1. Identify required tables
        # For simplicity, assuming all metrics/dimensions are in the first table or joined ones
        # Real implementation would need a graph traversal to find the optimal join path.
        
        select_clause = []
        group_by_clause = []
        
        # Resolve Dimensions
        for dim_name in request.dimensions:
            dim = self._find_dimension(dim_name)
            if dim:
                select_clause.append(f"{dim.sql} AS {dim.name}")
                group_by_clause.append(f"{dim.name}") # Or index
            else:
                raise ValueError(f"Dimension {dim_name} not found")
                
        # Resolve Metrics
        for metric_name in request.metrics:
            metric = self._find_metric(metric_name)
            if metric:
                select_clause.append(f"{metric.aggregation.value}({metric.sql}) AS {metric.name}")
            else:
                raise ValueError(f"Metric {metric_name} not found")
                
        # Construct Query
        # Assuming single table for now for MVP
        primary_table = self.model.tables[0]
        
        sql = f"SELECT {', '.join(select_clause)} FROM {primary_table.sql_table_name}"
        
        # Add Joins (simplified)
        for join in self.model.joins:
            sql += f" {join.type.value.upper()} JOIN {join.to_table} ON {join.sql_on}"
            
        if group_by_clause:
            sql += f" GROUP BY {', '.join(group_by_clause)}"
            
        return sql
        
    def _find_dimension(self, name: str) -> Optional[Dimension]:
        for table in self.model.tables:
            for dim in table.dimensions:
                if dim.name == name:
                    return dim
        return None
        
    def _find_metric(self, name: str) -> Optional[Metric]:
        for table in self.model.tables:
            for metric in table.metrics:
                if metric.name == name:
                    return metric
        return None
