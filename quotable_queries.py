import pymongo
from pprint import pprint


def mongo_conn(db, collection):
    conn = pymongo.MongoClient('localhost', 27017)
    db_conn = conn[db]
    coll_conn = db_conn[collection]
    print coll_conn
    return coll_conn


def list_and_count(coll_field, coll_conn, display_limit=10):
    a = list(coll_conn.aggregate(
        [{
             "$group":
             {"_id": "$" + coll_field, "count":
              {
                  "$sum": 1
              }

              }
             }, {"$sort": {"count": -1}}, {"$limit": display_limit}
         ]))
    for i, enum in enumerate(a):
        print enum

my_conn = mongo_conn('imdb', 'imdb_top250')
# list_and_count('author', my_conn, 20)
##########################################################
# def list_imdb(coll_conn):
#     curr_conn = coll_conn
#     print curr_conn
#     all_titles,all_ids,all_nquotes = [],[],[]
#     all_docs = coll_conn.find()
#     for doc in all_docs:
# pprint(doc)
#         doc["len_quotes"] = len(doc['quotes'])
#         title,imdb_id,n_quotes = doc['name'], doc['imdb_id'], doc['len_quotes']
#         all_titles.append(title)
#         all_ids.append(imdb_id)
#         all_nquotes.append(n_quotes)
#     return (zip(all_ids,all_titles,all_nquotes))


# my_list = list_imdb(my_conn)
# print len(my_list)
# print my_list[0]

# sort a list of tuples based on the third value
# q_desc = sorted(my_list, key = lambda tup:tup[2], reverse = True)
# print q_desc
# print my_dict.items()[1]

def title_and_count(coll_conn):
    curr_conn = coll_conn
    all_titles = list(curr_conn.aggregate([
                      {"$unwind": "$quotes"},
                       {"$group":
                         {"_id":{
                                "name": "$name"
                                ,"imdb_id": "$imdb_id"
                                ,"rating": "$rating"
                                ,"desc": "$description"
                                ,"director": "$director"
                                ,"img_src": "$img_src"
                         }
                         ,"count": {"$sum": 1}
                         }
                        },
                        {"$sort":{"count": -1}
                        }
                        ,{"$limit":3}
                      ])
    )

    # print len(all_titles)
    # pprint(all_titles)
    return all_titles

all_titles =  title_and_count(my_conn)
print len(all_titles)
print all_titles[0]

 #########################################################
def find_by_title_id(title_id, coll_conn):
    curr_conn=coll_conn
    quotes_by_id=curr_conn.find_one({"imdb_id": title_id})
    return quotes_by_id


#########################################################

curr_movie = find_by_title_id('tt0266543', my_conn)

# print curr_movie['name']
# for i,enum in enumerate(curr_movie['quotes']):
#     print str(i+1) + enum.encode('utf-8',errors='ignore') + '\n\t' + 10 * '*'
