from pymongo import MongoClient
from werkzeug.datastructures import ImmutableMultiDict
import logging as log

MONGO_URL = "mongodb://heroku:M0ng0_p455w0rd5_4_411@troup.mongohq.com:10002/restservice"

ARG_LIMIT = 'limit'
ARG_FIELD = 'field'
ARG_NOT_FIELD = 'notfield'
ARG_CATEGORY = 'category'
ARG_NOT_CATEGORY = 'notcategory'

ACCEPTED_ARGS = [
    ARG_LIMIT,
    ARG_FIELD,
    ARG_NOT_FIELD,
    ARG_CATEGORY,
    ARG_NOT_CATEGORY
]


class Backend():
    def __init__(self, db_url=MONGO_URL):
        self.connection = MongoClient(db_url)
        self.db = self.connection.restservice

    def get_root(self):
        return self.db.products.find_one()

    def get_products(self, raw_args):
        args = self.parse_args(raw_args)

    def parse_args(self, raw_args):
        parsed_args = {}
        for argument in ACCEPTED_ARGS:
            value = raw_args.getlist(argument)
            print value
            if not value:
                # No matches
                continue
            if argument is ARG_LIMIT:
                # Limit search results by first given argument
                parsed_args[argument] = value[0]
            elif argument is ARG_FIELD or argument is ARG_NOT_FIELD:
                print 'here'
                if 'fields' not in parsed_args:
                    parsed_args['fields'] = {'_id': False}
                if argument is ARG_FIELD:
                    include = True
                else:
                    include = False
                for field in value:
                    parsed_args['fields'][field] = include
        print parsed_args
        return parsed_args
