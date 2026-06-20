from flask import Flask

from app.dialogue.engine import DialogueEngine

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
    app.run(debug=True)