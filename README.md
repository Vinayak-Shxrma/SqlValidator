# SQL Query Validator

An intelligent, compiler-based SQL validation system built with Flask. It validates SQL queries through three formal compiler phases — Lexical Analysis, Syntax Parsing, and Semantic Analysis — and provides AI-powered suggestions via Google Gemini.

> **Academic Project** — Graphic Era (Deemed to be University), B.Tech CSE (AI), Semester VI  
> Subject: Compiler Design (TCS 601)

---

## Features

- **Lexical Analysis** — Tokenizes the SQL query and detects invalid characters
- **Syntax Parsing** — Builds an Abstract Syntax Tree (AST) and catches grammar violations
- **Semantic Analysis** — Validates table and column names against a predefined schema
- **AI Suggestions** — Uses Google Gemini 2.5 Flash to generate beginner-friendly fix recommendations
- **Interactive AST Viewer** — Renders a pannable, zoomable SVG tree of the parsed query
- **Token Categorization** — Groups tokens by type (KEYWORD, IDENTIFIER, OPERATOR, etc.)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Vanilla JS, Feather Icons |
| Compiler Phases | Custom Lexer, Parser, Semantic Analyzer |
| AI Integration | Google Gemini 2.5 Flash (`google-genai`) |
| Fuzzy Matching | `python-Levenshtein`, `rapidfuzz` |

---

## Project Structure

```
SqlValidator/
├── app.py                  # Flask app & API routes
├── requirements.txt
├── compiler/
│   ├── lexer.py            # Tokenizer (Phase 1)
│   ├── parser.py           # AST builder (Phase 2)
│   ├── semantic.py         # Schema validator (Phase 3)
│   ├── ai_suggestion.py    # Gemini AI integration
│   └── schema.py           # Predefined DB schema
├── templates/
│   └── index.html          # Main UI
├── static/
│   ├── style.css
│   └── script.js
├── test_compiler.py        # Unit tests
└── test_queries.py         # Unit queries
```

---

## Supported Schema

The system validates queries against three built-in tables:

| Table | Columns |
|---|---|
| `students` | `id`, `name`, `age`, `course` |
| `courses` | `course_id`, `course_name`, `credits` |
| `employees` | `id`, `name`, `salary`, `role` |

---

## Getting Started

### Prerequisites
- Python 3.9+
- A Google Gemini API key ([get one here](https://aistudio.google.com/))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Vinayak-Shxrma/SqlValidator.git
cd SqlValidator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
# Create a .env file in the root directory:
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 4. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## Supported SQL Statements

| Statement | Example |
|---|---|
| `SELECT` | `SELECT name, age FROM students;` |
| `INSERT` | `INSERT INTO students VALUES (...)` |
| `UPDATE` | `UPDATE employees SET salary = 6000` |
| `DELETE` | `DELETE FROM courses` |
| `DROP` | `DROP TABLE students;` |
| `TRUNCATE` | `TRUNCATE TABLE employees;` |

---

## Example Validations

**Valid Query**
```sql
SELECT name, age FROM students;
```
No errors. AST rendered.

**Lexical Error**
```sql
SELECT name @ FROM students;
```
`Lexical Error: Invalid character '@' at position 12`

**Semantic Error + AI Fix**
```sql
SELECT names FROM studants;
```
`Semantic Error: Unknown table 'studants'.`  
*"Did you mean table 'students'? Also, 'names' is not a valid column — try 'name'."*

---

## Running Tests

```bash
python test_compiler.py
```

Covers: valid queries, lexical errors, syntax errors, semantic errors, and AI suggestion accuracy.

---

## Team

| Name | Role |
|---|---|
| Mansi Rawat | Compiler phases, AI integration |
| Vinayak Sharma | Backend, project lead |
| Devang Saklani | Frontend, UI/UX |
| Sakshi Kaintura | Testing, documentation |

---

## License

This project is for academic purposes at Graphic Era (Deemed to be University).
