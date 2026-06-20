import random

from app.dialogue.states import DialogueState
from app.dialogue.moves import MoveType
from app.dialogue.agents import Agent
from app.dialogue.scenarios import TRAVEL_OPTIONS

class DialogueEngine:

    def __init__(self):

        self.state = DialogueState.OPENING
        self.agent_a = Agent("Agent A")
        self.agent_b = Agent("Agent B")

        self.current_agent = self.agent_a

        self.current_proposal = None

        self.turn_count = 0
        self.max_turns = 10

    def switch_turn(self):

        if self.current_agent == self.agent_a:
            self.current_agent = self.agent_b
        else:
            self.current_agent = self.agent_a

    def propose(self):

        proposal = random.choice(TRAVEL_OPTIONS)

        self.current_proposal = proposal

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.PROPOSE.value} "
            f"'{proposal}'"
        )
        
        if self.state == DialogueState.OPENING:
            self.state = DialogueState.DELIBERATION

    def accept(self):
        
        print(
            f"{self.current_agent.name}: "
            f"{MoveType.ACCEPT.value}"
        )

        self.state = DialogueState.CLOSING

    def reject(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.REJECT.value}"
        )

        self.current_proposal = None

    def run(self):

        print("Dialogue Started")
        print()

        while self.state != DialogueState.CLOSING:

            self.turn_count += 1

            print(f"Turn {self.turn_count}")
            print(f"State: {self.state.value}")

            if self.turn_count >= self.max_turns:

                print("Maximum turns reached.")
                self.state = DialogueState.CLOSING
                break

            # OPENING State Below
            if self.state == DialogueState.OPENING:

                self.propose()

            # DELIBERATION State Below
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

            if self.state != DialogueState.CLOSING:
                self.switch_turn()

        print("Dialogue Ended")





