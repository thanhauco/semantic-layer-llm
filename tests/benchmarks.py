import time
from semantic_layer.compiler.sql_compiler import SqlCompiler

def benchmark_query_compilation():
    # Benchmark SQL compilation
    start = time.time()
    for _ in range(1000):
        # Compile query
        pass
    duration = time.time() - start
    print(f"1000 compilations: {duration:.2f}s")

if __name__ == "__main__":
    benchmark_query_compilation()
