```mermaid
sequenceDiagram

participant A as Agent A
participant B as Agent B

A->>B: PROPOSE(Travel by Train)

B->>A: CHALLENGE

A->>B: SUPPORT(Cheaper)

B->>A: ACCEPT

Note over A,B: Dialogue Closes
```