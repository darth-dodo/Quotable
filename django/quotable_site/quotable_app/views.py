from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import collections
import random
# Create your views here.


def hello(request):
    return render(request, 'hello.html')


def mongo_conn(collname, db='Quotable'):
    conn = pymongo.MongoClient('localhost', 27017)
    database_conn = conn[db]
    coll_conn = database_conn[collname]
    return coll_conn


def convert(data):

    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def display_modes(sitename):
    db_coll = mongo_conn(collname='modes')
    print db_coll

    all_modes = []
    all_modes_raw = db_coll.find({"site": sitename})
    # print all_modes_raw

    for raw_mode in all_modes_raw:
        # print 'raw_mode >\t', raw_mode
        clean_mode = convert(raw_mode)
        # print 'clean_mode >\t', clean_mode
        all_modes.append(clean_mode)

    return all_modes


def modes(request, offset):
    print 'welcome to modes! >> ', offset
    all_modes = display_modes(offset)
    print all_modes
    return render(request, 'mode.html', {'listed_modes': all_modes})


def imdb_worker_para(request, media, mode):
    print (request.path)
    mode_name = mode.replace('-', '_')
    print 'MEDIA >> ', media
    print 'COLL >> ', mode_name

    if mode_name in ('top_250tv', 'top_250'):

        grid_data = []
        grid_data = get_list(coll_name=mode_name)
        return render(request, 'grid.html', {'grid_data': grid_data})

    elif (mode_name == 'list_all'):

        all_colls_for_media = get_all_coll_names(media_type=media)
        all_titles = []

        for i in all_colls_for_media:
            grid_data = get_list(coll_name=i)
            all_titles.extend(grid_data)

        return render(request, 'grid.html', {'grid_data': all_titles})

    elif (mode_name == 'randomizer'):

        all_colls_for_media = get_all_coll_names(media_type=media)
        print all_colls_for_media
        rand_coll = random.choice(all_colls_for_media)
        print rand_coll
        random_quotes = randomizer(coll_name=rand_coll)

        return render(request, 'randomizer.html', {'random_quotes': random_quotes})
    else:
        pass

    return render(request, 'top10.html')


def randomizer(coll_name):

    curr_coll = mongo_conn(coll_name)
    count = curr_coll.count()
    if (count != 0):
        random_doc_skip = random.randint(1, count - 1)
        print random_doc_skip
        cursor = curr_coll.find({}).skip(random_doc_skip).limit(1)
        for i in cursor:
            if (len(i['quotes']) != 0):
                random_quote = {
                    "quote": random.choice(i['quotes']), "title": i['name']
                }
            print random_quote
        return random_quote


def get_all_coll_names(media_type):
    coll_conn = mongo_conn('media_desc')
    all_colls = coll_conn.find_one({'media_type': media_type})
    return all_colls['media_collections']


def get_list(coll_name):
    curr_coll = mongo_conn(collname=coll_name)
    print 'get_grid coll conn > ', curr_coll
    cursor = (curr_coll.find({},
                             {'name': 1, '_id': 1, 'rating': 1,
                              'img_src': 1, 'imdb_id': 1
                              }).sort("rating", pymongo.DESCENDING))
    grid_view = []
    for i in cursor:
        grid_view.append(i)

    return grid_view[:-1]


def imdb_get_quotes(coll_name, imdb_id):
    coll_conn = mongo_conn(collname=coll_name)
    print coll_conn
    all_q = []
    all_q = coll_conn.find_one({"imdb_id": imdb_id})
    return all_q


def get_title(request, media, mode, title):
    print 'request>> ', request.path
    print 'media >> ', media
    print 'mode >> ', mode
    print 'title >> ', title
    collection_name = mode.replace('-', '_')
    print 'collection_name >> ', collection_name

    all_quotes = imdb_get_quotes(coll_name=collection_name, imdb_id=title)

    return render(request, 'imdb_quotes.html', {'all_quotes': all_quotes})
