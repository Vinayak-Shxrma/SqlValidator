import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from compiler.schema import SCHEMA

class AISuggestionEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def analyze_errors(self, query, tokens, lexical_errors, syntax_errors, semantic_errors):
        if not lexical_errors and not syntax_errors and not semantic_errors:
            return []
            
        if not self.client:
            return ["AI Integration Warning: GEMINI_API_KEY environment variable is not set. Please set it to receive intelligent SQL suggestions."]

        schema_str = str(SCHEMA)
        
        prompt = f"""
You are an expert SQL Compiler assistant built to help students learn Compiler Design. 
The student submitted the following SQL Query: '{query}'

The compiler phases reported the following errors:
Lexical: {lexical_errors}
Syntax: {syntax_errors}
Semantic: {semantic_errors}

Here is the predefined database schema available (in Python dict format):
{schema_str}

Please provide 1 to 2 clear, beginner-friendly sentences acting as an AI Suggestion. 
If there's a typo in a keyword or a schema entity, suggest the correction.
Just output the suggestion text, do not use formatting like bold or headers.
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return [response.text.strip()]
        except Exception as e:
            return [f"AI Suggestion Error: Could not connect to Gemini API ({str(e)})"]
