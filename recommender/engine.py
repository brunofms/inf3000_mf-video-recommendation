# encoding: utf8

import sys
import time
import numpy
import random

class MFEngine:
	
	# PATH = '../data/globocom/bbb/'
	# TRAIN_FILE = 'bbb.mar.100000.base'
	
	def __init__(self, bias):
		
		self._bias = bias
		
		# train and test data
		self._train = {}
		self._test = {}
		
		# users and videos index
		self._user_index = {}
		self._video_index = {}
		
		# viewing data (sparse matrix)
		self._R = []
		
		# feature matrices
		self._W = []
		self._Q = []
	
	
	"""
	Carrega o dataset da globo.com (bbb)
	"""
	def load_globocom(self, path='../data/globocom/auto_esporte/auto_esporte.may'):
	# def load_globocom(self, path='../data/globocom/bbb/bbb.mar.1000000'):
		
		# load train data
		train={}
		for line in open(path + '.base'):
			(user_utma, video_id, ts_bin) = line.strip().split('\t')
			train.setdefault( user_utma, {} )
			train[user_utma][video_id] = ts_bin
		
		# load test data
		test={}
		for line in open( path + '.test' ):
			(user_utma, video_id, ts_bin) = line.strip().split('\t')
			test.setdefault( user_utma, {} )
			test[user_utma][video_id] = ts_bin
		
		# Load video data
		videos={}
		for line in open( path + '.item' ):
			video_data = line.strip().split('|')
			videos.setdefault( video_data[0], {} )
			videos[video_data[0]] = {"title":video_data[1],"release_date":video_data[2]}

		self._train = train
		self._test = test
		self._videos = videos
	
	
	"""
	Carrega o dataset da movielens
	"""
	def load_movielens( self, path='../data/movielens/100k' ):

		# Load training data
		train={}
		for line in open( path + '/ua.base' ):
			(user, movieid, rating, ts) = line.strip().split('\t')
			# (user, movieid, rating, ts) = line.strip().split('::')
			train.setdefault( user, {} )
			train[user][movieid] = float( rating )

		# Load training data
		test={}
		for line in open( path + '/ua.test' ):
			(user, movieid, rating, ts) = line.strip().split('\t')
			# (user, movieid, rating, ts) = line.strip().split('::')
			test.setdefault( user, {} )
			test[user][movieid] = float( rating )

		# Load users data
		users={}
		for line in open( path + '/u.user' ):
			(user_id, age, gender, occupation, zip_code) = line.strip().split('|')
			users.setdefault( user_id, {} )
			users[user_id] = {"age":age,"gender":gender,"occupation":occupation,"zip_code":zip_code}

		# Load movie data
		movies={}
		for line in open( path + '/u.item' ):
			movie_data = line.strip().split('|')
			movies.setdefault( movie_data[0], {} )
			movies[movie_data[0]] = {"title":movie_data[1],"release_date":movie_data[2]}

		self._train = train
		self._test = test
		self._videos = movies
	
	
	"""
	Mapeia videos e usuarios em arrays indexados
	"""
	def build_indexes(self):
		
		data = self._train

		user_index = {}
		video_index = {}
		bin_index = {}

		i = 0
		j = 0
		k = 0
		nr = 0
		for user_ratings in data.items():

			user_id = user_ratings[0]
			user_index[user_id] = i
			i = i + 1

			ratings = user_ratings[1]
			nr = nr + len(ratings)

			for video_id in ratings.keys():
				if not video_index.has_key(video_id):
					video_index[video_id] = j
					j = j + 1
				if not bin_index.has_key(ratings[video_id]):
					bin_index[ratings[video_id]] = k
					k = k + 1

		nu = len(user_index)
		nv = len(video_index)
		nb = len(bin_index)
		
		print "%d users" % nu
		print "%d videos" % nv
		print "%d bins" % nb
		print "%d videos viewed\n" % nr
		sys.stdout.flush()
		
		self._user_index=user_index
		self._video_index=video_index
		self._bin_index=bin_index

	"""
	
	"""
	def init_data_matrix(self):
		
		user_index = self._user_index
		video_index = self._video_index
		bin_index = self._bin_index
		data = self._train

		dimension = (len(user_index), len(video_index))
		md_dimension = (len(video_index), len(bin_index))
		R = numpy.zeros(dimension)
		RB = numpy.zeros(dimension)
		MD = numpy.zeros(md_dimension)

		for user_views in data.items():
			user = user_views[0]
			views = user_views[1]
			bin 
			for video_id in views.keys():
				R[user_index[user]][video_index[video_id]] = 1.0 # 1.0
				RB[user_index[user]][video_index[video_id]] = float( bin_index[data[user][video_id]] ) # bin
				MD[video_index[video_id]][bin_index[data[user][video_id]]] = 1.0

		self._R = R
		self._RB = RB
		self._MD = MD

	"""
	Train features using Weighted Matrix Factorization
	"""
	def learn_factors_wmf(self, n_features, max_e=50, lrate=0.001, regularization=0.02):
		
		R = self._R

		n_users = numpy.shape(R)[0]
		n_movies = numpy.shape(R)[1]
		
		# init variables
		rmse = 1000

		# initialize the weight and feature matrices with random values
		W = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for f in range(n_features)] for u in range(n_users)])
		Q = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for m in range(n_movies)] for f in range(n_features)])
		
		# initialize bias
		u_bias = [0.0 for u in range(n_users)]
		v_bias = [0.0 for v in range(n_movies)]

		for step in xrange(max_e):
			
			print "\t\t%s - Epoch %d of %d" % (time.strftime('%X'), step+1, max_e)
			
			sq = 0
			n = 0
			rmse_last = rmse
			
			for i in xrange(n_users):
				for j in xrange(n_movies):
					if R[i][j] > 0:
						
						rated = R[i][j]
						predicted = 0.0 + numpy.dot(W[i,:],Q[:,j]) #+ u_bias[i] + v_bias[j] + numpy.dot(W[i,:],Q[:,j])
						eij = rated - predicted
						
						if i==0 and (j==0 or j==1):
							print 'i:%d, j:%d :: rated = %f, predicted = %f (w= %f, q= %f), err = %f' % (i, j, rated, predicted, W[i,0], Q[0,j], err)
							sys.stdout.flush()
						
						# update biases
						u_bias[i] = u_bias[i] + 0.0009 * (eij - 0.022 * u_bias[i])
						v_bias[j] = v_bias[j] + 0.0009 * (eij - 0.022 * v_bias[j])
						
						sq = sq + (eij**2)
						n = n + 1
						
						for f in xrange(n_features):
							W[i,f] = W[i,f] + lrate * ( 2 * eij * Q[f,j] - regularization * W[i,f] )
							Q[f,j] = Q[f,j] + lrate * ( 2 * eij * W[i,f] - regularization * Q[f,j] )
			
			rmse = numpy.sqrt(sq/n)

			print "\t\t\trmse=%f" % rmse
			sys.stdout.flush()
			
			if rmse_last - rmse < 0.0001:
				print "rmse_last - rmse < 0.0001: BREAK!!!"
				break

		self._u_bias = u_bias
		self._v_bias = v_bias
		self._W = W
		self._Q = Q
	
	
	"""
	Train features using Simon Funk's SVD
	"""
	def learn_factors_sfunk (self, n_features, min_e=30, max_e=50, lrate=0.001, regularization=0.02):
		
		R = self._R
		RB = self._RB
		MD = self._MD

		# init contants
		min_improvement = 0.0001
		learn_rate = lrate
		min_epochs = min_e
		max_epochs = max_e
		self._n_features = n_features

		n_users = numpy.shape(R)[0]
		n_videos = numpy.shape(R)[1]
		
		n_bins = numpy.shape(MD)[1]

		# initialize the weight and feature matrices with random values :: viewing
		W = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for f in range(n_features)] for u in range(n_users)])
		Q = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for m in range(n_videos)] for f in range(n_features)])

		# initialize the weight and feature matrices with random values :: viewing data
		MF = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for k in range(n_features)] for u in range(n_videos)])
		DF = numpy.matrix([[numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for k in range(n_bins)] for u in range(n_features)])
		
		# initialize bias
		u_bias = [numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for u in range(n_users)]
		v_bias = [numpy.sqrt(0.5/max_e) + random.uniform(-0.005, +0.005) for v in range(n_videos)]

		# initialize features cache
		dimension = (n_users, n_videos)
		md_dimension = (n_videos, n_bins)
		cache_R = numpy.zeros(dimension)
		cache_MD = numpy.zeros(md_dimension)

		# init variables
		rmse = 1000	
		rmse_last = 1000


		for f in range(n_features):

			# keep looping until you have passed a minimum number 
	        # of epochs or have stopped making significant progress
			e = 0
			while (e < min_epochs or rmse <= rmse_last - min_improvement) and e < max_epochs:

				print "\t\t%s - Calculating feature %d of %d - Epoch %d of %d" % (time.strftime('%X'), f+1, n_features, e+1, max_epochs)
				sys.stdout.flush()

				n = 0
				sq = 0
				rmse_last = rmse

				for i in xrange(n_users):
					for j in xrange(n_videos):
						if R[i][j] > 0:

							# predict rating and calc error
							rated = R[i][j]
							bin = RB[i][j]
							t_v_bias = numpy.dot(MF[j,:], DF[:,bin]) # TODO: cache features
							predicted = self._predict_rating_for_feature(i, j, f, W, Q, cache_R, 1.0) \
								+ u_bias[i] \
								+ v_bias[j] 
								# + self._predict_temporal_effect_for_feature(j, bin, f, MF, DF, cache_MD, 1.0)
								
							err = rated - predicted

							if i==0 and (j==0 or j==1):
								print 'i:%d, j:%d :: rated = %f, predicted = %f (w= %f, q= %f, u_bias= %f, v_bias= %f, t_v_bias= %f), err = %f' % (i, j, rated, predicted, W[i,f], Q[f,j], u_bias[i], v_bias[j], t_v_bias, err)
								sys.stdout.flush()

							sq = sq + (err**2)
							n = n + 1

							# update biases
							u_bias[i] = u_bias[i] + 0.0009 * (err - 0.022 * u_bias[i])
							v_bias[j] = v_bias[j] + 0.0009 * (err - 0.022 * v_bias[j])
							
							# # update temporal biases
							# for k in range(3):
							# for b in xrange(n_bins):
							# 
							# 	# cache off old feature movie-date values
							# 	mf = MF[j,f]
							# 	df = DF[f,b]
							# 
							# 	# cross-train the movie-date features
							# 	MF[j,f] = mf + 0.00004 * (err - 0.022 * df)
							# 	DF[f,b] = df + 0.00004 * (err - 0.022 * mf)

							# cache off old feature values
							cf = W[i,f]
							mf = Q[f,j]

							# cross-train the features
							W[i,f] = W[i,f] + learn_rate * (2 * err * mf - regularization * cf)
							Q[f,j] = Q[f,j] + learn_rate * (2 * err * cf - regularization * mf)

				rmse = numpy.sqrt(sq/n)

				print "\t\t\trmse=%f" % rmse
				sys.stdout.flush()
				
				e = e + 1
			
			# cache off old predictions
			for i in xrange(n_users):
				for j in xrange(n_videos):
					if R[i][j] > 0:
						cache_R[i,j] = self._predict_rating_for_feature(i, j, f, W, Q, cache_R, 0.0)
			
			# for j in xrange(n_videos):
			# 	for b in xrange(n_bins):
			# 		if MD[j][b] > 0:
			# 			cache_MD[j][b] = self._predict_temporal_effect_for_feature(j, b, f, MF, DF, cache_MD, 0.0)

		self._u_bias = u_bias
		self._v_bias = v_bias
		self._W = W
		self._Q = Q
		self._MF = MF
		self._DF = DF
	
	"""
	Test dataset
	"""
	def process_test (self):

		for data in [self._train, self._test]:
			
			i=0
			err = 0.0
			
			for video_views in data.items():
				user = video_views[0]
				views = video_views[1]
				for video_id in views.keys():
					if self._user_index.has_key(user) and self._video_index.has_key(video_id):
						predicted = self._predict_rating( self._user_index[user], self._video_index[video_id], self._bin_index[data[user][video_id]] )
						# rated = float( data[user][video_id] )
						rated = 1.0
						err = err + (rated - predicted)**2
						i = i + 1
						if i % 500 == 0:
							print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)

			mse = err/i
			rmse = numpy.sqrt(mse)
			
			# print "\nRMSE: %s (K=%d, e=%d, lrate=%s, reg=%f)" % (rmse, self._K, self._e, self._lrate, self._reg)
			print "\nRMSE: %s" % rmse
			sys.stdout.flush()
	

	"""
	Rank user and video features
	"""
	def show_video_features(self, out='features.txt'):
		outfile = file(out, 'w')
		wc,pc = numpy.shape(self._W)

		# Loop over all the features
		for f in range(pc):
		
			outfile.write('Feature '+str(f)+':\n')
		
			ulist=[]
			# Create a list of users and their weights
			for u in range(wc):
				ulist.append((self._W[u,f],self._find_key(self._user_index,u)))
			# Reverse sort the users list
			ulist.sort()
			ulist.reverse()
		
			# Print the first six elements
			n=[u[1] for u in ulist[0:5]]
			outfile.write(str(n)+'\n')
		
			#Create a list of movies for this feature
			mlist=[]
			for m in range(len(self._video_index)):
				# Add the movie with its weight
				mlist.append((self._Q[f,m],self._videos[self._find_key(self._video_index,m)]['title']))
		
			# Reverse sort the list
			mlist.sort()
			mlist.reverse()
		
			# Show the top 5 movies
			for m in mlist[0:5]:
				outfile.write(str(m).decode('string_escape')+'\n')
			outfile.write('\n')
			
			# Show the bottom 5 movies
			mlist.reverse()
			for m in mlist[0:5]:
				outfile.write(str(m).decode('string_escape')+'\n')
			outfile.write('\n')

		outfile.close()
	
	"""
	Add contribution of each feature to the prediction
	"""
	def _predict_rating_for_feature (self, i, j, f, W, Q, cache_R, trailing):

		if cache_R[i,j] > 0:
			result = cache_R[i,j]
		else:
			# TODO: mean + bias(user) + bias(item)
			result = 0.0 # global bias - PseudoAvg

		# add contribution of current feature
		result = result + W[i,f] * Q[f,j]
		
		# add up trailing defaults values
		if trailing > 0:
			result = result + (self._n_features - f - 1) * pow (0.1, 2)

		return result

	"""
	Add contribution of each feature to the temporal effect biases
	"""
	def _predict_temporal_effect_for_feature (self, j, b, f, MF, DF, cache_MD, trailing):

		if cache_MD[j,b] > 0:
			result = cache_MD[j,b]
		else:
			result = 0.0 # global bias - PseudoAvg

		# add contribution of current feature
		result = result + MF[j,f] * DF[f,b]

		# add up trailing defaults values
		if trailing > 0:
			result = result + (self._n_features - f - 1) * pow (0.1, 2)

		return result

	"""
	Predict rating
	"""
	def _predict_rating (self, i, j, bin):

		result = 0.0 # global bias - PseudoAvg

		# add contribution of features
		result = result + numpy.dot(self._W[i,:], self._Q[:,j])
		
		# add contribution of user and video biases
		result = result + self._u_bias[i] + self._v_bias[j]
		
		# add contribution of temporal video biases
		# result = result + numpy.dot(self._MF[j,:], self._DF[:,bin])

		return result
	
	"""
	"""
	def _find_key(self, dic, val):
		
	    # return the key of dictionary dic given the value
	    return [k for k, v in dic.iteritems() if v == val][0]
	


if __name__ == "__main__":
	
	engine = MFEngine(True)
	
	# TODO: dao
	engine.load_globocom()
	# engine.load_movielens()
	engine.build_indexes()
	engine.init_data_matrix()
	
	engine.learn_factors_sfunk(5)
	# engine.learn_factors_wmf(10,200)
	engine.process_test()
	
	engine.show_video_features()