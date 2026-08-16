from app.dialogue.commitment import Commitment
from app.dialogue.burden import BurdenManager

def test_duplicate_suppport_is_prevented():

    commitment = Commitment(
        "Travel by Train",
        "Agent A"
    )

    assert commitment.add_support("Agent B") is True
    assert commitment.add_support("Agent B") is False
    assert commitment.supports == 1

def test_duplicate_challenge_is_prevented():

    commitment = Commitment(
        "Travel by Train",
        "Agent A"
    )

    assert commitment.mark_challenged() is True
    assert commitment.mark_challenged() is False


def test_burden_lifecycle():

    burden = BurdenManager()

    burden.create_burden(
        "Agent A",
        "Travel by Train"
    )

    assert burden.get_status() == "CREATED"

    burden.activate_burden()

    assert burden.get_status() == "ACTIVE"

    burden.satisfy_burden()

    assert burden.get_status() == "SATISFIED"

    burden.resolve_burden()

    assert burden.has_burden() is False

