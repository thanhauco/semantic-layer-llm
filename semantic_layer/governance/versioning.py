from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class MetricVersion:
    version: str
    sql: str
    created_at: datetime
    created_by: str
    changelog: str

class MetricVersioning:
    """Version control for metric definitions."""
    
    def __init__(self):
        self.versions = {}  # metric_name -> [versions]
    
    def create_version(self, metric_name: str, sql: str, 
                      created_by: str, changelog: str) -> str:
        """Create a new version of a metric."""
        if metric_name not in self.versions:
            self.versions[metric_name] = []
        
        version_num = len(self.versions[metric_name]) + 1
        version = MetricVersion(
            version=f"v{version_num}",
            sql=sql,
            created_at=datetime.now(),
            created_by=created_by,
            changelog=changelog
        )
        
        self.versions[metric_name].append(version)
        return version.version
    
    def get_version(self, metric_name: str, version: Optional[str] = None) -> Optional[MetricVersion]:
        """Get specific version or latest."""
        if metric_name not in self.versions:
            return None
        
        if version is None:
            return self.versions[metric_name][-1]  # Latest
        
        for v in self.versions[metric_name]:
            if v.version == version:
                return v
        return None
    
    def compare_versions(self, metric_name: str, v1: str, v2: str) -> Dict:
        """Compare two versions of a metric."""
        version1 = self.get_version(metric_name, v1)
        version2 = self.get_version(metric_name, v2)
        
        if not version1 or not version2:
            return {"error": "Version not found"}
        
        return {
            "metric": metric_name,
            "v1": {"version": v1, "sql": version1.sql},
            "v2": {"version": v2, "sql": version2.sql},
            "sql_changed": version1.sql != version2.sql
        }
