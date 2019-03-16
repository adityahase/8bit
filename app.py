from flask import Flask, jsonify, render_template, request
from emulator import Emulator


app = Flask(__name__, static_url_path='/static')

@app.route("/emulate", methods=['POST'])
def emulate():
    data = request.get_json(force=True)
    program = [i.split() for i in data["program"]]
    emulator = Emulator(data["memory"], program, data["registers"])
    states = list(emulator.run())
    return jsonify(states)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
