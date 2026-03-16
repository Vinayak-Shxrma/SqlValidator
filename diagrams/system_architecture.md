# System Architecture

```mermaid
flowchart TD
    %% Styling
    classDef ui fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef phase fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef engine fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef db fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;

    %% Components
    UI[Web Interface]:::ui
    Lex[Lexical Analyzer\n(Tokenization)]:::phase
    Parse[Syntax Analyzer\n(AST Generation)]:::phase
    Sem[Semantic Analyzer\n(Validation)]:::phase
    DB[(Schema Database)]:::db
    AI[AI Suggestion Engine\n(Error Correction)]:::engine
    Err[Error Reporting Module]:::engine

    %% Flow
    UI -->|Raw SQL Query| Lex
    Lex -->|Tokens| Parse
    Parse -->|Abstract Syntax Tree| Sem
    
    %% Semantic DB check
    DB -.->|Table & Column rules| Sem
    DB -.->|Schema Metadata| AI
    
    %% AI Correction
    Lex -.->|Lexical Errors| AI
    Parse -.->|Syntax Errors| AI
    Sem -.->|Semantic Errors| AI
    
    %% Returns
    AI -->|Generated Suggestions| Err
    Lex -->|Tokens| Err
    Parse -->|AST| Err
    Sem -->|Validation Status| Err
    
    Err -->|Formatted JSON Response| UI
```
