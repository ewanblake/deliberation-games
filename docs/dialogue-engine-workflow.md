```mermaid
flowchart TD

    A([Start Dialogue])

    B -> C[Determine Legal Moves]

    C -> D[Select Agent]

    D --> E[Generate Move]

    E --> F[Validate Move]

    F --> |Invalid| C

    F --> |Valid| G[Execute Move]

    G --> H[Update Dialogue State]

    H --> I[Updated Commitment Store]

    I --> J[Record Transcript]

    J --> K{Termination Conditions?}

    K -->|No| L[Switch Agent]

    L --> B

    K -->|Yes| M[End Dialogue]
```

