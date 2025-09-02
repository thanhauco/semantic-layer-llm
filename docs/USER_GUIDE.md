# User Guide

## Getting Started

### Installation
```bash
poetry install
```

### Define Your Schema
Create a YAML file defining your metrics and dimensions:

```yaml
tables:
  - name: users
    sql_table_name: public.users
    dimensions:
      - name: country
        type: string
        sql: country
    metrics:
      - name: user_count
        type: integer
        aggregation: count
        sql: id
```

### Query Your Data
```python
from semantic_layer import SemanticLayer

sl = SemanticLayer.from_yaml("schema.yaml")
result = sl.query(
    metrics=["user_count"],
    dimensions=["country"]
)
```

## Advanced Features

### Natural Language Queries
```python
result = sl.query_natural_language("Show me users by country")
```

### Anomaly Detection
```python
anomalies = sl.detect_anomalies(metric="revenue", window="7d")
```
