class MetricCatalog:
    def __init__(self):
        self.catalog = {}
    
    def register_metric(self, name: str, metadata: dict):
        self.catalog[name] = metadata
    
    def search(self, query: str) -> list:
        return [k for k in self.catalog.keys() if query.lower() in k.lower()]
