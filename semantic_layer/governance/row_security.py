class RowLevelSecurity:
    def __init__(self):
        self.policies = {}
    
    def add_policy(self, table: str, user_role: str, filter_sql: str):
        key = f"{table}:{user_role}"
        self.policies[key] = filter_sql
    
    def apply_policy(self, table: str, user_role: str, sql: str) -> str:
        key = f"{table}:{user_role}"
        if key in self.policies:
            return sql + f" AND {self.policies[key]}"
        return sql
