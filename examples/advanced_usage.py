# Advanced Usage Examples

from semantic_layer.sdk.client import SemanticLayerClient
from semantic_layer.advanced.materialization import IncrementalMaterialization
from semantic_layer.ai.query_suggestions import QuerySuggestions

# Example 1: Using the SDK
with SemanticLayerClient("http://localhost:8000", api_key="your-key") as client:
    result = client.query(
        metrics=["revenue", "user_count"],
        dimensions=["country", "date"],
        filters={"date": {"$gte": "2025-10-01"}}
    )
    print(result)

# Example 2: Incremental Materialization
materializer = IncrementalMaterialization()
materializer.materialize(
    metric_name="daily_revenue",
    sql="SELECT date, SUM(amount) as revenue FROM orders GROUP BY date",
    partition_by="date"
)

# Example 3: AI Query Suggestions
suggestions = QuerySuggestions()
suggestions.track_query(["revenue"], ["country"])
next_dims = suggestions.suggest_next_dimension(["revenue"])
print(f"Suggested dimensions: {next_dims}")

# Example 4: Natural Language Query
result = client.natural_language_query("Show me revenue by country for last month")
print(result)
