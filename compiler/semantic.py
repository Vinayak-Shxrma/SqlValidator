from compiler.schema import SCHEMA

class SemanticAnalyzer:
    def __init__(self):
        self.schema = SCHEMA

    def analyze(self, ast):
        errors = []
        
        if not ast or "table" not in ast:
            return errors
            
        table = ast["table"]
        
        # 1. Validate Table Exists
        if table and table not in self.schema:
            errors.append(f"Semantic Error: Unknown table '{table}'.")
            return errors # Fast fail, we don't know the schema to check columns
            
        # 2. Validate Columns for SELECT statements
        if ast["type"] == "SELECT":
            for col in ast["columns"]:
                if col != "*" and col not in self.schema[table]["columns"]:
                    errors.append(f"Semantic Error: Unknown column '{col}' in table '{table}'.")
                    
        return errors
