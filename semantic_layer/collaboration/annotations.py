from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Annotation:
    id: str
    metric_name: str
    timestamp: datetime
    user: str
    content: str
    tags: List[str]

class KnowledgeGraph:
    """
    Social layer for metrics. Allows users to annotate data points,
    verify definitions, and discuss lineage.
    """
    
    def __init__(self):
        self.annotations = []
        self.endorsements = {} # metric -> level (Gold/Silver)

    def add_annotation(self, metric: str, user: str, content: str, date: datetime = None):
        """Annotate a specific point in time or general metric."""
        self.annotations.append(Annotation(
            id=f"note_{len(self.annotations)}",
            metric_name=metric,
            timestamp=date or datetime.now(),
            user=user,
            content=content,
            tags=[]
        ))

    def endorse_metric(self, metric: str, level: str, user: str):
        """Mark a metric as verified/trusted."""
        self.endorsements[metric] = {
            "level": level,
            "verified_by": user,
            "date": datetime.now()
        }

    def get_context(self, metric: str) -> Dict:
        """Retrieve all social context for a metric."""
        return {
            "endorsement": self.endorsements.get(metric),
            "annotations": [a for a in self.annotations if a.metric_name == metric]
        }
