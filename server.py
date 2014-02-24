from flask import Flask, request
from flask.json import jsonify
from backend import Backend

app = Flask(__name__)
backend = Backend()


@app.route('/')
def index():
    response = "This is restservice. Specify a url to use the REST interface"
    return response


@app.route('/products/', methods=['GET'])
def get_products():
    return str(request.args)

if __name__ == "__main__":
    app.run()
