from math import *
from numpy import *
from time import *
import sys

"""
"""
def learn_factors (R, n_features, min_improvement=0.0001, learn_rate=0.0001, regularization=0.02):

	n_users=shape(R)[0]
	n_movies=shape(R)[1]
	
	#Initialize the weight and feature matrices with random values
	W=matrix([[random.random() for f in range(n_features)] for u in range(n_users)])
	Q=matrix([[random.random() for m in range(n_movies)] for f in range(n_features)])
	
	#init contants
	min_epochs = 10
	max_epochs = 200
	
	#init variables
	rmse_last = 2.0
	rmse = 2.0
	
	
	for f in range(n_features):
		
		print "\tCalculating feature %d of %d" % (f+1, n_features)
		sys.stdout.flush()
		
		# Keep looping until you have passed a minimum number 
        # of epochs or have stopped making significant progress
		#for e in range(min_epochs):
		e = 0
		while (e < min_epochs or rmse <= rmse_last - min_improvement) and e < max_epochs:
			
			print "\t\tEpoch %d" % (e+1)
			sys.stdout.flush()
			
			n = 0
			sq = 0
			rmse_last = rmse
			
			for i in xrange(n_users):
				for j in xrange(n_movies):
					
					# Predict rating and calc error
					err = R[i][j] - predict_rating_for_feature(i, j, f, W, Q)
					sq = sq + (err**2)
					n = n + 1

					# Cross-train the features
					W[i,f] = W[i,f] + learn_rate * (2 * err * Q[f,j] - regularization * W[i,f])
					Q[f,j] = Q[f,j] + learn_rate * (2 * err * W[i,f] - regularization * Q[f,j])
			
			rmse = sqrt(sq/n)
			
			print "\t\t\trmse=%f" % rmse
			sys.stdout.flush()
			
			e = e + 1
			
	return W, Q
	
"""
"""
def predict_rating_for_feature (i, j, f, W, Q):
	
	result = 1.0 # global bias
	# result = 0.2 # global bias
	
	# Add contribution of current feature
	result = result + dot( W[i,:], Q[:,j])
	
	if result > 5.0:
		result = 5.0
	if result < 1.0:
		result = 1.0
	
	# if result > 1.0:
	# 	result = 1.0
	# if result < 0.0:
	# 	result = 0.0
	
	return result

"""
"""
def test_predictions (nR, data, user_index, movie_index):
	
	i=0
	err = 0.0
	
	for user_ratings in data.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			if user_index.has_key(user) and movie_index.has_key(movie_id):
				predicted = nR[user_index[user]][movie_index[movie_id]]
				rated = float( data[user][movie_id] ) # 1.0
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 300 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)
	
	mse = err/i
	rmse = sqrt(mse)
	
	return rmse

	

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
				predicted = dot( W[user_index[user],:], Q[:,movie_index[movie_id]])
				
				if predicted > 5.0:
					predicted = 5.0
				if predicted < 1.0:
					predicted = 1.0
				
				rated = float( data[user][movie_id] )
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 500 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)

	mse = err/i
	rmse = sqrt(mse)

	return rmse

"""
"""
def process_test (test, nW, nQ, user_index, movie_index, K):

	i=0
	err = 0.0
		
	for user_ratings in test.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			if user_index.has_key(user) and movie_index.has_key(movie_id):
				predicted = predict_rating(nW, nQ, user_index[user], movie_index[movie_id], K)
				rated = float( test[user][movie_id] ) # 1.0
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 300 == 0:
				# if i % 5 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)
	
	mse = err/i
	rmse = sqrt(mse)
	
	return rmse

"""
"""
def predict_rating (W, Q, i, j, K):

	#result = 1.0 # global bias
	result = 0.0 # global bias

	#for f in range(K):
	result = result + dot( W[i,:], Q[:,j])
	
	if result > 5.0:
		result = 5.0
	if result < 1.0:
		result = 1.0

	# if result > 1.0:
	# 	result = 1.0
	# if result < 0.0:
	# 	result = 0.0

	return result