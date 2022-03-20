from pymongo import MongoClient

class MongoDBConnection():
    '''MongoDB Connection'''

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        '''
        sets up a MongoDB connection
        '''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        closes the MongoDB connection
        '''
        self.connection.close()


def print_mdb_collection(collection_name):
    '''
    prints out a collection
    '''
    for doc in collection_name.find():
        print(doc)


def main():
    '''
    sets up MongoDB connection object
    '''
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.social_network

        return db


def drop_data(collection_1, collection_2):
    '''
    clears the data from the MongoDB collections
    '''
    choice = input('Drop data? (Y/N) ')
    if choice.upper() == 'Y':
        collection_1.database.drop()
        collection_2.database.drop()
