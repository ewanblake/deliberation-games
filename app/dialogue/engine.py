import random

from states import DialogueState
from moves import MoveType
from agents import Agent
from scenarios import TRAVEL_OPTIONS

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