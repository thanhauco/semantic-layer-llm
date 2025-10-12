class QueryExplain:
    def explain(self, sql: str) -> dict:
        return {
            "plan": "Sequential Scan",
            "estimated_rows": 1000,
            "estimated_cost": 100.0
        }
