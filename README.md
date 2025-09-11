# Semantic Layer for LLM

A robust Semantic Layer bridging data warehouses and Large Language Models.

## Features

- 🎯 **Semantic Modeling**: Define metrics and dimensions declaratively
- 🔌 **Multi-Warehouse**: Support for Postgres, Snowflake, DuckDB, and more
- 🤖 **AI-Powered**: Natural language queries via LLM integration
- 📊 **Smart Analytics**: Anomaly detection and metric recommendations
- 🚀 **Production-Ready**: Caching, optimization, and observability built-in

## Quick Start

```bash
# Install
poetry install

# Define your schema
cat > schema.yaml <<EOF
tables:
  - name: users
    sql_table_name: users
    metrics:
      - name: user_count
        aggregation: count
        sql: id
EOF

# Query
poetry run python -c "
from semantic_layer import SemanticLayer
sl = SemanticLayer.from_yaml('schema.yaml')
print(sl.query(metrics=['user_count']))
"
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Documentation

- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Migration Guide](docs/MIGRATION.md)

## Deployment

```bash
docker-compose up
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
