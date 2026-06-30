class Commitment:

    def __init__(self, proposal, owner):

        # Represents a proposal currently under discussion
        self.proposal = proposal
        self.owner = owner

        # New commitments begin in the active state
        self.status = "ACTIVE"

        # Tracks the number of agents who have supported the proposal
        self.supports = 0

    def add_support(self):

        self.supports += 1

    def accept(self):

        self.status = "ACCEPTED"

    def reject(self):

        self.status = "REJECTED"

    def withdraw(self):

        self.status = "WITHDRAWN"