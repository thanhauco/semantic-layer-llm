import networkx as nx

class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_metric(self, metric_name: str, depends_on: list):
        self.graph.add_node(metric_name)
        for dep in depends_on:
            self.graph.add_edge(dep, metric_name)
    
    def get_dependencies(self, metric_name: str) -> list:
        return list(nx.ancestors(self.graph, metric_name))
    
    def detect_circular_dependencies(self) -> list:
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []
