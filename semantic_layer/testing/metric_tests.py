from typing import Dict, List, Callable
from dataclasses import dataclass

@dataclass
class MetricTest:
    name: str
    metric_name: str
    test_type: str  # freshness, accuracy, completeness
    assertion: Callable
    severity: str = "error"  # error, warning

class MetricTesting:
    """Automated testing framework for metrics."""
    
    def __init__(self):
        self.tests = []
    
    def add_freshness_test(self, metric_name: str, max_age_hours: int):
        """Test if metric data is fresh."""
        test = MetricTest(
            name=f"{metric_name}_freshness",
            metric_name=metric_name,
            test_type="freshness",
            assertion=lambda data: data["last_updated_hours_ago"] < max_age_hours
        )
        self.tests.append(test)
    
    def add_accuracy_test(self, metric_name: str, expected_range: tuple):
        """Test if metric value is within expected range."""
        test = MetricTest(
            name=f"{metric_name}_accuracy",
            metric_name=metric_name,
            test_type="accuracy",
            assertion=lambda data: expected_range[0] <= data["value"] <= expected_range[1]
        )
        self.tests.append(test)
    
    def add_completeness_test(self, metric_name: str, min_row_count: int):
        """Test if metric has minimum required data."""
        test = MetricTest(
            name=f"{metric_name}_completeness",
            metric_name=metric_name,
            test_type="completeness",
            assertion=lambda data: data["row_count"] >= min_row_count
        )
        self.tests.append(test)
    
    def run_tests(self, metric_data: Dict) -> List[Dict]:
        """Run all tests and return results."""
        results = []
        
        for test in self.tests:
            if test.metric_name in metric_data:
                data = metric_data[test.metric_name]
                passed = test.assertion(data)
                
                results.append({
                    "test_name": test.name,
                    "metric": test.metric_name,
                    "type": test.test_type,
                    "passed": passed,
                    "severity": test.severity
                })
        
        return results
