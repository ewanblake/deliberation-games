import random

from app.dialogue.states import DialogueState
from app.dialogue.moves import MoveType
from app.dialogue.agents import Agent
from app.dialogue.scenarios import TRAVEL_OPTIONS
from app.dialogue.transcript import TranscriptManager

class DialogueEngine:

    def __init__(self):

        # Initial dialogue setup
        self.state = DialogueState.OPENING
        self.agent_a = Agent("Agent A")
        self.agent_b = Agent("Agent B")

        # Agent A will always start the conversation
        self.current_agent = self.agent_a

        # Stores the most recent proposal under discussion
        self.current_proposal = None

        self.transcript = TranscriptManager()

        self.turn_count = 0
        self.max_turns = 10

    def switch_turn(self):

        # Alternates between the two agents after each turn is completed
        if self.current_agent == self.agent_a:
            self.current_agent = self.agent_b
        else:
            self.current_agent = self.agent_a

    def propose(self):

        # Select a travel option to put forward at random for the discussion
        proposal = random.choice(TRAVEL_OPTIONS)

        self.current_proposal = proposal

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.PROPOSE.value} "
            f"'{proposal}'"
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.PROPOSE.value,
            proposal=proposal
        )

        # The first proposal moves the dialogue into the DELIBERATION state       
        if self.state == DialogueState.OPENING:
            self.state = DialogueState.DELIBERATION

    def accept(self):
        
        print(
            f"{self.current_agent.name}: "
            f"{MoveType.ACCEPT.value}"
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.ACCEPT.value,
            proposal=self.current_proposal
        )

        # Acceptance ends the dialogue successfully
        self.state = DialogueState.CLOSING

    def reject(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.REJECT.value}"
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.REJECT.value,
            proposal=self.current_proposal
        )

        # Remove the proposal to a new one can be introduced later
        self.current_proposal = None

    def run(self):

        print("Dialogue Started")
        print()

        while self.state != DialogueState.CLOSING:

            self.turn_count += 1

            print(f"Turn {self.turn_count}")
            print(f"State: {self.state.value}")

            # End the dialogue if it exceeds the allowed turn limit (10)
            if self.turn_count >= self.max_turns:

                print("Maximum turns reached.")
                self.state = DialogueState.CLOSING
                break

            # OPENING State Below
            # A dialogue must begin with a proposal!
            if self.state == DialogueState.OPENING:

                self.propose()

            # DELIBERATION State Below
            # Agents can ACCEPT, REJECT, or PROPOSE a new proposal
            elif self.state == DialogueState.DELIBERATION:

                move = random.choice([
                    MoveType.ACCEPT,
                    MoveType.REJECT,
                    MoveType.PROPOSE
                ])

                if move == MoveType.ACCEPT:
                    self.accept()

                elif move == MoveType.REJECT:
                    self.reject()

                elif move == MoveType.PROPOSE:
                    self.propose()

            print()

            # Only switch turns if the dialogue is still active!
            if self.state != DialogueState.CLOSING:
                self.switch_turn()

        print("Dialogue Ended")

        self.transcript.save()

        print("Transcript Saved")





