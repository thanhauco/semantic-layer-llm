from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class TenantMLModel(ABC):
    """Abstract base class for tenant-specific ML models."""
    
    @abstractmethod
    def load_adapter(self, tenant_id: str) -> bool:
        """Load tenant-specific LoRA adapter."""
        pass
        
    @abstractmethod
    def predict(self, tenant_id: str, input_data: Any) -> Any:
        """Run inference for a specific tenant."""
        pass

class LoRAModelManager(TenantMLModel):
    """
    Manages a shared base model and dynamic LoRA adapters for multi-tenancy.
    Scales to 1000s of tenants with minimal GPU memory overhead.
    """
    
    def __init__(self, base_model_path: str):
        self.base_model_path = base_model_path
        self.active_adapters: Dict[str, Any] = {}
        # self.base_model = load_base_model(base_model_path) # Mock loading
        print(f"Loaded shared base model from {base_model_path}")

    def load_adapter(self, tenant_id: str) -> bool:
        """
        Dynamically load a LoRA adapter for the tenant from storage.
        """
        if tenant_id in self.active_adapters:
            return True
            
        print(f"Loading LoRA adapter for tenant {tenant_id} from object storage...")
        # adapter_weights = download_from_s3(f"tenants/{tenant_id}/adapter.bin")
        # self.base_model.load_adapter(adapter_weights)
        self.active_adapters[tenant_id] = "loaded_adapter_weights"
        return True

    def predict(self, tenant_id: str, input_data: Any) -> Any:
        """
        Run inference using the tenant's specific adapter.
        """
        if tenant_id not in self.active_adapters:
            self.load_adapter(tenant_id)
            
        print(f"Running inference for {tenant_id} using Adapter + Base Model")
        # with self.base_model.use_adapter(tenant_id):
        #     return self.base_model.generate(input_data)
        return {"result": f"Personalized result for {tenant_id}: {input_data}"}

class VectorTenantManager:
    """
    Handles multi-tenant vector search with strict isolation.
    """
    
    def __init__(self, vector_db_client):
        self.client = vector_db_client
        
    def search(self, tenant_id: str, query_vector: list, top_k: int = 5):
        """
        Search with mandatory tenant_id filter.
        """
        return self.client.search(
            collection="semantic_layer",
            vector=query_vector,
            filter=f"tenant_id == '{tenant_id}'", # Strict filter injection
            limit=top_k
        )
