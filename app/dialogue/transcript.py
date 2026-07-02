import json
import os

class TranscriptManager:

    def __init__(self):

        # Stores all turns of dialogue before they are written to the disk
        self.turns = []

    def record_turn(
            self,
            turn,
            agent,
            state,
            move,
            proposal=None,
            target_proposal=None,
            commitment_status=None,
            support_count=None
    ):
        turn_data = {
            "turn": turn,
            "agent": agent,
            "state": state,
            "move": move,
            "proposal": proposal,
            "target_proposal": target_proposal,
            "commitment_status": commitment_status,
            "support_count": support_count
        }

        self.turns.append(turn_data)

    def save(self):

        # Builds complete structure of the transcript for exporting
        transcript = {
            "scenario": "Travel Planning",
            "turn_count": len(self.turns),
            "turns": self.turns
        }

        folder = "app/transcripts"

        # Will create the transcript directory if it does not exist already
        os.makedirs(
            folder, 
            exist_ok=True)

        filename =os.path.join(
            folder,
            "dialogue_001.json"
        )

        # Saves the transcript, formatted as JSON for readability purposes
        with open(filename, "w") as file:

            json.dump(
                transcript,
                file,
                indent=4
            )
