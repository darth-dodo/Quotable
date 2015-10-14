    # TODO
# fix the back to home issue
# add custom filtering
# add partial text search
# add argparse
# integrate spiders

import pymongo
from random import randint
import sys


class Goodreads():

    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['goodreadsDB']

    def count(self, collection):
        db = self.db
        collection = db[collection]
        count = collection.count()
        return count

        # print collection
        # pprint(count)
    def homePage(self):

        home = int(raw_input(
            'Select mode [enter number]\n\t1. Popular\n\t2. Authors\n\t3. List available authors\n\t4. Exit the program\n\t> '))
        return home

    def emptyColl(self, miss_col, author=None):

        print 'Collection', miss_col, 'is Empty!'
        choice = raw_input(
            'Wanna populate all the quotes from Goodreads?\ny or n\n>')
        if (choice.lower() == 'y'):
            print 'Spider call'
            pass
        else:
            print 'Rerouting to homepage'
            self.homePage()

    def gen_collection_flow(self, collName):
        print '\n\t> What would you like to do? '
        option = int(raw_input(
            '\n\t1. Top 10 quotes\n\t2. Top 10 tags in quotes \n\t3. Random Quotes\n\t4. Based on tags\n\t5. Specific author\n\t6. Return to homepage\n\t7. Exit the program\n\t> '))

        if (option == 1):
            self.result_set_fetch(coll=collName, sort_value="likes")
            already_skipped = 0
            option = raw_input('Fetch more quotes?\ny or n\n\t> ')

            # write a skip method

            if (option.lower() == 'y'):
                skip_amt = int(raw_input("How many?\nPlease enter number\n\t"))
                skip_amt += already_skipped
                self.result_set_fetch(
                    coll=collName, sort_value="likes", skip_value=skip_amt)
                already_skipped = skip_amt

        elif(option == 2):
            self.top_10_tags(coll=collName)

        elif (option == 3):
            self.randomizer(coll=collName)

        elif(option == 4):
            print 'Tag based filtering under development'
            self.gen_collection_flow(collName)

        elif (option == 5):
            print 'Author Specific filtering under development'
            self.gen_collection_flow(collName)

        elif (option == 6):
            # crashes the system. Looping incorrect. Sync with the object
            print 'Rerouting to homepage'
            self.homePage()

        elif (option == 7):
            print '\n\t\t\t\t\t\tThanks for using Quotable!\n'
            sys.exit(1)

        else:
            print 'Incorrect option.\nPlease try again...'
            self.gen_collection_flow(collName)

    def top_10_tags(self, coll):
        self.collection = self.db[coll]
        tag_counts = self.collection.aggregate([{"$unwind": "$tags"},
                                                {"$group": {
                                                    "_id": "$tags", "count": {"$sum": 1}}},
                                                {"$sort": {"count": -1}
                                                 }, {"$limit": 10}
                                                ])
        for tag in tag_counts:
            print 'Tag: ', tag["_id"], '\n', 'Occurances: ', tag["count"], '\n\n'
        self.gen_collection_flow(coll)

    def result_set_fetch(self, coll, filters=None, sort_value=None, skip_value=0):
        self.collection = self.db[coll]
        quotes = self.collection.find().sort(
            sort_value, pymongo.DESCENDING).limit(10).skip(skip_value)
        # quotes = [quotes[i].encode('utf-8', ignore='errors') for i,items in enumerate(quotes) ]
        for quote in quotes:

            print '\nQuote: ', quote["quote"].encode('ascii','ignore')
            print quote["quote"].encode('ascii','ignore').split(' ')

            print '\nQuote: ', quote["quote"]
            print quote["quote"].split(' ')

            print '\nLen of Quote', len(quote["quote"])

            print 'Author: ', quote["author"], '\t\t\tLikes: ', quote["likes"], '\n'
        self.gen_collection_flow(coll)

    def randomizer(self, coll):
        self.collection = self.db[coll]
        coll_count = self.count(coll)
        i = 0
        skipping = randint(1, coll_count)
        quotes = self.collection.find().skip(skipping).limit(1)
        for quote in quotes:
            print '\nQuote: ', quote["quote"]
            print 'Author: ', quote["author"], '\t\t\tLikes: ', quote["likes"], '\n'

            print quote["quote"].encode('ascii','ignore')
            print quote["quote"].encode('ascii','ignore').split(' ')

        option = raw_input('\n\tMore random awesomeness?\n\ty or n\n\t> ')
        if (option.lower() == 'y'):
            self.randomizer(coll)
        else:
            self.gen_collection_flow(coll)

    def distinct_authors(self, coll):
        self.collection = self.db[coll]
        authors_contents = self.collection.aggregate([
            {"$group": {"_id": "$author", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 10}
        ])
        print 'Below are the details of a few available authors :\n'
        for author in authors_contents:
            print 'Author ', author["_id"], 'has ', author["count"], 'quotes in the system!'

if __name__ == '__main__':

    sesh = Goodreads()
    print '\n\t\t\t\t\t\tWelcome to Quotable!\n'
    print '\n\t\t\t\t\tContent scraped from www.goodreads.com\n'

    choice = sesh.homePage()

    if (choice == 1):
        # popular
        coll_count = sesh.count('popular')

        if (coll_count == 0):
            # spider calls
            sesh.emptyColl('popular')
        else:
            # mongo activity
            print 'Popular has ', coll_count, ' quotes.\n'
            sesh.gen_collection_flow('popular')

    elif (choice == 2):

        coll_count = sesh.count('authors')
        if (coll_count == 0):
            # spider calls
            sesh.emptyColl('authors')
        else:
            # mongo activity
            print 'Authors has ', coll_count, ' quotes.\n'
            sesh.distinct_authors('authors')
            sesh.gen_collection_flow('authors')

    elif (choice == 3):
        coll_count = sesh.count('all_authors')
        if (coll_count == 0):
            # spider calls
            sesh.emptyColl('authors')
        else:
            # mongo activity
            print 'Under development'

    elif (choice == 4):
        print '\n\t\t\t\t\t\tThanks for using Quotable!\n'
        sys.exit(1)

    else:
        sesh.homePage()
