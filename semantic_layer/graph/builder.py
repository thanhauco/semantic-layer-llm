from typing import List
# from semantic_layer.core.schema import SemanticModel
from semantic_layer.graph.store import GraphStore

class KnowledgeGraphBuilder:
    """
    Converts the Semantic Model (Tables, Metrics, Dimensions) into a Graph structure.
    Nodes: Table, Metric, Dimension
    Edges: HAS_DIMENSION, HAS_METRIC, DEPENDS_ON, JOINED_WITH
    """
    
    def __init__(self, graph_store: GraphStore):
        self.store = graph_store

    def build_from_model(self, model):
        """Ingest SemanticModel into GraphDB."""
        print(f"Building Knowledge Graph for model: {model.name}")
        
        for table in model.tables:
            # Create Table Node
            self.store.add_node("Table", {"name": table.name, "sql": table.sql_table_name})
            
            for dim in table.dimensions:
                # Create Dimension Node
                self.store.add_node("Dimension", {"name": dim.name, "type": str(dim.type)})
                # Link Table -> Dimension
                self.store.add_edge(table.name, dim.name, "HAS_DIMENSION")
                
            for metric in table.metrics:
                # Create Metric Node
                self.store.add_node("Metric", {"name": metric.name, "type": str(metric.type)})
                # Link Table -> Metric
                self.store.add_edge(table.name, metric.name, "HAS_METRIC")
                
                # Analyze SQL to find dependencies (simple heuristic)
                for dim in table.dimensions:
                    if dim.name in metric.sql:
                        self.store.add_edge(metric.name, dim.name, "DEPENDS_ON")
