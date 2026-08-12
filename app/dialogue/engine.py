import random

from app.dialogue.states import DialogueState
from app.dialogue.moves import MoveType
from app.dialogue.agents import Agent
from app.dialogue.scenarios import TRAVEL_OPTIONS
from app.dialogue.transcript import TranscriptManager
from app.dialogue.commitment_store import CommitmentStore
from app.dialogue.burden import BurdenManager

class DialogueEngine:

    def __init__(
            self,
            protocol = "Standard"
    ):

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
        self.burden = BurdenManager()

        self.turn_count = 0
        self.max_turns = 30
        self.termination_reason = None

        self.protocol = protocol

        if self.protocol not in ["Standard", "Burden"]:
            raise ValueError(
                "Protocol must be either 'Standard' or 'Burden'!"
            )

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

           # Active burden!

           if (
               self.protocol == "Burden"
               and self.burden.is_active()
           ):
               
               # Burden holder's turn

               if (
                   self.current_agent.name
                   ==
                   self.burden.get_owner()
               ):
                   
                   return [
                       MoveType.SUPPORT,
                       MoveType.WITHDRAW
                   ]
               
               # Other participant then waits

               return []
           
           # The standard move collection

           if self.current_proposal:
               
               # Each agent can only support a current proposal once during its lifespan
               if not self.commitment_store.has_supported(
                   self.current_proposal,
                   self.current_agent.name
               ):

                   legal_moves.append(
                       MoveType.SUPPORT
                   )

                # Each proposal can only receive one challenge
               if not self.commitment_store.has_been_challenged(
                    self.current_proposal
                ):

                   legal_moves.append(
                       MoveType.CHALLENGE
                   )

                # ACCEPT and REJECT remain available whilst the proposal is active
               legal_moves.extend([
                    MoveType.ACCEPT,
                    MoveType.REJECT
                ])

                

                

                   

           # Do not introduce another proposal whilst a proposal is being currently considered
           if self.current_proposal is None:

               legal_moves.append(
                   MoveType.PROPOSE
               )

           if (
               self.current_proposal
               and
               self.commitment_store.get_owner(
                   self.current_proposal
               )
               ==
               self.current_agent.name
           ):
               
               legal_moves.append(MoveType.WITHDRAW)
           
        return legal_moves

    def propose(self):


        # Only one proposal can be under consideration at any time!
        if self.current_proposal is not None:

            print(
                "Cannot introduce a new proposal whilst another proposal is active!"
            )

            return False

        # Select a travel option to put forward at random for the discussion
        available = [

            proposal
            for proposal in TRAVEL_OPTIONS

            if not self.commitment_store.proposal_exists(proposal)

        ]

        if not available:

            print("No new proposals available!")

            self.termination_reason = "NO_PROPOSALS_REMAIN"

            self.state = DialogueState.CLOSING

            return
        
        proposal = random.choice(available)

        self.current_proposal = proposal
        self.proposal_owner = self.current_agent.name
        self.commitment_store.create_commitment(
            proposal,
            self.current_agent.name
        )

        if self.protocol == "Burden":

            self.burden.create_burden(
                owner = self.current_agent.name,
                proposal = proposal
            )

        commitment = self.commitment_store.get_commitment(proposal)

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.PROPOSE.value} "
            f"'{proposal}'"
        )

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.PROPOSE.value,
            proposal=proposal,
            target_proposal=None,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=(
                "CREATED"
                if self.protocol == "Burden"
                else None
            ),
            **burden_data
            
        )

        self.commitment_store.display()

        # The first proposal moves the dialogue into the DELIBERATION state       
        if self.state == DialogueState.OPENING:
            self.state = DialogueState.DELIBERATION

        return True

        

    def support(self):

        burden_event = None

        if (
            self.protocol == "Burden"
            and self.burden.is_active()
            and self.current_agent.name == self.burden.get_owner()
        ):
            if self.burden.satisfy_burden():

                burden_event = "SATISFIED"

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.SUPPORT.value}"
        )

        self.commitment_store.support_commitment(
            self.current_proposal,
            self.current_agent.name
        )

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.SUPPORT.value,
            proposal=None,
            target_proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=burden_event,
            **burden_data
            )
        

        self.commitment_store.display()

    def challenge(self):

        # A challenge is unable to be made if a burden is currently active
        if (
            self.protocol == "Burden"
            and
            self.burden.is_active()
        ):

            print(
                "Challenge rejected: An existing burden is already active!"
            )

            return False

        print(
            f"{self.current_agent.name}: "
            f"{MoveType.CHALLENGE.value}"
        )

        burden_event = None

        if self.protocol == "Burden":

            if self.burden.activate_burden():

                burden_event = "ACTIVATED"

        commitment = self.commitment_store.get_commitment(
            self.current_proposal
        )

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.CHALLENGE.value,
            proposal=None,
            target_proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=burden_event,
            **burden_data
        )

        self.commitment_store.display()

        return True

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

        burden_event = None

        if self.protocol == "Burden":

            if self.burden.has_burden():

                burden_event = "RESOLVED"

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.ACCEPT.value,
            proposal=None,
            target_proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=burden_event,
            **burden_data
        )

        self.commitment_store.display()

        if self.protocol == "Burden":

            self.burden.remove_burden()

        self.termination_reason = "PROPOSAL ACCEPTED"
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

        burden_event = None

        if (
            self.protocol == "Burden"
            and
            self.burden.has_burden()
        ):

            burden_event = "RESOLVED"

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.REJECT.value,
            proposal=None,
            target_proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=burden_event,
            **burden_data
        )

        self.commitment_store.display()

        if self.protocol == "Burden":

            self.burden.remove_burden()

        if not self.commitment_store.has_active_commitments():
            self.termination_reason = "PROPOSAL_REJECTED"
            self.state = DialogueState.CLOSING

        # Remove the proposal so a new one can be introduced later on
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

        burden_event = None

        if (
            self.protocol == "Burden"
            and 
            self.burden.has_burden()
        ):

            burden_event = "RESOLVED"

        burden_data = (
            self.burden.to_dict()
            if self.protocol == "Burden"
            else {}
        )

        self.transcript.record_turn(
            turn=self.turn_count,
            agent=self.current_agent.name,
            state=self.state.value,
            move=MoveType.WITHDRAW.value,
            proposal=None,
            target_proposal=self.current_proposal,
            commitment_status=commitment.status,
            support_count=commitment.supports,
            burden_event=burden_event,
            **burden_data
        )

        self.commitment_store.display()

        if self.protocol == "Burden":
                    
            self.burden.remove_burden()

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
            if self.turn_count > self.max_turns:

                print("Maximum dialogue length reached!")
                self.termination_reason = "MAX_TURNS_REACHED"
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

                if not legal_moves:

                    if (
                        self.protocol == "Burden"
                        and self.burden.is_active()
                    ):

                        print(
                            "Waiting for burden holder to respond!"
                        )

                        self.switch_turn()
                        continue

                    print("No legal moves remain!")

                    self.termination_reason = "NO_LEGAL_MOVES"
                    self.state = DialogueState.CLOSING

                    break

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

        outcome = self.termination_reason or "UNKNOWN"

        accepted_proposal = None

        if self.termination_reason == "PROPOSAL_ACCEPTED":
            accepted_proposal = self.current_proposal

        self.transcript.save(
            protocol=self.protocol,
            outcome=outcome,
            accepted_proposal=accepted_proposal,
            termination_reason=self.termination_reason
        )

        print("Transcript Saved")



def run_simulation(protocol):
    """
    Run a single dialogue simulation using the specified protocol!
    """

    print("=" * 50)
    print(f"Running {protocol} Protocol Simulation")
    print("=" * 50)

    engine = DialogueEngine(protocol=protocol)

    engine.run()

    return engine


def run_comparative_simulation():
    """
    Runs one Standard protocol and one Burden of Proposing protocol simulation
    """

    print()
    print("#" * 60)
    print("COMPARATIVE DIALOGUE SIMULATION")
    print("#" * 60)

    standard_engine = DialogueEngine(
        protocol="Standard"
    )

    standard_engine.run()

    print()
    print("#" * 60)
    print("STANDARD SIMULATION COMPLETE")
    print("#" * 60)
    print()

    burden_engine = DialogueEngine(
        protocol="Burden"
    )

    burden_engine.run()

    print()
    print("#" * 60)
    print("BURDEN SIMULATION COMPLETE")
    print("#" * 60)

    return {
        "standard": standard_engine,
        "burden": burden_engine
    }


