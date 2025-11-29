from typing import List, Dict, Set
import networkx as nx

class EntityResolver:
    """
    Universal Entity Resolution (ID Stitching).
    Links disparate identities across systems into a single canonical ID.
    """
    
    def __init__(self):
        self.graph = nx.Graph()

    def ingest_mappings(self, source: str, mappings: List[Dict[str, str]]):
        """
        Ingest identity pairs.
        e.g. {'email': 'j.doe@example.com', 'user_id': 'u_123'}
        """
        for mapping in mappings:
            # Create edges between all identifiers in the mapping
            ids = list(mapping.values())
            for i in range(len(ids) - 1):
                self.graph.add_edge(ids[i], ids[i+1], source=source)

    def resolve(self, identifier: str) -> str:
        """Return the canonical ID for any identifier."""
        if identifier not in self.graph:
            return identifier
            
        # Canonical ID is the smallest lexicographical ID in the connected component
        component = nx.node_connected_component(self.graph, identifier)
        return min(component)

    def get_all_aliases(self, identifier: str) -> Set[str]:
        """Get all known aliases for an entity."""
        if identifier not in self.graph:
            return {identifier}
        return nx.node_connected_component(self.graph, identifier)
