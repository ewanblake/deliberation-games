from flask import Flask, render_template, request

from app.dialogue.engine import DialogueEngine
from app.dialogue.engine import (
    run_multiple_simulations,
    run_comparative_batch
)

from app.dialogue.excel_export import export_comparative_results

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():

    return render_template(
        "index.html"
    )

@app.route("/simulate", methods=["POST"])
def simulate():

    protocol = request.form.get(
        "protocol",
        "Standard"
    )

    simulation_count = request.form.get(
        "simulation_count",
        "1"
    )

    try:

        simulation_count = int(
            simulation_count
        )

        if simulation_count < 1:
            simulation_count = 1

        if simulation_count > 100:
            simulation_count = 100

    except ValueError:

        simulation_count = 1

    engines = run_multiple_simulations(
        protocol=protocol,
        simulation_count=simulation_count
    )

    if protocol == "Standard":

        excel_file = export_comparative_results(
            standard_engines=engines,
            burden_engines=[]
        )

    else:

        excel_file = export_comparative_results(
            standard_engines=[],
            burden_engines=engines
        )

    results = []

    for number, engine in enumerate(
        engines, 
        start=1
    ):

        move_counts = {
            "PROPOSE": 0,
            "SUPPORT": 0,
            "CHALLENGE": 0,
            "ACCEPT": 0,
            "REJECT": 0,
            "WITHDRAW": 0
        }

        for turn in engine.transcript.turns:

            move = turn.get("move")

            if move in move_counts:
                move_counts[move] += 1

        burden_events = {
            "CREATED": 0,
            "ACTIVATED": 0,
            "SATISFIED": 0,
            "RESOLVED": 0
        }

        if protocol == "Burden":

            for turn in engine.transcript.turns:

                event = turn.get(
                    "burden_event"
                )

                if event in burden_events:
                    burden_events[event] += 1

        results.append({
            "simulation_number": number,
            "protocol": protocol,
            "turn_count": len(
                engine.transcript.turns
            ),
            "outcome": (
                engine.termination_reason
                or "UNKNOWN"
            ),
            "move_counts": move_counts,
            "burden_events": burden_events,
            "transcript": engine.transcript.turns
        })

    total_turns = sum(
        result["turn_count"]
        for result in results
    )

    average_turns = (
        round(
            total_turns / len(results),
            2
        )
        if results
        else 0
    )

    accepted = sum(
        1
        for result in results
        if result["outcome"]
        == "PROPOSAL_ACCEPTED"
    )

    rejected = sum(
        1
        for result in results
        if result["outcome"]
        == "PROPOSAL_REJECTED"
    )

    summary = {
        "protocol": protocol,
        "simulation_count": simulation_count,
        "average_turns": average_turns,
        "accepted": accepted,
        "rejected": rejected,
        "excel_file": excel_file
    }

    return render_template(
        "index.html",
        results=results,
        summary=summary
    )

if __name__ == "__main__":

    app.run(
        debug=True
    )