```mermaid
stateDiagram-v2

    [*] --> OPENING

    OPENING --> DELIBERATION : First Proposal

    DELIBERATION --> CLOSING : Proposal Accepted
    DELIBERATION --> CLOSING : Proposal Rejected
    DELIBERATION --> CLOSING : No Proposals Remain
    DELIBERATION --> CLOSING : No Legal Moves
    DELIBERATION --> CLOSING : Max Turns Reached

    CLOSING --> [*]
```
