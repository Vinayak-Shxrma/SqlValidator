class Parser:
    def __init__(self):
        pass

    def parse(self, tokens):
        errors = []
        ast = {}
        
        # filter out whitespaces
        tokens = [t for t in tokens if t["type"] != "WHITESPACE"]
        
        if not tokens:
            errors.append("Syntax Error: Empty query.")
            return ast, errors

        # Basic parsing structure based on the first keyword
        first_token = tokens[0]
        
        if first_token["type"] == "KEYWORD":
            command = first_token["value"].upper()
            if command == "SELECT":
                ast, errors = self.parse_select(tokens)
            elif command == "INSERT":
                ast, errors = self.parse_insert(tokens)
            elif command == "UPDATE":
                ast, errors = self.parse_update(tokens)
            elif command == "DELETE":
                ast, errors = self.parse_delete(tokens)
            else:
                errors.append(f"Syntax Error: Unsupported statement starting with '{command}'")
        else:
            errors.append(f"Syntax Error: Query must start with a valid SQL command (SELECT, INSERT, UPDATE, DELETE). Found '{first_token['value']}'")
            
        return ast, errors

    def parse_select(self, tokens):
        errors = []
        ast = {"type": "SELECT", "columns": [], "table": None}
        
        state = "COLUMNS"
        
        for i in range(1, len(tokens)):
            token = tokens[i]
            
            if token["value"].upper() == "FROM":
                state = "FROM"
                continue
            elif token["value"].upper() in ["WHERE", "ORDER", "GROUP", "LIMIT"]:
                break # We only support basic SELECT FROM for this project scope
                
            if state == "COLUMNS":
                if token["type"] == "IDENTIFIER" or (token["type"] == "SYMBOL" and token["value"] == "*"):
                    ast["columns"].append(token["value"])
                elif token["type"] == "SYMBOL" and token["value"] == ",":
                    continue
                elif token["type"] == "SYMBOL" and token["value"] == ";":
                    break
                else:
                    errors.append(f"Syntax Error: Unexpected token '{token['value']}' in column list.")
                    
            elif state == "FROM":
                if token["type"] == "IDENTIFIER":
                    if ast["table"]:
                        errors.append(f"Syntax Error: Unexpected token '{token['value']}' in FROM clause.")
                    else:
                        ast["table"] = token["value"]
                elif token["type"] == "SYMBOL" and token["value"] == ";":
                    break
                else:
                    errors.append(f"Syntax Error: Unexpected token '{token['value']}' in FROM clause.")
                
        if not ast["table"]:
            errors.append("Syntax Error: Missing FROM clause.")
        if not ast["columns"]:
            errors.append("Syntax Error: Missing column selection.")
            
        return ast, errors

    def parse_insert(self, tokens):
        ast = {"type": "INSERT", "table": None}
        errors = []
        try:
            if tokens[1]["value"].upper() != "INTO":
                errors.append("Syntax Error: Expected 'INTO' after 'INSERT'.")
            if tokens[2]["type"] != "IDENTIFIER":
                errors.append("Syntax Error: Expected table name.")
            else:
                ast["table"] = tokens[2]["value"]
        except IndexError:
            errors.append("Syntax Error: Incomplete INSERT statement.")
            
        return ast, errors
        
    def parse_update(self, tokens):
        ast = {"type": "UPDATE", "table": None}
        errors = []
        try:
            if tokens[1]["type"] != "IDENTIFIER":
                errors.append("Syntax Error: Expected table name after 'UPDATE'.")
            else:
                ast["table"] = tokens[1]["value"]
            if tokens[2]["value"].upper() != "SET":
                errors.append("Syntax Error: Expected 'SET' after table name.")
        except IndexError:
            errors.append("Syntax Error: Incomplete UPDATE statement.")
            
        return ast, errors

    def parse_delete(self, tokens):
        ast = {"type": "DELETE", "table": None}
        errors = []
        try:
            if tokens[1]["value"].upper() != "FROM":
                errors.append("Syntax Error: Expected 'FROM' after 'DELETE'.")
            if tokens[2]["type"] != "IDENTIFIER":
                errors.append("Syntax Error: Expected table name.")
            else:
                ast["table"] = tokens[2]["value"]
        except IndexError:
            errors.append("Syntax Error: Incomplete DELETE statement.")
            
        return ast, errors
