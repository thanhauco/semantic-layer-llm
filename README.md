# Semantic Layer for LLM

A production-ready Semantic Layer bridging data warehouses and Large Language Models with advanced ML capabilities.

## ✨ Features

### Core Capabilities
- 🎯 **Declarative Schema**: Define metrics and dimensions using Pydantic models or YAML
- 🔌 **Multi-Warehouse Support**: Postgres, Snowflake, DuckDB adapters with dialect-specific SQL generation
- 📊 **Advanced SQL Compiler**: Automatic JOIN resolution, WHERE/HAVING clauses, ORDER BY, aggregations
- 🔄 **Query Optimization**: Cost estimation, query plan analysis, and automatic optimization

### AI & Machine Learning
- 🤖 **LLM Integration**: Natural language to SQL query translation
- 🔍 **Semantic Search**: Vector store for schema context retrieval
- 📈 **Anomaly Detection**: Isolation Forest-based metric anomaly detection
- 💡 **Smart Recommendations**: ML-powered related metrics suggestions

### Production Features
- ⚡ **Redis Caching**: Query result caching with intelligent invalidation
- 📡 **Observability**: OpenTelemetry integration, distributed tracing, metrics collection
- 🔐 **Security**: JWT authentication, RBAC, SQL injection protection
- 🎨 **UI**: Streamlit-based query builder and metric explorer

### APIs
- 🌐 **REST API**: FastAPI-based endpoints with automatic validation
- 🔗 **GraphQL**: Full GraphQL schema and resolvers
- 📚 **Comprehensive Docs**: API documentation, user guides, examples

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd infrared-cluster

# Install dependencies
poetry install
```

### Define Your Schema

Create a semantic model using Python:

```python
from semantic_layer.core.schema import *

# Define your model
users_table = Table(
    name="users",
    sql_table_name="public.users",
    dimensions=[
        Dimension(name="country", type=DataType.STRING, sql="country"),
        Dimension(name="signup_date", type=DataType.DATE, sql="created_at::date")
    ],
    metrics=[
        Metric(name="user_count", type=DataType.INTEGER, 
               aggregation=AggregationType.COUNT, sql="id"),
        Metric(name="active_users", type=DataType.INTEGER,
               aggregation=AggregationType.COUNT, sql="CASE WHEN active THEN id END")
    ]
)

model = SemanticModel(name="analytics", tables=[users_table])
```

### Execute Queries

```python
from semantic_layer.compiler.sql_compiler import SqlCompiler
from semantic_layer.compiler.query import QueryRequest

# Compile a query
compiler = SqlCompiler(model)
request = QueryRequest(
    metrics=["user_count", "active_users"],
    dimensions=["country"],
    filters={"signup_date": {"$gte": "2025-01-01"}},
    order_by=["country"]
)

sql = compiler.compile(request)
print(sql)
# Output: SELECT country AS country, COUNT(id) AS user_count, 
#         COUNT(CASE WHEN active THEN id END) AS active_users 
#         FROM public.users WHERE signup_date >= '2025-01-01' 
#         GROUP BY country ORDER BY country ASC
```

## 🏃 Running the Application

### Start the API Server

```bash
# Development mode with auto-reload
poetry run uvicorn semantic_layer.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
poetry run uvicorn semantic_layer.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

### Launch the UI

```bash
# Start Streamlit UI
poetry run streamlit run semantic_layer/ui/app.py
```

Access the UI at `http://localhost:8501`

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Deploy to Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f deploy/k8s-deployment.yaml

# Check deployment status
kubectl get pods -l app=semantic-layer
```

## 📖 Usage Examples

### REST API Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["user_count"],
    "dimensions": ["country"],
    "filters": {"country": "US"},
    "limit": 10
  }'
```

### Natural Language Query (with LLM)

```python
from semantic_layer.ml.llm_interface import LLMInterface

llm = LLMInterface(provider="openai")
result = llm.text_to_query(
    "Show me total users by country for the last month",
    schema_context=model.dict()
)
# Returns: {"metrics": ["user_count"], "dimensions": ["country"], ...}
```

### Anomaly Detection

```python
from semantic_layer.ml.anomaly_detection import AnomalyDetector
import pandas as pd

detector = AnomalyDetector()
data = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=30),
    "revenue": [100, 105, 98, 102, 500, 99, ...]  # 500 is anomaly
})

detector.fit(data, "revenue")
anomalies = detector.detect(data, "revenue")
print(f"Anomalies found at indices: {[i for i, a in enumerate(anomalies) if a]}")
```

## 🧪 Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=semantic_layer --cov-report=html

# Run specific test file
poetry run pytest tests/test_compiler.py

# Run integration tests
poetry run pytest tests/test_integration.py
```

## 📚 Documentation

- **[API Documentation](docs/API.md)** - REST and GraphQL endpoint reference
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and components
- **[User Guide](docs/USER_GUIDE.md)** - Detailed usage instructions
- **[Migration Guide](docs/MIGRATION.md)** - Upgrading between versions

## 🏗️ Project Structure

```
infrared-cluster/
├── semantic_layer/
│   ├── core/           # Schema models and validation
│   ├── compiler/       # SQL generation and optimization
│   ├── connectors/     # Data source adapters
│   ├── api/            # FastAPI and GraphQL endpoints
│   ├── ml/             # LLM integration and ML features
│   ├── cache/          # Redis caching layer
│   ├── optimization/   # Query optimization
│   ├── telemetry/      # Observability and monitoring
│   └── ui/             # Streamlit UI components
├── tests/              # Test suite
├── docs/               # Documentation
├── deploy/             # Deployment configs
└── examples/           # Example queries and usage
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] Additional data source connectors (BigQuery, Redshift)
- [ ] Enhanced ML capabilities (forecasting, correlation analysis)
- [ ] Real-time query execution
- [ ] Advanced caching strategies
- [ ] Multi-tenancy support

## 📊 Project Stats

- **89 commits** from June to September 2025
- **58 Python files** with production-ready code
- **6 development phases** covering all aspects
- **Comprehensive test coverage** with integration tests

---

Built with ❤️ by the Semantic Layer team
