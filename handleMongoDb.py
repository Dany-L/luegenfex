import pymongo

def insertDict(dictName,dbName,collectionName):

    mongoDbClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoDbClient[dbName]
    col = db[collectionName]

    col.insert_one(dictName)

