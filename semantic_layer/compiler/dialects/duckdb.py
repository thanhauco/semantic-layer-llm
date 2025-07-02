from .base import SqlDialect

class DuckDBDialect(SqlDialect):
    def quote_identifier(self, identifier: str) -> str:
        return f'\"{identifier}\"'
    
    def limit_clause(self, limit: int) -> str:
        return f"LIMIT {limit}"
