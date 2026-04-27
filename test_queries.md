# Test Queries for SQL Validation System

Run these queries in the web interface to verify compiler phase checks.

## 1. Perfectly Valid Query
**Input:** `SELECT name, age FROM students;`
**Expected Outcome:**
- **Tokens:** Keywords (`SELECT`, `FROM`), Identifiers (`name`, `age`, `students`), Symbols (`,`, `;`).
- **Syntax:** AST successfully built.
- **Semantic:** Target table `students` and columns `name`, `age` exist in Schema. Valid.
- **Errors:** None.

## 2. Lexical Error
**Input:** `SELECT name @ FROM students;`
**Expected Outcome:**
- **Lexical Analyzer** catches invalid character `@`. Token generation continues after it.
- **Errors:** "Lexical Error: Invalid character '@' at position ..."

## 3. Syntax Error (Missing Columns)
**Input:** `SELECT FROM students;`
**Expected Outcome:**
- **Parser** fails to find column `IDENTIFIER`s after `SELECT`.
- **Errors:** "Syntax Error: Missing column selection."

## 4. Syntax Error (Misplaced Keywords)
**Input:** `SELECT name students FROM;`
**Expected Outcome:**
- **Parser** expects `FROM` before `students`. Fails grammar structure.
- **Errors:** "Syntax Error: Unexpected token 'students' in column list."

## 5. Semantic Error & Suggestion (Unknown Table)
**Input:** `SELECT name FROM studants;`
**Expected Outcome:**
- **Syntax Analysis** passes (proper SQL sentence layout).
- **Semantic Analyzer** flags `studants` not existing in Schema.
- **AI Suggestion Engine** calculates Levenshtein distance and proposes `students`.
- **Errors:** "Semantic Error: Unknown table 'studants'."
- **Suggestions:** "Did you mean table 'students' instead of 'studants'?"

## 6. Semantic Error & Suggestion (Unknown Column)
**Input:** `SELECT names, ages FROM students;`
**Expected Outcome:**
- **Semantic Analyzer** spots `names` and `ages` missing from schema.
- **Errors:** "...Unknown column 'names'...", "...Unknown column 'ages'..."
- **Suggestions:** "Did you mean column 'name' instead of 'names'?" "Did you mean column 'age' instead of 'ages'?"

## 7. AI Keyword Fix 
**Input:** `SELEC name FROM students;`
**Expected Outcome:**
- **Lexical Analyzer** classes `SELEC` as an `IDENTIFIER` since it's not a strict known `KEYWORD`.
- **Parser** will fail the syntax check since query doesn't start with recognized keyword.
- **AI Engine** assesses all `IDENTIFIER`s. Flags `SELEC` as highly likely misspelled `SELECT`.
- **Suggestions:** "Identifier 'SELEC' might be misspelled. Did you mean keyword 'SELECT'?"

## 8. DROP TABLE Validation
**Input:** `DROP TABLE students;`
**Expected Outcome:**
- **Tokens:** Keywords (`DROP`, `TABLE`), Identifier (`students`).
- **Syntax Analysis:** Successfully parses Table drop structure.
- **Errors:** None (if `students` exist in the logic constraints).

## 9. TRUNCATE TABLE Validation
**Input:** `TRUNCATE TABLE employees;`
**Expected Outcome:**
- **Tokens:** Keywords (`TRUNCATE`, `TABLE`), Identifier (`employees`).
- **Syntax Analysis:** Successfully maps to TRUNCATE block.

## 10. Complex Semantic Analysis Evaluation
**Input:** `SELECT id, name, salary FROM employees WHERE salary > 5000 AND role LIKE 'manager';`
**Expected Outcome:**
- Robust test representing long parsed keywords (LIKE, AND, >) and nested expression validation. AST SVG will span wider to test the scroll feature.
