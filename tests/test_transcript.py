import json

from app.dialogue.transcript import TranscriptManager

def test_transcript_is_saved_correctly(
        tmp_path,
        monkeypatch
):

    monkeypatch.chdir(tmp_path)

    transcript = TranscriptManager()

    transcript.record_turn(
        turn=1,
        agent="Agent A",
        state="OPENING",
        move="PROPOSE",
        proposal="Travel by Train"
    )

    transcript.save(
        protocol="Standard",
        outcome="PROPOSAL_ACCEPTED",
        accepted_proposal="Travel by Train",
        termination_reason="PROPOSAL_ACCEPTED"
    )

    folder = tmp_path / "app" / "transcripts"

    files = list(
        folder.glob("dialogue_*.json")
    )

    assert len(files) == 1

    with open(files[0], "r") as file:
        data = json.load(file)

    assert data["protocol"] == "Standard"
    assert data["turn_count"] == 1
    assert data["termination_reason"] == "PROPOSAL_ACCEPTED"