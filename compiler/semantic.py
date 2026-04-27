from compiler.schema import SCHEMA

class SemanticAnalyzer:
    def __init__(self):
        self.schema = SCHEMA

    def analyze(self, ast):
        errors = []
        
        if not ast or "table" not in ast:
            return errors
            
        table = ast["table"]
        
        
        if table is None or table not in self.schema:
            if table is not None:
                errors.append(f"Semantic Error: Unknown table '{table}'.")
            return errors 
            
        
        if ast["type"] == "SELECT":
            for col in ast["columns"]:
                if col != "*" and col not in self.schema[table]["columns"]:
                    errors.append(f"Semantic Error: Unknown column '{col}' in table '{table}'.")
            
            if "where" in ast:
                for token in ast["where"]:
                    if token["type"] == "IDENTIFIER":
                        col = token["value"]
                        if col not in self.schema[table]["columns"]:
                            errors.append(f"Semantic Error: Unknown column '{col}' in WHERE clause for table '{table}'.")
                    
        return errors
