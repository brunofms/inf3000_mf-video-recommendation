from movielens import *
from recommendations import *
import numpy, time

if __name__ == "__main__":
	
	print "Start time: %s\n" % time.strftime('%X %x %Z')
	
	#load dataset
	train, test = load_movielens()
	user_index, movie_index = build_indexes( train )
	
	#train dataset
	K = 2
	R, P, Q = format_data(user_index, movie_index, train, K)
	nP, nQ = matrix_factorization(R, P, Q, K)
	nR = numpy.dot(nP, nQ.T)
	
	#test results
	rmse = test_results(nR, test)
	print "\nRMSE: %s" % rmse
	
	print "\nEnd time: %s" % time.strftime('%X %x %Z')