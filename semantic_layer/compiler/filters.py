from typing import Dict, Any, List

class FilterBuilder:
    @staticmethod
    def build_where_clause(filters: Dict[str, Any]) -> str:
        if not filters:
            return ""
        
        conditions = []
        for key, value in filters.items():
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            elif isinstance(value, (int, float)):
                conditions.append(f"{key} = {value}")
            elif isinstance(value, list):
                values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                conditions.append(f"{key} IN ({values})")
        
        return " AND ".join(conditions) if conditions else ""
