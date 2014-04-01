from pymongo import MongoClient, ASCENDING, DESCENDING
from werkzeug.datastructures import ImmutableMultiDict
import logging as log
from pprint import pprint

#MONGO_URL = "mongodb://heroku:M0ng0_p455w0rd5_4_411@troup.mongohq.com:10002/restservice"

ARG_LIMIT = 'limit'
ARG_NOT_FIELD = 'notfield'
ARG_CATEGORY = 'category'
ARG_NOT_CATEGORY = 'notcategory'
ARG_SUBCATEGORY = 'subcategory'
ARG_NOT_SUBCATEGORY = 'notsubcategory'
ARG_MAX_PRICE = 'maxprice'
ARG_SORT_UP = 'sort'
ARG_SORT_DOWN = 'dsort'
ARG_AMOUNT_MIN = 'minamount'

CATEGORIES = [
    ARG_CATEGORY,
    ARG_NOT_CATEGORY,
    ARG_SUBCATEGORY,
    ARG_NOT_SUBCATEGORY
]

ACCEPTED_ARGS = [
    ARG_LIMIT,
    ARG_NOT_FIELD,
    ARG_CATEGORY,
    ARG_NOT_CATEGORY,
    ARG_SUBCATEGORY,
    ARG_NOT_SUBCATEGORY,
    ARG_MAX_PRICE,
    ARG_SORT_UP,
    ARG_SORT_DOWN,
    ARG_AMOUNT_MIN
]

FORBIDDEN_FIELDS = [
    '_id'
]

BASE_ARGS = {
    'fields': {
        '_id': False
    }
}


class Backend():
    def __init__(self, db_url=MONGO_URL):
        self.connection = MongoClient(db_url)
        self.db = self.connection.restservice

    def get_root(self):
        return self.db.products.find_one()

    def get_products(self, raw_args):
        args = self.parse_args(raw_args)
        return self.search(self.db.products, args)

    def get_categories(self):
        return self.db.products.find().distinct('category')

    def search(self, collection, args):
        result = collection.find(**args)
        return list(result)

    def parse_args(self, raw_args=None):
        parsed_args = BASE_ARGS.copy()

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
            try:
                # Make lowercase
                value = [string.lower() for string in value]
            except:
                # Not strings
                pass
            if argument is ARG_LIMIT:
                # Limit search results by last given argument
                try:
                    val = int(value[-1])
                    if val < 0:
                        raise Exception('Less than 0')
                except:
                    # NaN or negative
                    continue
                parsed_args[argument] = val
            elif argument is ARG_NOT_FIELD:
                # exclude specified fields
                for field in value:
                    parsed_args['fields'][field.lower()] = False
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
                try:
                    val = int(value[-1])
                except:
                    # NaN
                    continue
                parsed_args['spec']['price']['$lt'] = val
            elif argument in [ARG_SORT_UP, ARG_SORT_DOWN]:
                # Sort by given fieldnames
                if argument is ARG_SORT_UP:
                    direction = ASCENDING
                else:
                    direction = DESCENDING
                if 'sort' not in parsed_args:
                    parsed_args['sort'] = []
                for fieldname in value:
                    parsed_args['sort'].append((fieldname, direction))
            elif argument is ARG_AMOUNT_MIN:
                try:
                    val = int(value[-1])
                except:
                    # NaN
                    continue
                check_parsed('amount')
                parsed_args['spec']['amount']['$gte'] = val
            else:
                # Unsupported parameter
                continue
        return parsed_args
