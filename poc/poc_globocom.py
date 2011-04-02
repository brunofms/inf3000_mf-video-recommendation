from dataset import *
from recommendations import *
import numpy, time

if __name__ == "__main__":
	
	print "Start time: %s\n" % time.strftime('%X %x %Z')
	
	#load dataset
	train, test = load_globocom()
	user_index, movie_index = build_indexes( train )
	
	#train dataset
	K = 16 # number of latent variables
#	R, P, Q = format_data(user_index, movie_index, train, K)
#	nP, nQ = matrix_factorization(R, P, Q, K)
#	nR = numpy.dot(nP, nQ.T)
	R, W, Q = init_data(user_index, movie_index, train, K)
	nW, nQ = learn_factors(R, W, Q, K)
	
	print "Start testing: %s\n" % time.strftime('%X %x %Z')
	
	#test results
#	rmse = test_predictions(nR, test, user_index, movie_index)
	rmse = process_test (test, nW, nQ, user_index, movie_index, K)
	print "\nRMSE: %s" % rmse
	
	print "\nEnd time: %s" % time.strftime('%X %x %Z')