import pytest

from app.dialogue.engine import DialogueEngine
from app.dialogue.moves import MoveType
from app.dialogue.states import DialogueState

def test_engine_initial_state():

    engine = DialogueEngine(protocol="Standard")

    assert engine.state == DialogueState.OPENING
    assert engine.current_agent.name == "Agent A"
    assert engine.max_turns == 30

def test_invalid_protocol_rejected():
    with pytest.raises(ValueError):
        DialogueEngine(protocol="Invalid")

def test_only_propose_legal_in_opening():

    engine = DialogueEngine(protocol="Standard")

    assert engine.get_legal_moves() == [
        MoveType.PROPOSE
    ]

def test_propose_moves_to_deliberation(monkeypatch):

    engine = DialogueEngine(protocol="Standard")

    monkeypatch.setattr(
        "app.dialogue.engine.random.choice",
        lambda options: options[0]
    )

    engine.propose()

    assert engine.state == DialogueState.DELIBERATION
    assert engine.current_proposal is not None

def test_standard_protocol_creates_no_burden(monkeypatch):

    engine = DialogueEngine(protocol="Standard")

    monkeypatch.setattr(
        "app.dialogue.engine.random.choice",
        lambda options: options[0]
    )

    engine.propose()

    assert engine.burden.has_burden() is False

def test_burden_protocol_creates_and_activates_burden(monkeypatch):

    engine = DialogueEngine(protocol="Burden")

    monkeypatch.setattr(
        "app.dialogue.engine.random.choice!",
        lambda options: options[0]
    )

    engine.propose()

    assert engine.burden.is_created()

    engine.switch_turn()
    engine.challenge()

    assert engine.burden.is_active()

def test_active_burden_restricts_proposer(monkeypatch):

    engine = DialogueEngine(protocol="Burden")

    monkeypatch.setattr(
        "app.dialogue.engine.random.choice",
        lambda options: options[0]
    )

    engine.propose()

    engine.switch_turn()
    engine.challenge()

    engine.switch_turn()

    assert set(engine.get_legal_moves()) == {
        MoveType.SUPPORT,
        MoveType.WITHDRAW
    }

def test_accept_closes_dialogue(monkeypatch):

    engine = DialogueEngine(protocol="Standard")

    monkeypatch.setattr(
        "app.dialogue.engine.random.choice",
        lambda options: options[0]
    )

    engine.propose()
    engine.accept()

    assert engine.state == DialogueState.CLOSING
    assert engine.termination_reason == "PROPOSAL_ACCEPTED"

