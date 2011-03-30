from math import sqrt
import numpy

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
		if step % 500 == 0:
			print "Progress: %d%%" % (step*100/steps)
		if e < 0.001:
			break
	return P, Q.T

"""
"""
def test_results (nR, data):
	
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
	
	mse = err/i
	rmse = sqrt(mse)
	
	return rmse