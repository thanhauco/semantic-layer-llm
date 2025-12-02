# Multi-Cloud & Scalable ML Architecture

This document outlines the strategy for deploying the Semantic Layer across multiple cloud providers (AWS, Azure, GCP) and handling multi-tenancy for Machine Learning workloads at scale.

## ☁️ Multi-Cloud Strategy: "Write Once, Deploy Anywhere"

To achieve cloud agnosticism, we rely on **Kubernetes** as the universal compute plane and abstract cloud-specific services using **Terraform** and **Interface Adapters**.

### 1. Infrastructure Abstraction (Terraform)

We use a modular Terraform structure where the root module defines the *intent* and provider-specific sub-modules handle the *implementation*.

```hcl
# main.tf (Root)
module "infrastructure" {
  source = "./providers/${var.cloud_provider}" # aws, azure, or gcp
  
  cluster_name = "semantic-layer-prod"
  node_count   = 10
}
```

| Component | AWS Implementation | Azure Implementation | GCP Implementation |
|-----------|--------------------|----------------------|--------------------|
| **Compute** | EKS | AKS | GKE |
| **Blob Storage** | S3 | Blob Storage | GCS |
| **Secrets** | Secrets Manager | Key Vault | Secret Manager |
| **Identity** | IAM Roles for SA | Workload Identity | Workload Identity |

### 2. Application Abstraction (Python Interfaces)

The code interacts with abstract interfaces, not direct SDKs.

```python
class BlobStorage(ABC):
    @abstractmethod
    def upload(self, path: str, data: bytes): pass

class AWSStorage(BlobStorage): ...
class AzureStorage(BlobStorage): ...
```

## 🏢 Multi-Tenancy at Scale

### 1. Data Isolation Levels
*   **Tier 1 (Enterprise)**: **Database Isolation**. Dedicated Postgres database / Snowflake Schema per tenant.
*   **Tier 2 (Standard)**: **Row-Level Security (RLS)**. Shared tables with `tenant_id` column and enforced filter predicates.

### 2. Compute Isolation
*   **Kubernetes Namespaces**: Each tenant (or group of tenants) gets a dedicated Namespace for strict resource quotas and network policies.
*   **Network Policies**: Deny cross-namespace traffic by default.

## 🧠 Scalable ML for Multi-Tenancy

Serving thousands of custom ML models (e.g., fine-tuned text-to-SQL models per tenant) is cost-prohibitive if done naively. We use **Parameter-Efficient Fine-Tuning (PEFT)** and **Dynamic Loading**.

### 1. The "LoRA Adapter" Pattern
Instead of deploying 1,000 full LLMs (70GB each), we deploy:
1.  **One Shared Base Model** (e.g., Llama-3-70B) loaded in GPU memory.
2.  **1,000 Lightweight Adapters** (LoRA weights, ~10MB each) stored in S3/Blob.

When a request comes from Tenant A:
1.  The Inference Server (vLLM or Ray Serve) loads Tenant A's LoRA adapter on the fly (ms latency).
2.  Inference runs against the Base Model + Adapter.

### 2. Vector Database Partitioning
*   **Single Cluster**: Do not spin up a Vector DB per tenant.
*   **Partitioning**: Use "Collection Partitioning" or Metadata Filtering (`tenant_id: "123"`).
*   **RBAC**: Ensure the API layer injects the `tenant_id` filter into every vector search query automatically.

### 3. Ray Serve for Inference Scaling
We use **Ray Serve** to orchestrate ML inference:
*   **Autoscaling**: Scale replicas based on queue depth.
*   **Fractional GPUs**: Pack multiple small models onto a single A100 GPU using Multi-Instance GPU (MIG) or time-slicing.

## 🔄 Deployment Pipeline

1.  **Terraform Apply**: Provisions cloud-specific infra.
2.  **Helm Install**: Deploys the application + Ray Cluster.
3.  **Tenant Provisioning**:
    *   Create K8s Namespace.
    *   Create Database/Schema.
    *   Initialize Tenant Config in Metadata DB.

