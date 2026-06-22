import json
import os

class TranscriptManager:

    def __init__(self):

        self.turns = []

    def record_turn(
            self,
            turn,
            agent,
            state,
            move,
            proposal=None,
            target_proposal=None
    ):
        turn_data = {
            "turn": turn,
            "agent": agent,
            "state": state,
            "move": move,
            "proposal": proposal,
            "target_proposal": target_proposal
        }

        self.turns.append(turn_data)

    def save(self):

        transcript = {
            "scenario": "Travel Planning",
            "turn_count": len(self.turns),
            "turns": self.turns
        }

        folder = "app/transcripts"

        os.makedirs(
            folder, 
            exist_ok=True)

        filename =os.path.join(
            folder,
            "dialogue_001.json"
        )

        with open(filename, "w") as file:

            json.dump(
                transcript,
                file,
                indent=4
            )
