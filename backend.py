from pymongo import Connection

MONGO_URL = "mongodb://heroku:M0ng0_p455w0rd5_4_411@troup.mongohq.com:10002/restservice"


class Backend():
    def __init__(self, db_url=MONGO_URL):
        self.connection = Connection(db_url)
        self.db = self.connection.restservice
        print self.db

    def get_root(self):
        print self.db.products.find_one()
        return self.db.products.find_one()
