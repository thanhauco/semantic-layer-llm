import time

class PerformanceMonitor:
    def __init__(self):
        self.timings = {}
    
    def measure(self, operation_name: str):
        start = time.time()
        yield
        duration = time.time() - start
        self.timings[operation_name] = duration
