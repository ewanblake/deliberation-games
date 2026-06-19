```mermaid
stateDiagram-v2

[*] --> OPENING

OPENING --> DELIBERATION : First Proposal

DELIBERATION --> CLOSING : Proposal Accepted

DELIBERATION --> CLOSING : No Valid Moves

DELIBERATION --> CLOSING : Max Turns Reached

CLOSING --> [*]
```