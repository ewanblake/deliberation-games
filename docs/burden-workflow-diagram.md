flowchart TD

    A[PROPOSE Executed]

    A --> B[Create Burden]

    B --> C[Status = INACTIVE]

    C --> D{CHALLENGE}

    D --> |No| E[Continue Dialogue]

    D --> |Yes| F[Activate Burden]

    F --> G[Status = ACTIVE]

    G --> H{Proposer Response}

    H --> |SUPPORT| I[Burden Satisfied]

    H --> |WITHDRAW| J[Remove Burden]

    I --> K[Status = SATISFIED]

    K --> L{Dialogue Ends?}

    L --> |ACCEPT / REJECT / WITHDRAW| M[Remove Burden]

    J --> N[Continue Dialogue]

    M --> O [Continue Dialogue]