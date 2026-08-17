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
            burden_proposal=None,
            burden_event=None
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
            "burden_proposal": burden_proposal,
            "burden_event": burden_event
        }

        self.turns.append(turn_data)

    def save(
            self,
            protocol="Standard",
            outcome="UNKNOWN",
            accepted_proposal=None,
            termination_reason="Unknown"
    ):

        folder = "app/transcripts"

        # Will create the transcript directory if it does not exist already
        os.makedirs(
            folder, 
            exist_ok=True)

        existing_files = [
            file
            for file in os.listdir(folder)
            if file.startswith("dialogue_") 
            and file.endswith(".json")

        ]

        next_number = len(existing_files) + 1

        statistics = {
            "proposals": 0,
            "supports": 0,
            "challenges": 0,
            "accepts": 0,
            "rejects": 0,
            "withdrawals": 0,
            "burdens_created": 0,
            "burdens_activated": 0,
            "burdens_satisfied": 0,
            "burdens_resolved": 0,
            "active_commitments": 0
        }

        for turn in self.turns:

            move = turn["move"]
            burden_event = turn["burden_event"]

            if move == "PROPOSE":
                statistics["proposals"] += 1

            elif move == "SUPPORT":
                statistics["supports"] += 1

            elif move == "CHALLENGE":
                statistics["challenges"] += 1

            elif move == "ACCEPT":
                statistics["accepts"] += 1

            elif move == "REJECT":
                statistics["rejects"] += 1

            elif move == "WITHDRAW":
                statistics["withdrawals"] += 1

            if burden_event == "CREATED":
                statistics["burdens_created"] += 1

            elif burden_event == "ACTIVATED":
                statistics["burdens_activated"] += 1

            elif burden_event == "SATISFIED":
                statistics["burdens_satisfied"] += 1

            elif burden_event == "RESOLVED":
                statistics["burdens_resolved"] += 1

            if turn["commitment_status"] == "ACTIVE":
                statistics["active_commitments"] += 1

        # Builds complete structure of the transcript for exporting
        transcript = {
            "dialogue_id": next_number,
            "scenario": "Travel Planning",
            "protocol": protocol,
            "turn_count": len(self.turns),
            "outcome": outcome,
            "termination_reason": termination_reason,
            "accepted_proposal": accepted_proposal,
            "statistics": statistics,
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
