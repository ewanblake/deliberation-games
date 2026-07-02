from app.dialogue.commitment import Commitment

class CommitmentStore:

    def __init__(self):

        # Stores commitments made by each agent
        self.commitments = {
            "Agent A": [],
            "Agent B": [],
        }

    def create_commitment(self, proposal, owner):

        # An agent may only have one active commitment at a time
        self.commitments[owner].clear()

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
    
    def get_commitment(self, proposal):
        
        return self.find_commitment(proposal)
    
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
    
    def display(self):
        
        print()
        print("Commitment Store")
        print("-" * 30)


        for agent, commitments in self.commitments.items():

            print(f"{agent}:")

            if not commitments:

                print(" No commitments")

            for commitment in commitments:

                print(f" Proposal  : {commitment.proposal}")
                print(f" Status    : {commitment.status}")
                print(f" Supports  : {commitment.supports}")

        print("-" * 30)