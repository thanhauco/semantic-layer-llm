# Production Deployment at Scale

This guide outlines the reference architecture for deploying the Semantic Layer at enterprise scale (10k+ QPS, multi-tenant, high availability).

## 🏗️ Reference Architecture

```mermaid
graph TD
    User[User / BI Tool] --> LB[Load Balancer (ALB/Nginx)]
    
    subgraph "Compute Layer (Kubernetes)"
        LB --> API[API Pods (FastAPI)]
        API --> Workers[Worker Pods (Celery)]
        API --> WS[WebSocket Service]
    end
    
    subgraph "Data & State"
        API --> Redis[Redis Cluster (Cache/Queue)]
        Workers --> Redis
        API --> VectorDB[Vector Store (Milvus/Pinecone)]
        API --> MetaDB[Metadata DB (Postgres)]
    end
    
    subgraph "Data Warehouses"
        API --> Snowflake
        API --> BigQuery
        API --> Databricks
    end
    
    subgraph "Observability"
        API -.-> OTel[OpenTelemetry Collector]
        OTel --> Prom[Prometheus]
        OTel --> Jaeger[Jaeger]
    end
```

## 🚀 Scaling Strategies

### 1. Stateless API Layer (Horizontal Scaling)
- **Component**: FastAPI application
- **Strategy**: Deploy on Kubernetes (EKS/GKE) with Horizontal Pod Autoscaler (HPA).
- **Metric**: Scale based on CPU utilization (>70%) or Request Latency.
- **Config**:
  ```yaml
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: semantic-layer-api
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: semantic-layer-api
    minReplicas: 3
    maxReplicas: 50
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  ```

### 2. Caching Strategy (Redis Cluster)
- **Tier 1 (L1)**: In-memory LRU cache within API pods (fastest, local).
- **Tier 2 (L2)**: Redis Cluster for distributed semantic caching.
- **Sharding**: Use consistent hashing for cache keys to distribute load evenly across Redis nodes.
- **Eviction**: Set `maxmemory-policy allkeys-lru` to handle memory pressure gracefully.

### 3. Asynchronous Processing (Celery Workers)
- **Workload**: Heavy tasks like `IncrementalMaterialization`, `PredictiveCacheWarming`, and `Alerts`.
- **Queues**: Split into `fast-lane` (interactive queries) and `slow-lane` (background jobs).
- **Scaling**: Scale worker pods based on Queue Depth (using KEDA - Kubernetes Event-driven Autoscaling).

### 4. Vector Search Scaling
- **Engine**: Use a distributed vector database (e.g., Milvus distributed or Qdrant).
- **Index**: Use HNSW indexes for low-latency (<10ms) approximate nearest neighbor search.
- **Replicas**: Increase read replicas for high QPS on semantic caching lookups.

### 5. Database Connection Pooling
- **Problem**: 100s of API pods can exhaust Warehouse connection limits.
- **Solution**: Use **PgBouncer** (for Postgres) or a dedicated Proxy Service for Snowflake/BigQuery to multiplex connections.
- **Pattern**: Implement "Connection Leases" where API pods borrow a connection only for the duration of the query execution.

## 🔒 Security & Governance at Scale

- **Isolation**: Use `TenantIsolation.SCHEMA` or `TenantIsolation.DATABASE` for strict data separation.
- **Network**: Deploy in private subnets; use VPC Endpoints (AWS PrivateLink) to connect to Warehouses securely without traversing public internet.
- **Secrets**: Use HashiCorp Vault or AWS Secrets Manager injected as environment variables.

## 🛠️ Infrastructure as Code (Terraform)

Recommended module structure:

```
terraform/
├── modules/
│   ├── eks/            # Kubernetes Cluster
│   ├── rds/            # Metadata Database
│   ├── elasticache/    # Redis Cluster
│   └── vpc/            # Networking
├── environments/
│   ├── prod/
│   └── staging/
└── main.tf
```

## 📊 Capacity Planning (Example)

| Component | Size | Count | Notes |
|-----------|------|-------|-------|
| API Pods | 2 vCPU, 4GB RAM | 10-50 | Autoscaled |
| Worker Pods | 4 vCPU, 8GB RAM | 5-20 | Autoscaled (KEDA) |
| Redis | cache.r6g.xlarge | 3 shards | Multi-AZ, Cluster Mode |
| Metadata DB | db.t4g.large | 2 | Primary + Standby |

## 🔄 CI/CD Pipeline

1. **Build**: Docker build + Unit Tests + Security Scan (Trivy).
2. **Staging**: Deploy to Staging Namespace -> Run Integration Tests.
3. **Canary**: Deploy to 5% of Prod traffic -> Monitor Error Rate.
4. **Promote**: Rollout to 100% if Canary passes.

