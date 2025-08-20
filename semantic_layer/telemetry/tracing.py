class DistributedTracer:
    def start_span(self, name: str):
        return {"span_id": "123", "trace_id": "456"}
    
    def end_span(self, span):
        pass
