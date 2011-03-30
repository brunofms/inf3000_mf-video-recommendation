import numpy

#
# carrega o dataset da movielens
#
def load_movielens( path='../data/movielens/100k' ):
	
	# Load training data
	train={}
	for line in open( path + '/ua.base' ):
		(user, movieid, rating, ts) = line.strip().split('\t')
		train.setdefault( user, {} )
		train[user][movieid] = float( rating )
	
	# Load training data
	test={}
	for line in open( path + '/ua.test' ):
		(user, movieid, rating, ts) = line.strip().split('\t')
		test.setdefault( user, {} )
		test[user][movieid] = float( rating )
	
	return train, test

#
#
#
def build_indexes(data):
	
	user_index = {}
	movie_index = {}
	
	i = 0
	j = 0
	nr = 0
	for user_ratings in data.items():
		
		user_id = user_ratings[0]
		user_index[user_id] = i
		i = i + 1
		
		ratings = user_ratings[1]
		nr = nr + len(ratings)
		
		for movie_id in ratings.keys():
			if not movie_index.has_key(movie_id):
				movie_index[movie_id] = j
				j = j + 1

	nu = len(user_index)
	nm = len(movie_index)
	print "%d users" % nu
	print "%d movies" % nm
	print "%d movies rated\n" % nr
	
	return user_index, movie_index

#
#
#
def format_data(user_index, movie_index, data, K):

	dimension = (len(user_index), len(movie_index))
	R = numpy.zeros(dimension)

	for user_ratings in data.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			R[user_index[user]][movie_index[movie_id]] = float( data[user][movie_id] ) # 1.0

	N = len(R)
	M = len(R[0])

	P = numpy.random.rand(N,K)
	Q = numpy.random.rand(M,K)
	
	return R, P, Q