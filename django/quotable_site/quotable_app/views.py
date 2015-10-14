from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import collections
# Create your views here.


def hello(request):
    return render(request, 'hello.html')


def mongo_conn(db, collname):
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
    db_coll = mongo_conn('Quotable', 'modes')
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
    # print all_modes
    return render(request, 'mode.html', {'listed_modes': all_modes})


def imdb_worker(request, offset):
    print (request.path)

    path_elems = (request.path).encode('utf-8', errors='ignore').split('/')
    print path_elems

    collection_name = path_elems[3].replace('-', '_')
    print 'MEDIA >> ', offset
    print 'COLL >> ', collection_name


    return render(request, 'top10.html')
