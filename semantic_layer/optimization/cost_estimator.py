from typing import Dict, List
import re

class CostEstimator:
    """Estimate query execution cost for optimization."""
    
    def __init__(self, warehouse_type: str = "snowflake"):
        self.warehouse_type = warehouse_type
        self.cost_per_tb = 5.0  # USD per TB scanned
    
    def estimate_cost(self, sql: str, table_stats: Dict) -> Dict:
        """Estimate query cost based on tables and operations."""
        tables = self._extract_tables(sql)
        
        total_bytes = 0
        for table in tables:
            if table in table_stats:
                total_bytes += table_stats[table]["size_bytes"]
        
        # Estimate based on operations
        complexity_multiplier = 1.0
        if "JOIN" in sql.upper():
            complexity_multiplier *= 1.5
        if "GROUP BY" in sql.upper():
            complexity_multiplier *= 1.2
        if "DISTINCT" in sql.upper():
            complexity_multiplier *= 1.3
        
        estimated_bytes = total_bytes * complexity_multiplier
        estimated_cost = (estimated_bytes / 1e12) * self.cost_per_tb
        
        return {
            "estimated_bytes_scanned": estimated_bytes,
            "estimated_cost_usd": round(estimated_cost, 4),
            "tables_accessed": tables,
            "complexity_score": complexity_multiplier
        }
    
    def _extract_tables(self, sql: str) -> List[str]:
        """Extract table names from SQL."""
        pattern = r'FROM\s+([\w.]+)|JOIN\s+([\w.]+)'
        matches = re.findall(pattern, sql, re.IGNORECASE)
        tables = [m[0] or m[1] for m in matches]
        return list(set(tables))
    
    def suggest_optimizations(self, sql: str, cost: Dict) -> List[str]:
        """Suggest query optimizations to reduce cost."""
        suggestions = []
        
        if cost["estimated_cost_usd"] > 1.0:
            suggestions.append("Consider materializing this query for reuse")
        
        if "SELECT *" in sql:
            suggestions.append("Select only required columns instead of SELECT *")
        
        if cost["complexity_score"] > 2.0:
            suggestions.append("Query is complex - consider breaking into CTEs")
        
        return suggestions
