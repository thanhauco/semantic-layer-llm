from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class LineageNode:
    name: str
    type: str  # table, metric, dimension
    dependencies: List[str]

class DataLineage:
    """Track data lineage for metrics and dimensions."""
    
    def __init__(self):
        self.graph = {}
    
    def add_node(self, node: LineageNode):
        self.graph[node.name] = node
    
    def get_upstream_dependencies(self, node_name: str) -> Set[str]:
        """Get all upstream dependencies (recursive)."""
        if node_name not in self.graph:
            return set()
        
        dependencies = set()
        node = self.graph[node_name]
        
        for dep in node.dependencies:
            dependencies.add(dep)
            dependencies.update(self.get_upstream_dependencies(dep))
        
        return dependencies
    
    def get_downstream_impact(self, node_name: str) -> Set[str]:
        """Get all metrics/dimensions that depend on this node."""
        impacted = set()
        for name, node in self.graph.items():
            if node_name in node.dependencies:
                impacted.add(name)
                impacted.update(self.get_downstream_impact(name))
        return impacted
    
    def generate_lineage_diagram(self, metric_name: str) -> str:
        """Generate mermaid diagram for lineage."""
        upstream = self.get_upstream_dependencies(metric_name)
        
        diagram = "graph TD\n"
        for dep in upstream:
            diagram += f"    {dep} --> {metric_name}\n"
        
        return diagram
