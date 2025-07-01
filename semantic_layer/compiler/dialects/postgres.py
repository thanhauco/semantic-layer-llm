from .base import SqlDialect

class PostgresDialect(SqlDialect):
    def quote_identifier(self, identifier: str) -> str:
        return f'\"{identifier}\"'
    
    def limit_clause(self, limit: int) -> str:
        return f"LIMIT {limit}"
