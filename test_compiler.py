import unittest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.ai_suggestion import AISuggestionEngine

class TestCompilerPhases(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.semantic = SemanticAnalyzer()
        self.ai = AISuggestionEngine()

    def test_valid_query(self):
        q = "SELECT name, age FROM students;"
        tokens, l_err = self.lexer.tokenize(q)
        self.assertEqual(len(l_err), 0, "Should have no lexical errors")
        ast, syn_err = self.parser.parse(tokens)
        self.assertEqual(len(syn_err), 0, "Should have no syntax errors")
        sem_err = self.semantic.analyze(ast)
        self.assertEqual(len(sem_err), 0, "Should have no semantic errors")

    def test_lexical_error(self):
        q = "SELECT name @ FROM students;"
        tokens, l_err = self.lexer.tokenize(q)
        self.assertTrue(len(l_err) > 0, "Should detect invalid character '@'")
        
    def test_syntax_error(self):
        q = "SELECT FROM students;"
        tokens, l_err = self.lexer.tokenize(q)
        ast, syn_err = self.parser.parse(tokens)
        self.assertTrue(len(syn_err) > 0, "Should detect missing columns")
        
    def test_semantic_error(self):
        q = "SELECT names FROM students;"
        tokens, l_err = self.lexer.tokenize(q)
        ast, syn_err = self.parser.parse(tokens)
        sem_err = self.semantic.analyze(ast)
        self.assertTrue(len(sem_err) > 0, "Should detect unknown column 'names'")
        suggestions = self.ai.analyze_errors(q, tokens, l_err, syn_err, sem_err)
        self.assertTrue(any("name" in s for s in suggestions), "Should suggest correct column 'name'")
        
    def test_ai_suggestion(self):
        q = "SELEC name FROM students;"
        tokens, l_err = self.lexer.tokenize(q)
        ast, syn_err = self.parser.parse(tokens)
        sem_err = self.semantic.analyze(ast)
        suggestions = self.ai.analyze_errors(q, tokens, l_err, syn_err, sem_err)
        self.assertTrue(any("SELECT" in s for s in suggestions), "Should suggest correct keyword 'SELECT'")

if __name__ == '__main__':
    print("Running Compiler Validation Tests...")
    unittest.main(verbosity=2)
