# Example Queries

from semantic_layer import SemanticLayer

sl = SemanticLayer.from_yaml("schema.yaml")

# Example 1: Simple aggregation
result = sl.query(
    metrics=["revenue"],
    dimensions=["country"]
)

# Example 2: With filters
result = sl.query(
    metrics=["user_count"],
    dimensions=["date"],
    filters={"country": "US"}
)

# Example 3: Natural language
result = sl.query_natural_language(
    "Show me revenue by country for last month"
)
