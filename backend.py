from pymongo import MongoClient
from werkzeug.datastructures import ImmutableMultiDict
import logging as log

MONGO_URL = "mongodb://heroku:M0ng0_p455w0rd5_4_411@troup.mongohq.com:10002/restservice"

ARG_LIMIT = 'limit'
ARG_FIELD = 'field'
ARG_NOT_FIELD = 'notfield'
ARG_CATEGORY = 'category'
ARG_NOT_CATEGORY = 'notcategory'
ARG_SUBCATEGORY = 'subcategory'
ARG_NOT_SUBCATEGORY = 'notsubcategory'
ARG_MAX_PRICE = 'maxprice'

CATEGORIES = [
    ARG_CATEGORY,
    ARG_NOT_CATEGORY,
    ARG_SUBCATEGORY,
    ARG_NOT_SUBCATEGORY
]

ACCEPTED_ARGS = [
    ARG_LIMIT,
    ARG_FIELD,
    ARG_NOT_FIELD,
    ARG_CATEGORY,
    ARG_NOT_CATEGORY,
    ARG_SUBCATEGORY,
    ARG_NOT_SUBCATEGORY,
    ARG_MAX_PRICE
]


class Backend():
    def __init__(self, db_url=MONGO_URL):
        self.connection = MongoClient(db_url)
        self.db = self.connection.restservice

    def get_root(self):
        return self.db.products.find_one()

    def get_products(self, raw_args):
        args = self.parse_args(raw_args)
        return self.search(self.db.products, args)

    def search(self, collection, args):
        result = collection.find(**args)
        return list(result)

    def parse_args(self, raw_args=None):
        parsed_args = {}

        def check_parsed(field):
            if 'spec' not in parsed_args:
                parsed_args['spec'] = {}
            if field not in parsed_args['spec']:
                parsed_args['spec'][field] = {}
        if not raw_args:
            return parsed_args
        for argument in ACCEPTED_ARGS:
            value = raw_args.getlist(argument)
            if not value:
                # No matches
                continue
            if argument is ARG_LIMIT:
                # Limit search results by last given argument
                parsed_args[argument] = value[-1]
            elif argument is ARG_FIELD or argument is ARG_NOT_FIELD:
                if 'fields' not in parsed_args:
                    parsed_args['fields'] = {'_id': False}
                if argument is ARG_FIELD:
                    include = True
                else:
                    include = False
                for field in value:
                    parsed_args['fields'][field] = include
            elif argument in CATEGORIES:
                # Inclusive or exclusive
                if argument in [ARG_CATEGORY, ARG_SUBCATEGORY]:
                    incl = '$in'
                else:
                    incl = '$nin'
                # category- or subcategory-field
                if argument in [ARG_CATEGORY, ARG_NOT_CATEGORY]:
                    field = 'category'
                else:
                    field = 'subcategory'
                check_parsed(field)
                parsed_args['spec'][field][incl] = value
            elif argument is ARG_MAX_PRICE:
                check_parsed('price')
                # Limit to prices lower than last given argument
                parsed_args['spec']['price']['$lt'] = value[-1]
            else:
                # Unsupported parameter
                continue
        return parsed_args
