from pymongo import MongoClient

class MongoDBModel(object):

    def __init__(self, database, MONGO_URI):
        self.client = MongoClient(MONGO_URI)
        self.database = database
    
    def insert(self, data, collection):
        db = self.client[self.database]
        return db[collection].insert_one(data)
    
    def getMediaID(self, collection):
        db = self.client[self.database]
        query = {'id':1, '_id':0}
        data = db[collection].find({}, query)

    def getIgPermalink(self, collection):
        db = self.client[self.database]
        query = {'permalink':1, '_id':0}
        data = db[collection].find({}, query)
        return data
    