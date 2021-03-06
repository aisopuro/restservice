from flask import Flask, request, make_response
from backend import Backend
from json import dumps
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

app = Flask(__name__)
backend = Backend()


@app.route('/', methods=['GET'])
def index():
    '''Front page'''
    return make_response(app.open_resource('index.html').read())


@app.route('/products/', methods=['GET'])
def get_products():
    '''Main search url. See Backend for more details'''
    return dumps(backend.get_products(request.args))


@app.route('/products/available/', methods=['GET'])
def get_available_products():
    '''
    Search with given arguments,
    but also limit the minimum amount to at least 1.
    '''
    args = MultiDict(request.args)
    args.add('minamount', 1)
    return dumps(backend.get_products(args))


@app.route('/products/categories/', methods=['GET'])
def get_categories():
    '''Return the categories available in the databse'''
    return dumps(backend.get_categories())


@app.route('/products/categories/<category>', methods=['GET'])
def get_by_category(category):
    '''
    Search with given arguments,
    but also limit the search to the given category.
    '''
    args = MultiDict(request.args)
    args.add('category', category)
    return dumps(backend.get_products(args))


@app.route('/restapi/wsdl', methods=['GET'])
def serve_wsdl():
    '''Return the WSDL description of the service.'''
    with app.open_resource('wsdl.xml', 'r') as wsdl:
        return make_response(wsdl.read())


@app.route('/restapi/xsd', methods=['GET'])
def serve_xsd():
    '''Return the XML-schema used by the service'''
    with app.open_resource('restservice.xsd', 'r') as xsd:
        return make_response(xsd.read())


@app.route('/restapi/schema', methods=['GET'])
def serve_schema():
    '''Return the JSON-schema describing the functions of the service.'''
    with app.open_resource('restservice.schema.json', 'r') as schema:
        return make_response(schema.read())

if __name__ == "__main__":
    app.run()
