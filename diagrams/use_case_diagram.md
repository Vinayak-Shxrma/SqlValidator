# Use Case Diagram

```mermaid
usecaseDiagram
    actor Student
    actor "System/Compiler" as System
    
    usecase "Submit SQL Query" as UC1
    usecase "View Tokenized Output" as UC2
    usecase "View Parsing Errors" as UC3
    usecase "View Semantic Errors" as UC4
    usecase "Receive AI Suggestions" as UC5
    usecase "Validate against Schema" as UC6
    
    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    
    System --> UC6
    
    UC1 ..> UC2 : <<includes>>
    UC1 ..> UC3 : <<includes>>
    UC1 ..> UC4 : <<includes>>
    UC1 ..> UC5 : <<includes>>
    
    UC4 ..> UC6 : <<includes>>
```
