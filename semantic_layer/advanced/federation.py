class QueryFederation:
    """Federate queries across multiple data sources."""
    
    def __init__(self):
        self.sources = {}
    
    def register_source(self, name: str, connector):
        self.sources[name] = connector
    
    def federated_query(self, query_plan: dict) -> list:
        results = []
        for source_name, sub_query in query_plan.items():
            if source_name in self.sources:
                result = self.sources[source_name].execute(sub_query)
                results.append(result)
        return self._merge_results(results)
    
    def _merge_results(self, results: list):
        # Merge results from multiple sources
        return results
