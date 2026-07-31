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
            support_count=None,
            burden_status=None,
            burden_owner=None,
            burden_proposal=None
    ):
        turn_data = {
            "turn": turn,
            "agent": agent,
            "state": state,
            "move": move,
            "proposal": proposal,
            "target_proposal": target_proposal,
            "commitment_status": commitment_status,
            "support_count": support_count,
            "burden_status": burden_status,
            "burden_owner": burden_owner,
            "burden_proposal": burden_proposal
        }

        self.turns.append(turn_data)

    def save(
            self,
            protocol=None,
            outcome=None,
            accepted_proposal=None
    ):

        folder = "app/transcripts"

        # Will create the transcript directory if it does not exist already
        os.makedirs(
            folder, 
            exist_ok=True)

        existing_files = [
            file
            for file in os.listdir(folder)
            if file.startswith("dialogue_") and file.endswith(".json")

        ]

        next_number = len(existing_files) + 1

        # Builds complete structure of the transcript for exporting
        transcript = {
            "dialogue_id": next_number,
            "scenario": "Travel Planning",
            "protocol": protocol,
            "outcome": outcome,
            "accepted_proposal": accepted_proposal,
            "turn_count": len(self.turns),
            "turns": self.turns
        }     

        filename = os.path.join(
            folder,
            f"dialogue_{next_number:03}.json"
        )
        
        # Saves the transcript, formatted as JSON for readability purposes
        with open(filename, "w") as file:

            json.dump(
                transcript,
                file,
                indent=4
            )
