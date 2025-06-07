import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from semantic_layer.core.schema import SemanticModel, Table, Dimension, Metric, DataType, AggregationType
from semantic_layer.compiler.query_compiler import SqlCompiler, QueryRequest
from semantic_layer.ml.llm_interface import LLMInterface
from semantic_layer.ml.anomaly_detection import AnomalyDetector

def test_flow():
    print("1. Defining Schema...")
    users_table = Table(
        name="users",
        sql_table_name="users",
        dimensions=[
            Dimension(name="user_id", type=DataType.INTEGER, sql="users.id"),
            Dimension(name="country", type=DataType.STRING, sql="users.country")
        ],
        metrics=[
            Metric(name="total_users", type=DataType.INTEGER, aggregation=AggregationType.COUNT, sql="users.id")
        ]
    )
    model = SemanticModel(name="ecommerce", tables=[users_table])
    print("   Schema defined successfully.")

    print("2. Compiling Query...")
    compiler = SqlCompiler(model)
    request = QueryRequest(metrics=["total_users"], dimensions=["country"])
    sql = compiler.compile(request)
    print(f"   Generated SQL: {sql}")
    assert "SELECT" in sql
    assert "GROUP BY" in sql

    print("3. Testing LLM Interface...")
    llm = LLMInterface(provider="mock")
    semantic_query = llm.generate_semantic_query("Show me total users by country", {})
    print(f"   LLM Output: {semantic_query}")
    assert "total_users" in semantic_query["metrics"]
    assert "country" in semantic_query["dimensions"]

    print("4. Testing Anomaly Detection...")
    detector = AnomalyDetector()
    # Create dummy data
    data = pd.DataFrame({
        "total_users": [100, 102, 98, 105, 1000, 101] # 1000 is anomaly
    })
    detector.fit(data, "total_users")
    anomalies = detector.detect(data, "total_users")
    print(f"   Anomalies detected: {anomalies}")
    assert anomalies[4] == True # The 1000 should be an anomaly

    print("\nAll systems operational!")

if __name__ == "__main__":
    test_flow()
