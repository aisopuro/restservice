from flask import Flask
from flask.json import jsonify
from backend import Backend

app = Flask(__name__)
backend = Backend()


@app.route('/')
def index():
    response = backend.get_root()
    return jsonify(response)

if __name__ == "__main__":
    app.run()
