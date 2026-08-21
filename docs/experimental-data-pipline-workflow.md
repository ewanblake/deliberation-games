```mermaid
flowchart TD

A[Simulated Dialogue] --> B[Individual Dialogue Turns]

B --> C[TranscriptManager]

C --> D[Structured JSON Transcript]

D --> E[Statistics Extraction]

E --> F[Excel Dataset]

F --> G[Comparative Evaluation]
```