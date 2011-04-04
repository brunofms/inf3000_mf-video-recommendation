from math import *
from numpy import *
from time import *

"""
@INPUT:
R     : a matrix to be factorized, dimension N x M
P     : an initial matrix of dimension N x K
Q     : an initial matrix of dimension M x K
K     : the number of latent features
steps : the maximum number of steps to perform the optimisation
alpha : the learning rate
beta  : the regularization parameter
@OUTPUT:
the final matrices P and Q
"""
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
	Q = Q.T
	for step in xrange(steps):
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0:
					eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * ( 2 * eij * Q[k][j] - beta * P[i][k] )
						Q[k][j] = Q[k][j] + alpha * ( 2 * eij * P[i][k] - beta * Q[k][j] )
		eR = numpy.dot( P, Q )
		e = 0
		for i in xrange( len( R ) ):
			for j in xrange( len( R[i] ) ):
				if R[i][j] > 0:
					e = e + pow( R[i][j] - numpy.dot( P[i,:], Q[:,j] ), 2 )
					for k in xrange(K):
						e = e + (beta/2) * ( pow( P[i][k], 2 ) + pow( Q[k][j], 2 ) )
		if e < 0.001:
			break
		if step % 500 == 0:
			print "Progress: %d%%, %s" % (step*100/steps, time.strftime('%X'))
	return P, Q.T

"""
"""
def learn_factors (R, W, Q, K, min_improvement=0.0001, learn_rate=0.0002, regularization=0.02):
	
	#init contants
	min_epochs = 120
	max_epochs = 200
	
	#init variables
	rmse_last = 0
	rmse = 2.0
	
	
	for f in range(K):
		
		e = 0
		
		print "\tCalculating feature %d" % (f+1)
		
		# Keep looping until you have passed a minimum number 
        # of epochs or have stopped making significant progress
		#for e in range(min_epochs):
		while (e < min_epochs or rmse <= rmse_last - min_improvement) and e < max_epochs:
			
			print "\t\tEpoch %d" % (e+1)
			
			n = 0
			sq = 0
			rmse_last = rmse
			
			for i in xrange(len(R)):
				for j in xrange(len(R[i])):
					
					# Predict rating and calc error
					err = R[i][j] - predict_rating_for_feature(i, j, f, W, Q)
					sq = sq + (err**2)
					n = n + 1

					# Cache off old feature values
					cf = W[f][i]
					mf = Q[f][j]

					# Cross-train the features
					W[f][i] = W[f][i] + learn_rate * (2 * err * mf - regularization * cf)
#					W[f][i] = W[f][i] + learn_rate * (err * mf - regularization * cf)
					Q[f][j] = Q[f][j] + learn_rate * (2 * err * cf - regularization * mf)
#					Q[f][j] = Q[f][j] + learn_rate * (err * cf - regularization * mf)

					#print "W[%d][%d]=%f, Q[%d][%d]=%f" % (f, i, W[f][i], f, j, Q[f][j])
			
			rmse = sqrt(sq/n)
			
			print "\t\t\trmse=%f" % rmse
			
			e = e + 1
			
#			if rmse > rmse_last - min_improvement:
#				break
	return W, Q
	
"""
"""
def predict_rating_for_feature (i, j, f, W, Q):
	
	result = 1.0 # global bias
	# result = 0.2 # global bias
	
	# Add contribution of current feature
	result = result + W[f][i] * Q[f][j]
	
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

	result = 1.0 # global bias
	# result = 0.2 # global bias

	for f in range(K):
		result = result + W[f][i] * Q[f][j]
	
	if result > 5.0:
		result = 5.0
	if result < 1.0:
		result = 1.0

	# if result > 1.0:
	# 	result = 1.0
	# if result < 0.0:
	# 	result = 0.0

	return result