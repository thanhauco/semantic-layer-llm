from semantic_layer.core.schema import SemanticModel, Dimension, Metric
from .query import QueryRequest
from typing import Optional

class SqlCompiler:
    def __init__(self, model: SemanticModel):
        self.model = model
    
    def compile(self, request: QueryRequest) -> str:
        """Compile semantic query to SQL."""
        select_parts = []
        
        # Add dimensions
        for dim_name in request.dimensions:
            dim = self._find_dimension(dim_name)
            if dim:
                select_parts.append(f"{dim.sql} AS {dim.name}")
        
        # Add metrics
        for metric_name in request.metrics:
            metric = self._find_metric(metric_name)
            if metric:
                select_parts.append(
                    f"{metric.aggregation.value}({metric.sql}) AS {metric.name}"
                )
        
        # Build query
        table = self.model.tables[0]  # Simplified: use first table
        sql = f"SELECT {', '.join(select_parts)} FROM {table.sql_table_name}"
        
        if request.dimensions:
            sql += f" GROUP BY {', '.join(request.dimensions)}"
        
        if request.limit:
            sql += f" LIMIT {request.limit}"
        
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
