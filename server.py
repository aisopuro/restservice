from flask import Flask, request
from backend import Backend
from json import dumps
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

app = Flask(__name__)
backend = Backend()


@app.route('/', methods=['GET'])
def index():
    response = "This is restservice. Specify a url to use the REST interface"
    return response


@app.route('/products/', methods=['GET'])
def get_products():
    return dumps(backend.get_products(request.args))


@app.route('/products/available', methods=['GET'])
def get_available_products():
    args = MultiDict(request.args)
    args.add('minamount', 1)
    return dumps(backend.get_products(args))


@app.route('/products/categories/', methods=['GET'])
def get_categories():
    return dumps(backend.get_categories())


@app.route('/products/categories/<category>', methods=['GET'])
def get_by_category(category):
    args = MultiDict(request.args)
    args.add('category', category)
    return dumps(backend.get_products(args))

if __name__ == "__main__":
    app.run()
