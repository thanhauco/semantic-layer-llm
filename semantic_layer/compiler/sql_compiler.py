from semantic_layer.core.schema import SemanticModel
from .query import QueryRequest

class SqlCompiler:
    def __init__(self, model: SemanticModel):
        self.model = model
    
    def compile(self, request: QueryRequest) -> str:
        """Compile semantic query to SQL."""
        # TODO: Implement compilation logic
        return "SELECT 1"
