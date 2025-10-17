class DataQuality:
    def check_nulls(self, data, column: str, max_null_pct: float = 0.05):
        null_count = data[column].isnull().sum()
        null_pct = null_count / len(data)
        return null_pct <= max_null_pct
    
    def check_uniqueness(self, data, column: str):
        return data[column].nunique() == len(data)
    
    def check_range(self, data, column: str, min_val, max_val):
        return (data[column] >= min_val).all() and (data[column] <= max_val).all()
