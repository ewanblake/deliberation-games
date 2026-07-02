import random

from app.dialogue.states import DialogueState
from app.dialogue.moves import MoveType
from app.dialogue.agents import Agent
from app.dialogue.scenarios import TRAVEL_OPTIONS
from app.dialogue.transcript import TranscriptManager
from app.dialogue.commitment_store import CommitmentStore

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
        self.proposal_owner = None

        self.transcript = TranscriptManager()
        self.commitment_store = CommitmentStore()

        self.turn_count = 0
        self.max_turns = 10

    def switch_turn(self):

        # Alternates between the two agents after each turn is completed
        if self.current_agent == self.agent_a:
            self.current_agent = self.agent_b
        else:
            self.current_agent = self.agent_a

    def get_legal_moves(self):

        legal_moves = []

        if self.state == DialogueState.OPENING:

            # A dialogue must begin with a proposal
            legal_moves.append(MoveType.PROPOSE)

            return legal_moves
        
        if self.state == DialogueState.DELIBERATION:

            # Once a proposal exists, agents can then respond to it
            if self.current_proposal:

                legal_moves.extend([
                    MoveType.SUPPORT,
                    MoveType.CHALLENGE,
                    MoveType.ACCEPT,
                    MoveType.REJECT
                ])
            
            # Agents can introduce a new proposal during the DELIBERATION state
            legal_moves.append(MoveType.PROPOSE)

            # Only the agent who made the current proposal can WITHDRAW it
            if (
                self.current_proposal and
                self.commitment_store.get_owner(
                    self.current_proposal
                ) == self.current_agent.name
            ):
                legal_moves.append(MoveType.WITHDRAW)

        return legal_moves

    def propose(self):

        # Select a travel option to put forward at random for the discussion
        proposal = random.choice(TRAVEL_OPTIONS)

        self.current_proposal = proposal
        self.commitment_store.create_commitment(
            proposal,
            self.current_agent.name
        )

        commitment = self.commitment_store.get_commitment(proposal)

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
            proposal=proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
            
        )

        self.commitment_store.display()

        # The first proposal moves the dialogue into the DELIBERATION state       
        if self.state == DialogueState.OPENING:
            self.state = DialogueState.DELIBERATION

        

    def support(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.SUPPORT.value}"
        )

        self.commitment_store.support_commitment(
            self.current_proposal
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.SUPPORT.value,
            proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
        )

        self.commitment_store.display()

    def challenge(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.CHALLENGE.value}"
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.CHALLENGE.value,
            proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
        )

        self.commitment_store.display()

    def accept(self):
        
        print(
            f"{self.current_agent.name}: "
            f"{MoveType.ACCEPT.value}"
        )

        self.commitment_store.accept_commitment(
            self.current_proposal
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.ACCEPT.value,
            proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
        )

        self.commitment_store.display()

        # Acceptance ends the dialogue successfully
        self.state = DialogueState.CLOSING

    def reject(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.REJECT.value}"
        )

        self.commitment_store.reject_commitment(
            self.current_proposal
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.REJECT.value,
            proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
        )

        

        self.commitment_store.display()

        # Remove the proposal to a new one can be introduced later
        self.current_proposal = None
        self.proposal_owner = None

    def withdraw(self):

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.WITHDRAW.value}"
        )

        self.commitment_store.withdraw_commitment(
            self.current_proposal
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.WITHDRAW.value,
            proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports
        )

        self.commitment_store.display()

        self.current_proposal = None
        self.proposal_owner = None   

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

                legal_moves = self.get_legal_moves()

                move = random.choice(legal_moves)

                if move == MoveType.ACCEPT:
                    self.accept()

                elif move == MoveType.REJECT:
                    self.reject()

                elif move == MoveType.PROPOSE:
                    self.propose()

                elif move == MoveType.SUPPORT:
                    self.support()
                
                elif move == MoveType.CHALLENGE:
                    self.challenge()

                elif move == MoveType.WITHDRAW:
                    self.withdraw()

            print()

            # Only switch turns if the dialogue is still active!
            if self.state != DialogueState.CLOSING:
                self.switch_turn()

        print("Dialogue Ended")

        self.transcript.save()

        print("Transcript Saved")





