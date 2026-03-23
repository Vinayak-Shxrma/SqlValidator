import re

class Lexer:
    def __init__(self):
        self.token_specs = [
            ("KEYWORD", r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|INTO|VALUES|SET)\b'),
            ("IDENTIFIER", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ("OPERATOR", r'[=><]+'),
            ("LITERAL_STRING", r"'[^']*'"),
            ("LITERAL_NUM", r'\b\d+\b'),
            ("SYMBOL", r'[;,.*()]'),
            ("WHITESPACE", r'\s+'),
        ]

    def tokenize(self, query):
        tokens = []
        errors = []
        pos = 0
        while pos < len(query):
            match = None
            for token_type, pattern in self.token_specs:
                regex = re.compile(pattern, re.IGNORECASE)
                match = regex.match(query, pos)
                if match:
                    if token_type != "WHITESPACE":
                        tokens.append({
                            "type": token_type,
                            "value": match.group(0),
                            "pos": pos
                        })
                    pos = match.end()
                    break
            
            if not match:
                char = query[pos]
                errors.append(f"Lexical Error: Invalid character '{char}' at position {pos}")
                pos += 1
                
        return tokens, errors
