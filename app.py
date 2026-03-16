from flask import Flask, request, jsonify, render_template
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.ai_suggestion import AISuggestionEngine

app = Flask(__name__)

lexer = Lexer()
parser = Parser()
semantic_analyzer = SemanticAnalyzer()
ai_engine = AISuggestionEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    query = data.get('query', '')
    
    # 1. Lexical Analysis
    tokens, lexical_errors = lexer.tokenize(query)
    
    # 2. Syntax Analysis
    ast, syntax_errors = parser.parse(tokens)
        
    # 3. Semantic Analysis
    semantic_errors = semantic_analyzer.analyze(ast)
        
    # 4. AI Suggestions
    suggestions = ai_engine.analyze_errors(tokens, lexical_errors, syntax_errors, semantic_errors)
    
    return jsonify({
        "tokens": tokens,
        "lexical_errors": lexical_errors,
        "syntax_errors": syntax_errors,
        "semantic_errors": semantic_errors,
        "suggestions": suggestions,
        "ast": ast
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
