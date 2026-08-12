from flask import Flask

from app.dialogue.engine import DialogueEngine
from app.dialogue.engine import (
    run_multiple_simulations,
    run_comparative_batch
)

app = Flask(__name__)

@app.route("/")
def home():
    return "Deliberation Games"

@app.route("/simulate")
def simulate():

    engine = DialogueEngine()

    engine.run()

    return "Simulation complete!"

if __name__ == "__main__":
    run_multiple_simulations(
        protocol="Standard",
        simulation_count=0
    )