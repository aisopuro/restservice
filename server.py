from flask import Flask
from flask.json import jsonify

app = Flask(__name__)


@app.route('/')
def index():
    response = {'success': 'nothing here yet'}
    return jsonify(response)

if __name__ == "__main__":
    app.run()
