class QueryPlanAnalyzer:
    def analyze(self, sql: str) -> dict:
        return {
            "tables": [],
            "joins": [],
            "filters": []
        }
