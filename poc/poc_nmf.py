from dataset import *
from recommendations import *
import numpy, time

"""
"""
def difcost(a, b):
	dif=0
	# Loop over every row and column in the matrix
	for i in range(shape(a)[0]):
		for j in range(shape(a)[1]):
			# Add together the differences
			dif+=pow(a[i,j]-b[i,j],2)
	return dif

"""
"""
def factorize(v, pc=10, iter=200):
	ic=shape(v)[0]
	fc=shape(v)[1]

	#Initialize the weight and feature matrices with random values
	w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
	h=matrix([[random.random() for i in range(fc)] for j in range(pc)])

	# Perform operation a maximum of item times
	for i in range(iter):
		wh=w*h
	
		# Calculate the current difference
		cost=difcost(v, wh)		
		if i%5==0: print cost
	
		# Terminate if the matrix has been fully factorized
		if cost==0: break
	
		# Update feature matrix
		hn=(transpose(w)*v)
		hd=(transpose(w)*w*h)
	
		h=matrix(array(h)*array(hn)/array(hd))
	
		# Update weights matrix
		wn=(v*transpose(h))
		wd=(w*h*transpose(h))
	
		w=matrix(array(w)*array(wn)/array(wd))

	return w,h

"""
"""
def test_factorization (nR, data, user_index, movie_index):

	i=0
	err = 0.0

	for user_ratings in data.items():
		user = user_ratings[0]
		ratings = user_ratings[1]
		for movie_id in ratings.keys():
			if user_index.has_key(user) and movie_index.has_key(movie_id):
				predicted = nR[user_index[user],movie_index[movie_id]]
				rated = float( data[user][movie_id] ) # 1.0
				err = err + (rated - predicted)**2
				i = i + 1
				if i % 50 == 0:
					print 'err: %f - rated: %f, predicted: %f' % (err, rated, predicted)
				# if user_index[user]<=2 and movie_index[movie_id]<=2:
				# 					print "train[%d][%d]: rated=%f predicted=%f" % (user_index[user], movie_index[movie_id], data[user][movie_id],  nR[user_index[user],movie_index[movie_id]])

	mse = err/i
	rmse = sqrt(mse)

	return rmse

def showfeatures(w, h, user_index, movie_index, out='features.txt'):
	outfile=file(out, 'w')
	pc,wc=shape(h)
	toppatterns=[[] for i in range(len(user_index))]
	patternnames=[]
	
	# Loop over all the features
	for i in range(pc):
		slist=[]
		# Create a list of words and their weights
		for j in range(wc):
			slist.append((h[i,j],movie_index[j]))
		# Reverse sort the word list
		slist.sort()
		slist.reverse()
		
		# Print the first six elements
		n=[s[1] for s in slist[0:6]]
		outfile.write(str(n)+'\n')
		patternnames.append(n)
		
		#Create a list of articles for this feature
		flist=[]
		for j in range(len(user_index)):
			# Add the article with its weight
			flist.append((w[i,j],user_index[j]))
			toppatterns[j].append((w[i,j],i,user_index[j]))
		
		# Reverse sort the list
		flist.sort()
		flist.reverse()
		
		# Show the top 3 articles
		for f in flist[0:3]:
			outfile.write(str(f)+'\n')
		outfile.write('\n')
	
	outfile.close()
	
	# Return the pattern names for later use
	return toppatterns, patternnames

if __name__ == "__main__":
	
	print "Start time: %s\n" % time.strftime('%X %x %Z')
	
	#load dataset
#	train, test = load_globocom()
	train, test = load_movielens()
	user_index, movie_index = build_indexes( train )
	
	#train dataset
	K = 20 # number of latent variables
#	R, P, Q = format_data(user_index, movie_index, train, K)
#	nP, nQ = matrix_factorization(R, P, Q, K)
#	nR = numpy.dot(nP, nQ.T)
	R, W, Q = init_data(user_index, movie_index, train, K)
	nW, nQ = factorize(R, K)
	nR=nW*nQ
	
	print "Start testing: %s\n" % time.strftime('%X %x %Z')

	print R
	print nR
	
	#test results
	rmse = test_factorization(nR, train, user_index, movie_index)
	print "\nRMSE treino: %s" % rmse
	rmse = test_factorization(nR, test, user_index, movie_index)
#	rmse = process_test (test, nW, nQ, user_index, movie_index, K)
	print "\nRMSE test: %s" % rmse
	
	print "\nEnd time: %s" % time.strftime('%X %x %Z')