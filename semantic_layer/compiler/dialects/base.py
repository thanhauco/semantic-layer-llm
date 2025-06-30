from abc import ABC, abstractmethod

class SqlDialect(ABC):
    @abstractmethod
    def quote_identifier(self, identifier: str) -> str:
        pass
    
    @abstractmethod
    def limit_clause(self, limit: int) -> str:
        pass
