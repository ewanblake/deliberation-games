```mermaid
stateDiagram-v2
direction LR

[*] --> NoCommitment
NoCommitment --> ActiveCommitment : PROPOSE

ActiveCommitment --> ActiveCommitment : SUPPORT
ActiveCommitment --> Finalised : ACCEPT
ActiveCommitment --> Removed : REJECT / WITHDRAW

Finalised --> [*]
Removed --> [*]
```