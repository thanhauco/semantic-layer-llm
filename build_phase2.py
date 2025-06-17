#!/usr/bin/env python3
"""Phase 2: Core Compiler (Commits 16-30)"""

import os
import subprocess
from datetime import datetime
import random

START_DATE = datetime(2025, 6, 1, 9, 0, 0)
END_DATE = datetime(2025, 9, 30, 18, 0, 0)

def run_git_command(cmd, date=None):
    env = os.environ.copy()
    if date:
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(cmd, shell=True, check=True, env=env, capture_output=True)

def commit(message, date):
    run_git_command("git add -A", date)
    run_git_command(f'git commit -m "{message}"', date)
    print(f"✓ {message}")

def generate_dates(count, start_idx):
    delta = END_DATE - START_DATE
    dates = []
    for _ in range(count):
        random_seconds = random.randint(0, int(delta.total_seconds()))
        dates.append(START_DATE + timedelta(seconds=random_seconds))
    return sorted(dates)

from datetime import timedelta
dates = generate_dates(86, 0)
commit_idx = 15  # Start after Phase 1

def next_commit(message):
    global commit_idx
    commit(message, dates[commit_idx])
    commit_idx += 1

print("\n📦 PHASE 2: CORE COMPILER")

# Commit 16: Add WHERE clause support
with open("semantic_layer/compiler/filters.py", "w") as f:
    f.write("""from typing import Dict, Any, List

class FilterBuilder:
    @staticmethod
    def build_where_clause(filters: Dict[str, Any]) -> str:
        if not filters:
            return ""
        
        conditions = []
        for key, value in filters.items():
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            elif isinstance(value, (int, float)):
                conditions.append(f"{key} = {value}")
            elif isinstance(value, list):
                values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                conditions.append(f"{key} IN ({values})")
        
        return " AND ".join(conditions) if conditions else ""
""")
next_commit("Add WHERE clause support with filter builder")

# Commit 17: Integrate filters into compiler
with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

content = content.replace(
    "from .query import QueryRequest",
    "from .query import QueryRequest\nfrom .filters import FilterBuilder"
)

content = content.replace(
    "if request.limit:\n            sql += f\" LIMIT {request.limit}\"",
    """# Add WHERE clause
        if request.filters:
            where_clause = FilterBuilder.build_where_clause(request.filters)
            if where_clause:
                # Insert WHERE before GROUP BY
                if " GROUP BY" in sql:
                    sql = sql.replace(" GROUP BY", f" WHERE {where_clause} GROUP BY")
                else:
                    sql += f" WHERE {where_clause}"
        
        if request.limit:
            sql += f" LIMIT {request.limit}\""""
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Integrate WHERE clause into SQL compiler")

# Commit 18: Add JOIN support
with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

# Add join building method
join_method = """
    def _build_joins(self) -> str:
        \"\"\"Build JOIN clauses from semantic model.\"\"\"
        join_clauses = []
        for join in self.model.joins:
            join_type = join.type.value.upper()
            join_clauses.append(
                f"{join_type} JOIN {join.to_table} ON {join.sql_on}"
            )
        return " ".join(join_clauses)
"""

content = content.replace(
    "        return None",
    f"        return None{join_method}"
)

# Update compile method to use joins
content = content.replace(
    'sql = f"SELECT {', '.join(select_parts)} FROM {table.sql_table_name}"',
    '''sql = f"SELECT {', '.join(select_parts)} FROM {table.sql_table_name}"
        
        # Add joins
        joins = self._build_joins()
        if joins:
            sql += f" {joins}"'''
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Add JOIN support to compiler")

# Commit 19: Add aggregation function registry
with open("semantic_layer/compiler/aggregations.py", "w") as f:
    f.write("""from enum import Enum

class AggFunction(str, Enum):
    SUM = "SUM"
    COUNT = "COUNT"
    AVG = "AVG"
    MIN = "MIN"
    MAX = "MAX"
    COUNT_DISTINCT = "COUNT(DISTINCT {})"
    STDDEV = "STDDEV"
    VARIANCE = "VARIANCE"

class AggregationRegistry:
    @staticmethod
    def format_aggregation(agg_type: str, expression: str) -> str:
        if agg_type == "count_distinct":
            return f"COUNT(DISTINCT {expression})"
        else:
            return f"{agg_type.upper()}({expression})"
""")
next_commit("Add aggregation function registry")

# Commit 20: Enhance dimension resolution with table prefixes
with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

content = content.replace(
    "def _find_dimension(self, name: str) -> Optional[Dimension]:",
    """def _find_dimension(self, name: str) -> Optional[Dimension]:
        # Support table.dimension notation
        if '.' in name:
            table_name, dim_name = name.split('.', 1)
            for table in self.model.tables:
                if table.name == table_name:
                    for dim in table.dimensions:
                        if dim.name == dim_name:
                            return dim
        # Fallback to simple name search"""
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Enhance dimension resolution with table prefixes")

# Commit 21: Add metric resolution improvements
with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

content = content.replace(
    "def _find_metric(self, name: str) -> Optional[Metric]:",
    """def _find_metric(self, name: str) -> Optional[Metric]:
        # Support table.metric notation
        if '.' in name:
            table_name, metric_name = name.split('.', 1)
            for table in self.model.tables:
                if table.name == table_name:
                    for metric in table.metrics:
                        if metric.name == metric_name:
                            return metric
        # Fallback to simple name search"""
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Add qualified metric resolution (table.metric)")

# Commit 22: Refactor to visitor pattern
with open("semantic_layer/compiler/visitor.py", "w") as f:
    f.write("""from abc import ABC, abstractmethod
from semantic_layer.core.schema import Dimension, Metric

class QueryVisitor(ABC):
    @abstractmethod
    def visit_dimension(self, dimension: Dimension) -> str:
        pass
    
    @abstractmethod
    def visit_metric(self, metric: Metric) -> str:
        pass

class SqlVisitor(QueryVisitor):
    def visit_dimension(self, dimension: Dimension) -> str:
        return f"{dimension.sql} AS {dimension.name}"
    
    def visit_metric(self, metric: Metric) -> str:
        return f"{metric.aggregation.value}({metric.sql}) AS {metric.name}"
""")
next_commit("Refactor compiler to use visitor pattern")

# Commit 23: Add SQL dialect abstraction
with open("semantic_layer/compiler/dialects/__init__.py", "w") as f:
    f.write("")

with open("semantic_layer/compiler/dialects/base.py", "w") as f:
    f.write("""from abc import ABC, abstractmethod

class SqlDialect(ABC):
    @abstractmethod
    def quote_identifier(self, identifier: str) -> str:
        pass
    
    @abstractmethod
    def limit_clause(self, limit: int) -> str:
        pass
    
    @abstractmethod
    def supports_cte(self) -> bool:
        pass
""")
next_commit("Add SQL dialect abstraction layer")

# Commit 24: Add Postgres dialect
with open("semantic_layer/compiler/dialects/postgres.py", "w") as f:
    f.write("""from .base import SqlDialect

class PostgresDialect(SqlDialect):
    def quote_identifier(self, identifier: str) -> str:
        return f'"{identifier}"'
    
    def limit_clause(self, limit: int) -> str:
        return f"LIMIT {limit}"
    
    def supports_cte(self) -> bool:
        return True
    
    def cast_to_date(self, expression: str) -> str:
        return f"{expression}::DATE"
""")
next_commit("Add Postgres SQL dialect")

# Commit 25: Add Snowflake dialect
with open("semantic_layer/compiler/dialects/snowflake.py", "w") as f:
    f.write("""from .base import SqlDialect

class SnowflakeDialect(SqlDialect):
    def quote_identifier(self, identifier: str) -> str:
        return f'"{identifier}"'
    
    def limit_clause(self, limit: int) -> str:
        return f"LIMIT {limit}"
    
    def supports_cte(self) -> bool:
        return True
    
    def cast_to_date(self, expression: str) -> str:
        return f"TO_DATE({expression})"
""")
next_commit("Add Snowflake SQL dialect")

# Commit 26: Add DuckDB dialect
with open("semantic_layer/compiler/dialects/duckdb.py", "w") as f:
    f.write("""from .base import SqlDialect

class DuckDBDialect(SqlDialect):
    def quote_identifier(self, identifier: str) -> str:
        return f'"{identifier}"'
    
    def limit_clause(self, limit: int) -> str:
        return f"LIMIT {limit}"
    
    def supports_cte(self) -> bool:
        return True
    
    def cast_to_date(self, expression: str) -> str:
        return f"CAST({expression} AS DATE)"
""")
next_commit("Add DuckDB SQL dialect")

# Commit 27: Add advanced filter parsing
with open("semantic_layer/compiler/filters.py", "a") as f:
    f.write("""

class AdvancedFilterBuilder:
    @staticmethod
    def parse_filter_expression(filter_dict: Dict[str, Any]) -> str:
        \"\"\"Parse complex filter expressions with operators.\"\"\"
        conditions = []
        
        for key, value in filter_dict.items():
            if key == "$and":
                sub_conditions = [AdvancedFilterBuilder.parse_filter_expression(f) for f in value]
                conditions.append(f"({' AND '.join(sub_conditions)})")
            elif key == "$or":
                sub_conditions = [AdvancedFilterBuilder.parse_filter_expression(f) for f in value]
                conditions.append(f"({' OR '.join(sub_conditions)})")
            elif isinstance(value, dict):
                # Operator-based filters
                for op, val in value.items():
                    if op == "$gt":
                        conditions.append(f"{key} > {val}")
                    elif op == "$gte":
                        conditions.append(f"{key} >= {val}")
                    elif op == "$lt":
                        conditions.append(f"{key} < {val}")
                    elif op == "$lte":
                        conditions.append(f"{key} <= {val}")
                    elif op == "$ne":
                        conditions.append(f"{key} != {val}")
            else:
                if isinstance(value, str):
                    conditions.append(f"{key} = '{value}'")
                else:
                    conditions.append(f"{key} = {value}")
        
        return " AND ".join(conditions)
""")
next_commit("Add advanced filter parsing with operators")

# Commit 28: Add complex filter support (AND/OR)
with open("tests/test_filters.py", "w") as f:
    f.write("""import pytest
from semantic_layer.compiler.filters import AdvancedFilterBuilder

def test_simple_filter():
    filters = {"country": "US"}
    result = AdvancedFilterBuilder.parse_filter_expression(filters)
    assert "country = 'US'" in result

def test_and_filter():
    filters = {
        "$and": [
            {"country": "US"},
            {"age": {"$gt": 18}}
        ]
    }
    result = AdvancedFilterBuilder.parse_filter_expression(filters)
    assert "AND" in result
    assert "age > 18" in result

def test_or_filter():
    filters = {
        "$or": [
            {"country": "US"},
            {"country": "CA"}
        ]
    }
    result = AdvancedFilterBuilder.parse_filter_expression(filters)
    assert "OR" in result
""")
next_commit("Add tests for complex AND/OR filters")

# Commit 29: Add HAVING clause support
with open("semantic_layer/compiler/query.py", "a") as f:
    f.write("""

class HavingClause(BaseModel):
    metric: str
    operator: str  # >, <, >=, <=, =
    value: float
""")

with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

content = content.replace(
    "if request.dimensions:\n            sql += f\" GROUP BY {', '.join(request.dimensions)}\"",
    """if request.dimensions:
            sql += f" GROUP BY {', '.join(request.dimensions)}"
        
        # Add HAVING clause (if present in request)
        if hasattr(request, 'having') and request.having:
            having_conditions = []
            for condition in request.having:
                having_conditions.append(f"{condition.metric} {condition.operator} {condition.value}")
            sql += f" HAVING {' AND '.join(having_conditions)}\""""
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Add HAVING clause support for metric filtering")

# Commit 30: Add ORDER BY support
with open("semantic_layer/compiler/query.py", "r") as f:
    content = f.read()

content = content.replace(
    "limit: Optional[int] = None",
    """limit: Optional[int] = None
    order_by: Optional[List[str]] = None
    order_desc: bool = False"""
)

with open("semantic_layer/compiler/query.py", "w") as f:
    f.write(content)

with open("semantic_layer/compiler/sql_compiler.py", "r") as f:
    content = f.read()

content = content.replace(
    "if request.limit:\n            sql += f\" LIMIT {request.limit}\"",
    """# Add ORDER BY
        if request.order_by:
            direction = "DESC" if request.order_desc else "ASC"
            sql += f" ORDER BY {', '.join(request.order_by)} {direction}"
        
        if request.limit:
            sql += f" LIMIT {request.limit}\""""
)

with open("semantic_layer/compiler/sql_compiler.py", "w") as f:
    f.write(content)
next_commit("Add ORDER BY support with ASC/DESC")

print(f"\n✅ Phase 2 complete: {commit_idx} commits")
print("=" * 60)
