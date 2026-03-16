import Levenshtein
from compiler.schema import SCHEMA

KEYWORDS = ["SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE", "INTO", "VALUES", "SET"]

class AISuggestionEngine:
    def get_closest_match(self, word, options, threshold=2):
        best_match = None
        min_distance = float('inf')
        
        for option in options:
            dist = Levenshtein.distance(word.upper(), option.upper())
            if dist < min_distance and dist <= threshold:
                min_distance = dist
                best_match = option
                
        return best_match

    def analyze_errors(self, tokens, lexical_errors, syntax_errors, semantic_errors):
        suggestions = []
        
        # Check for misspelled keywords in identifiers
        for token in tokens:
            if token["type"] == "IDENTIFIER":
                val = token["value"]
                # Maybe it was a misspelled keyword?
                closest_kw = self.get_closest_match(val, KEYWORDS, threshold=2)
                
                # Make sure it's not actually supposed to be a column name or table name
                valid_identifiers = list(SCHEMA.keys())
                for t in SCHEMA.values():
                    valid_identifiers.extend(list(t["columns"].keys()))
                    
                if closest_kw and val.lower() not in valid_identifiers:
                    suggestions.append(f"Identifier '{val}' might be misspelled. Did you mean keyword '{closest_kw}'?")
                    
        # Provide suggestions for semantic errors
        for error in semantic_errors:
            if "Unknown table" in error:
                import re
                match = re.search(r"Unknown table '([^']+)'", error)
                if match:
                    table = match.group(1)
                    closest = self.get_closest_match(table, list(SCHEMA.keys()))
                    if closest:
                        suggestions.append(f"Did you mean table '{closest}' instead of '{table}'?")
            elif "Unknown column" in error:
                import re
                match = re.search(r"Unknown column '([^']+)' in table '([^']+)'", error)
                if match:
                    col = match.group(1)
                    table = match.group(2)
                    if table in SCHEMA:
                        closest = self.get_closest_match(col, list(SCHEMA[table]["columns"].keys()))
                        if closest:
                            suggestions.append(f"Did you mean column '{closest}' instead of '{col}'?")
                            
        return suggestions
