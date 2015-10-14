import pymongo
import random
import time
import pynotify

'''
    Extract data from goodreads MongoDB collections
    (hit the db once to extract 100 random quotes)
    and display them as notifications using pynotify periodically.
    Script set up in system cron.
'''


class goodreadNotif():

    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['goodreadsDB']

    def count(self, collection):
        db = self.db
        collection = db[collection]
        count = collection.count()
        return count

    def randomizer(self, coll):
        self.collection = self.db[coll]
        coll_count = self.count(coll)
        all_quotes = []
        all_authors = []
        # skips = [random.randint(1, coll_count) for b in xrange(0, 99)]
        # check for max limit of coll count > range
        skips = [random.randint(1, coll_count) for b in xrange(0, 599)]
        print len(skips)
        print skips [:3]

        for i, enum in enumerate(skips):
            # print skips[i]
            curr_quote = self.collection.find().skip(i).limit(1)
            for quote in curr_quote:
                all_quotes.append(quote["quote"])
                all_authors.append(quote["author"])

        '''building the notif data list and looping for 48 elements (2/hr)'''
        notif_data = zip(all_quotes, all_authors)
        print 'Random data length', len(notif_data)

        # for i in xrange(0, 48):
        for i in xrange(0, 500):
            '''picking random quote from notif_data'''

            a = random.randint(0, len(notif_data) - 1)
            notif_quote = str(notif_data[a][0]),
            notif_author = str(notif_data[a][1])

            '''display quotes every 30 mins'''

            notif = myPyNotif()
            notif.pynotify_quotable(quote=notif_quote, author=notif_author)

            '''deleting quote so it doesn't repeat'''
            del notif_data[a]
            # time.sleep(60 * 30)
            time.sleep(60 * 5)


class myPyNotif():

    def __init__(self):
        pass

    def pynotify_quotable(self, quote, author):
        pynotify.init("Quotable")
        n_quote = ''.join(quote)
        n_author = '\n\t ~ ' + ''.join(author)
        print n_quote, '\n', n_author, '\n\n'

        n = pynotify.Notification(n_quote, n_author)
        n.show()

if __name__ == '__main__':

    new_sesh = goodreadNotif()
    new_sesh.randomizer('popular')
