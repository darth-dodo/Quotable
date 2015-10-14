import pymongo

def mongo_conn(db,collname):
	conn = pymongo.MongoClient('localhost', 27017)
	database_conn = conn[db]
	coll_conn = database_conn[collname]
	return coll_conn

def get_top10(db,collname):
	coll = mongo_conn(db, collname)
	print 'collection->',coll
	cursor = coll.find({},{'quote':1,'_id':0,'likes':1}).sort("likes",pymongo.DESCENDING).limit(10)
	# cursor = coll.count()
	print cursor
	data = []
	for value in cursor:
		print value,'\n'
		data.append(value)
	return data
# output = db_coll('goodreads')
# print 'data output->',output
output = db_coll('goodreadsDB','popular')
print output

