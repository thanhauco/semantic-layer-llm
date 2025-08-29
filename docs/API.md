# API Documentation

## Overview
The Semantic Layer API provides REST and GraphQL endpoints for querying data.

## Endpoints

### POST /query
Execute a semantic query.

**Request Body:**
```json
{
  "metrics": ["total_users", "revenue"],
  "dimensions": ["country", "date"],
  "filters": {
    "country": "US"
  },
  "limit": 100
}
```

**Response:**
```json
{
  "sql": "SELECT ...",
  "data": [...],
  "row_count": 42
}
```

### GET /health
Health check endpoint.

### GET /schema
Get the semantic model schema.
