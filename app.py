from flask import Flask, jsonify, render_template, request
from emulator import Emulator, MEMORY_SIZE, REGISTER_MAP


app = Flask(__name__, static_url_path='/static')

@app.route("/emulate", methods=['POST'])
def emulate():
    data = request.get_json(force=True)
    if data:
        program = [i.split() for i in data["program"].split("\n") if i]
        emulator = Emulator(data["memory"], program, data["registers"])
        states = list(emulator.run())
        if not states:
            states = [emulattor.state()]
    else:
        states = [
            {
                "memory": [0]*MEMORY_SIZE,
                "registers": {key:0 for key in REGISTER_MAP}
            }
        ]
    return jsonify(states)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
