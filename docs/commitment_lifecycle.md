```mermaid
stateDiagram-v2

[*] --> NoCommitment

NoCommitment --> ActiveCommitment : PROPOSE

ActiveCommitment --> ActiveCommitment : SUPPORT

ActiveCommitment --> Finalised : ACCEPT

ActiveCommitment --> Removed : REJECT

ActiveCommitment --> Removed : WITHDRAW

Finalised --> [*]

Removed --> [*]
```