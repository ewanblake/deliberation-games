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