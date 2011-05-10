from multiprocessing import Process
from dataset import *
from numpy import *
import time, sys

"""
"""
def learn_factors (R, n_features, e=2, lrate=0.0001, regularization=0.02):

	n_users=shape(R)[0]
	n_movies=shape(R)[1]
	
	#Initialize the weight and feature matrices with random values
	W=matrix([[0.1 for f in range(n_features)] for u in range(n_users)])
	Q=matrix([[0.1 for m in range(n_movies)] for f in range(n_features)])
	
	#Initialize features cache
	dimension = (n_users, n_movies)
	cache_R = numpy.zeros(dimension)	
	
	#init contants
	min_improvement=0.0001
	learn_rate=lrate
	min_epochs = e
	max_epochs = 200
	
	#init variables
	rmse = 1000	
	rmse_last = 1000
	
	
	for f in range(n_features):
		
		print "\t%s - Calculating feature %d of %d" % (time.strftime('%X'), f+1, n_features)
		sys.stdout.flush()
		
		# rmse_last = 1000
		
		# Keep looping until you have passed a minimum number 
        # of epochs or have stopped making significant progress
		#for e in range(min_epochs):
		e = 0
		while (e < min_epochs or rmse <= rmse_last - min_improvement) and e < max_epochs:
		# while e < max_epochs:
			
			print "\t\t%s - Epoch %d of %d" % (time.strftime('%X'), e+1, max_epochs)
			sys.stdout.flush()
			
			n = 0
			sq = 0
			rmse_last = rmse
			
			for i in xrange(n_users):
				for j in xrange(n_movies):
					if R[i][j] > 0:		
					
						# Predict rating and calc error
						rated = R[i][j]
						predicted = predict_rating_for_feature(i, j, f, W, Q, cache_R)
						err = rated - predicted
					
						if i==100 and (j==104 or j==480):
							print 'i:%d, j:%d :: rated = %f, predicted = %f (w= %f, q= %f), err = %f' % (i, j, rated, predicted, W[i,f], Q[f,j], err)
							sys.stdout.flush()
					
						sq = sq + (err**2)
						n = n + 1
					
						# Cache off old feature values
						cf = W[i,f]
						mf = Q[f,j]

						# Cross-train the features
						W[i,f] = W[i,f] + learn_rate * (err * mf - regularization * cf)
						Q[f,j] = Q[f,j] + learn_rate * (err * cf - regularization * mf)
			
			rmse = sqrt(sq/n)
			
			print "\t\t\trmse=%f" % rmse
			sys.stdout.flush()
			
			# if rmse > rmse_last - min_improvement:
			# 	break
			# else:
			# 	rmse_last = rmse
			
			e = e + 1
		
		err = 0
		# Cache off old predictions
		for i in xrange(n_users):
			for j in xrange(n_movies):
				if R[i][j] > 0:
					cache_R[i,j] = predict_rating_for_feature(i, j, f, W, Q, cache_R)
				
			
	return W, Q
	
"""
"""
def predict_rating_for_feature (i, j, f, W, Q, cache_R):
	
	if cache_R[i,j] > 0:
		result = cache_R[i,j]
	else:
		# TODO: mean + bias(user) + bias(item)
		result = 4.0 # global bias - PseudoAvg

	# Add contribution of current feature
	result = result + W[i,f] * Q[f,j]
	
	# if result > 5.0:
	# 	result = 5.0
	# if result < 1.0:
	# 	result = 1.0
	
	# Add up trailing defaults values
	
	return result

"""
"""
def predict_rating (i, j, W, Q):

	result = 4.0 # global bias - PseudoAvg

	# Add contribution of current feature
	result = result + dot(W[i,:], Q[:,j])

	# if result > 5.0:
	#  	result = 5.0
	# if result < 1.0:
	#  	result = 1.0

	return result

"""
"""
def test_factorization (W, Q, data, user_index, movie_index):

	i=0
	err = 0.0

	for user_ratings in data.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			if user_index.has_key(user) and movie_index.has_key(movie_id):
				predicted = predict_rating( user_index[user], movie_index[movie_id], W, Q )
				rated = float( data[user][movie_id] )
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 500 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)

	mse = err/i
	rmse = sqrt(mse)

	return rmse

def define_params(R, K, e, lrate, reg, train, test, user_index, movie_index):
	
	nW, nQ = learn_factors(R, K, e, lrate, reg)

	#validate on testing data
	rmse_train = test_factorization(nW, nQ, train, user_index, movie_index)
	print "\nRMSE train: %s (K=%d, e=%d, lrate=%s, reg=%f)" % (rmse_train, K, e, lrate, reg)
	sys.stdout.flush()

	#validate on testing data
	rmse_test = test_factorization(nW, nQ, test, user_index, movie_index)
	print "\nRMSE test: %s (K=%d, e=%d, lrate=%s, reg=%f)" % (rmse_test, K, e, lrate, reg)
	sys.stdout.flush()

	print "\nEnd time: %s (K=%d, e=%d, lrate=%s, reg=%f)" % (time.strftime('%X %x %Z'), K, e, lrate, reg)
	sys.stdout.flush()


"""
MAIN
"""
if __name__ == "__main__":
	
	print "Start training: %s\n" % time.strftime('%X %x %Z')
	sys.stdout.flush()
	
	#load dataset
	train, test, users, movies = load_movielens()
	#train, test = load_globocom()
	user_index, movie_index = build_indexes( train )
	
	#train dataset
	#K = 10 # number of latent variables
	R = init_data_matrix(user_index, movie_index, train)

	for lrate in [0.0015]:
		for reg in [0.045]:
			for e in [120]:
				for K in [100]:
					p = Process(target=define_params, args=(R, K, e, lrate, reg, train, test, user_index, movie_index))
					p.start()