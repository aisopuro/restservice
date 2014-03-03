from flask import Flask, request
from backend import Backend
from json import dumps

app = Flask(__name__)
backend = Backend()


@app.route('/', methods=['GET'])
def index():
    response = "This is restservice. Specify a url to use the REST interface"
    return response


@app.route('/products/', methods=['GET'])
def get_products():
    return dumps(backend.get_products(request.args))

if __name__ == "__main__":
    app.run()
