from typing import Dict, List, Optional
from enum import Enum

class TenantIsolation(str, Enum):
    SCHEMA = "schema"  # Separate schema per tenant
    ROW_LEVEL = "row_level"  # Row-level security
    DATABASE = "database"  # Separate database per tenant

class MultiTenancy:
    """Multi-tenancy support with different isolation levels."""
    
    def __init__(self, isolation_level: TenantIsolation = TenantIsolation.ROW_LEVEL):
        self.isolation_level = isolation_level
        self.tenant_configs = {}
    
    def register_tenant(self, tenant_id: str, config: Dict):
        """Register a new tenant with configuration."""
        self.tenant_configs[tenant_id] = {
            "schema": config.get("schema", f"tenant_{tenant_id}"),
            "allowed_tables": config.get("allowed_tables", []),
            "row_filter": config.get("row_filter", f"tenant_id = '{tenant_id}'")
        }
    
    def apply_tenant_filter(self, tenant_id: str, sql: str) -> str:
        """Apply tenant-specific filters to SQL query."""
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Unknown tenant: {tenant_id}")
        
        config = self.tenant_configs[tenant_id]
        
        if self.isolation_level == TenantIsolation.SCHEMA:
            # Prefix table names with tenant schema
            return sql.replace("FROM ", f"FROM {config['schema']}.")
        
        elif self.isolation_level == TenantIsolation.ROW_LEVEL:
            # Add WHERE clause for row-level security
            if "WHERE" in sql:
                return sql.replace("WHERE", f"WHERE {config['row_filter']} AND")
            else:
                return sql + f" WHERE {config['row_filter']}"
        
        return sql
    
    def validate_access(self, tenant_id: str, table_name: str) -> bool:
        """Check if tenant has access to table."""
        config = self.tenant_configs.get(tenant_id, {})
        allowed = config.get("allowed_tables", [])
        return not allowed or table_name in allowed
