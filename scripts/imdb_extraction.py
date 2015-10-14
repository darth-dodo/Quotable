import pymongo
from pprint import pprint
from random import randint, choice
import sys
import subprocess


'''
- TODO 0 quotes exception
'''
class imdbQuotable():

    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['imdb']

    def count(self, collection):
        db = self.db
        collection = db[collection]
        count = collection.count()
        return count

    def randomizer(self, coll):
        self.collection = self.db[coll]
        coll_count = self.count(coll)
        i = 0
        skipping = randint(1, coll_count)
        quotes = self.collection.find({"name": "Dragon Ball Z"})
        # quotes = self.collection.find().skip(skipping).limit(1)
        for quote in quotes:
            print 'Title :', quote["name"]
            print 'ID:',quote['imdb_id']

            print quote["name"], " has ", len(quote["quotes"]), " quotes"

            if len(quote["quotes"]) != 0:
                notif_quote = choice(quote["quotes"])
                print 'Quote: \n', notif_quote.strip()
            else:
                print "Seems like " + quote["name"] + " has no quotes! :("
                print "trying another title!\n"
                self.randomizer(coll)
            # subprocess.Popen(['notify-send', notif_quote ])

if __name__ == '__main__':
    imdbWorker = imdbQuotable()
    # coll = 'imdb_top250tv'
    # coll = 'imdb_top250tv'
    coll = 'raj'
    print coll + ' has ', imdbWorker.count(coll), ' titles'
    imdbWorker.randomizer(coll)
