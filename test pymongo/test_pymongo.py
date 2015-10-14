import pymongo

def conn(db, colln):
    conn = pymongo.MongoClient('localhost', 27017)
    database = conn[db]
    coll = database[colln]
    return coll

def modes():

    collection = conn('imdb', 'modes')
    modes = collection.find({"type":"series"})
    for mode in modes:
        print mode['modes']


modes()
