class Commitment:

    def __init__(self, proposal, owner):

        # Represents a current proposal under discussion
        self.proposal = proposal
        self.owner = owner

        # Fresh commitments start in the active state
        self.status = "ACTIVE"

        # Tracks which agents have supported the proposal
        self.supporters = set()

        # Tracks whether the proposal has already been challenged
        self.challenged = False

    @property
    def supports(self):

        return len(self.supporters)

    def add_support(self, agent):

        # Each agent can only support the proposal once and only once!
        if agent in self.supporters:
            return False

        self.supports.add(agent)

        return True

    def has_supported(self, agent):

        return agent in self.supporters


    def mark_challenged(self):

        # A proposal can only be challenged once!
        if self.challenged:
            return False

        self.challenged = True

        return True

    def has_been_challenged(self):

        return self.challenged

    def accept(self):

        self.status = "ACCEPTED"

    def reject(self):

        self.status = "REJECTED"

    def withdraw(self):
        self.status = "WITHDRAWN" 