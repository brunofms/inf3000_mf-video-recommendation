from dataset import *
from numpy import *
import scipy, time

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
def matrix_factorization(R, n_features, steps=4, alpha=0.0001, beta=0.02):
	
	n_users=shape(R)[0]
	n_movies=shape(R)[1]

	#Initialize the weight and feature matrices with random values
	w=matrix([[random.random() for f in range(n_features)] for u in range(n_users)])
	h=matrix([[random.random() for m in range(n_movies)] for f in range(n_features)])
	
	for step in xrange(steps):
		for i in xrange(n_users):
			for j in xrange(n_movies):
				if R[i][j] > 0:
					eij = R[i][j] - dot(w[i,:],h[:,j])
					for f in xrange(n_features):
						w[i,f] = w[i,f] + alpha * ( 2 * eij * h[f,j] - beta * w[i,f] )
						h[f,j] = h[f,j] + alpha * ( 2 * eij * w[i,f] - beta * h[f,j] )
		# eR = numpy.dot( P, Q )
		e = 0
		for i in xrange(n_users):
			for j in xrange(n_movies):
				if R[i][j] > 0:
					e = e + pow( R[i][j] - dot( w[i,:], h[:,j] ), 2 )
					for f in xrange(n_features):
						e = e + (beta/2) * ( pow( w[i,f], 2 ) + pow( h[f,j], 2 ) )
		if e < 0.001:
			print "e < 0.001: BREAK!!!"
			break
		if step % 5 == 0:
			print "Progress: %d%% -- e = %f" % (step*100/steps, e)
	return w, h

"""
"""
def test_factorization (w, h, data, user_index, movie_index):

	i=0
	err = 0.0

	for user_ratings in data.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			if user_index.has_key(user) and movie_index.has_key(movie_id):
				predicted = dot( w[user_index[user],:], h[:,movie_index[movie_id]])
				rated = float( data[user][movie_id] ) # 1.0
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 500 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)

	mse = err/i
	rmse = sqrt(mse)

	return rmse

"""
"""
def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]	

"""
"""
def showfeatures(w, h, user_index, movie_index, users, movies, out='features.txt'):
	outfile=file(out, 'w')
	wc,pc=shape(w)
	
	# Loop over all the features
	for f in range(pc):
		
		outfile.write('Feature '+str(f)+':\n')
		
		ulist=[]
		# Create a list of users and their weights
		for u in range(wc):
			ulist.append((w[u,f],find_key(user_index,u)))
		# Reverse sort the users list
		ulist.sort()
		ulist.reverse()
		
		# Print the first six elements
		n=[u[1] for u in ulist[0:5]]
		outfile.write(str(n)+'\n')
		
		#Create a list of movies for this feature
		mlist=[]
		for m in range(len(movie_index)):
			# Add the movie with its weight
			mlist.append((h[f,m],movies[find_key(movie_index,m)]['title']))
		
		# Reverse sort the list
		mlist.sort()
		mlist.reverse()
		
		# Show the top 3 movies
		for m in mlist[0:5]:
			outfile.write(str(m)+'\n')
		outfile.write('\n')
	
	outfile.close()

"""
MAIN
"""
if __name__ == "__main__":
	
	print "Start time: %s\n" % time.strftime('%X %x %Z')
	
	#load dataset
	train, test, users, movies = load_movielens()
	user_index, movie_index = build_indexes( train )
	
	#train dataset
	f = 20 # number of latent variables
	R = init_data_matrix(user_index, movie_index, train)
	nW, nQ = matrix_factorization(R, f)
	
	print "Start testing: %s\n" % time.strftime('%X %x %Z')

	# print R
	# print nR
	
	#validate on training data
	rmse = test_factorization(nW, nQ, train, user_index, movie_index)
	print "\nRMSE treino: %s" % rmse

	#validate on testing data	
	rmse = test_factorization(nW, nQ, test, user_index, movie_index)
	print "\nRMSE test: %s" % rmse
	
	print "\nEnd time: %s" % time.strftime('%X %x %Z')
	
	showfeatures(nW, nQ, user_index, movie_index, users, movies)