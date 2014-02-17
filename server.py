from flask import Flask
from flask.json import jsonify
from backend import Backend

app = Flask(__name__)
backend = Backend()


@app.route('/')
def index():
    response = backend.get_root()
    r = jsonify(response)
    print r
    return r

if __name__ == "__main__":
    app.run()
