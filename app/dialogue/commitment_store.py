from app.dialogue.commitment import Commitment

class CommitmentStore:

    def __init__(self):

        # Stores commitments made by each agent
        self.commitments = {
            "Agent A": [],
            "Agent B": [],
        }

    def create_commitment(self, proposal, owner):

        commitment = Commitment(proposal, owner)

        self.commitments[owner].append(commitment)

        return commitment
    
    def find_commitment(self, proposal):

        # Search both agents' commitments for the specified proposal
        for agent_commitments in self.commitments.values():

            for commitment in agent_commitments:

                if commitment.proposal == proposal:

                    return commitment
                
        return None
    
    def support_commitment(self, proposal):

        commitment = self.find_commitment(proposal)

        if commitment:

            commitment.add_support()

    def accept_commitment(self, proposal):

        commitment = self.find_commitment(proposal)

        if commitment:

            commitment.accept()

    def reject_commitment(self, proposal):
        
        commitment = self.find_commitment(proposal)

        if commitment:

            commitment.reject()

    def withdraw_commitment(self, proposal):

        commitment = self.find_commitment(proposal)

        if commitment:

            commitment.withdraw()

    def get_owner(self, proposal):

        commitment = self.find_commitment(proposal)

        if commitment:

            return commitment.owner
        
        return None