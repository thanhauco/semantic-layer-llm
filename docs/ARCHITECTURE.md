# Architecture

## Overview
The Semantic Layer consists of several key components:

```
┌─────────────────────────────────────────┐
│           API Layer                     │
│  (FastAPI, GraphQL)                     │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│      Compiler & Optimizer               │
│  (SQL Generation, Query Planning)       │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│      Data Source Adapters               │
│  (Postgres, Snowflake, DuckDB)          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          ML Components                  │
│  (LLM, Anomaly Detection, Recommender)  │
└─────────────────────────────────────────┘
```

## Components

### Core Engine
- Schema definitions (Metrics, Dimensions, Tables)
- Validation logic

### Compiler
- SQL generation
- Dialect support
- Query optimization

### ML Engine
- LLM integration for natural language queries
- Anomaly detection
- Metric recommendations

### API Layer
- REST endpoints
- GraphQL interface
- Authentication & authorization
