from dataset import views
from recommendations import matrix_factorization
import numpy, time

if __name__ == "__main__":
	
	print "Start time: %s\n" % time.strftime('%X %x %Z')
	
	user_index = {}
	P = {}
	video_index = {}
	Q = {}
	
	i = 0
	j = 0
	nr = 0
	for user_views in views.items():
		
		user = user_views[0]
		user_index[user] = i
		P[user] = numpy.random.random_sample(1)[0]
		i = i + 1
		
		video_collection = user_views[1]
		nr = nr + len(video_collection)
		
		for video in video_collection.keys():
			if not video_index.has_key(video):
				video_index[video] = j
				Q[video] = numpy.random.random_sample(1)[0]
				j = j + 1

	nu = len(user_index)
	nv = len(video_index)
	print "%d users" % nu
	print "%d videos" % nv
	print "%d videos vistos (ratings)\n" % nr
				
	dimension = (nu, nv)
	R = numpy.zeros(dimension)
	
	for user_views in views.items():
		user = user_views[0]
		video_collection = user_views[1]
		for video in video_collection.keys():
			R[user_index[user]][video_index[video]] = 1.0
	
	#print R
		
	N = len(R)
	M = len(R[0])
	K = 2

	P = numpy.random.rand(N,K)
	Q = numpy.random.rand(M,K)

	nP, nQ = matrix_factorization(R, P, Q, K)
	nR = numpy.dot(nP, nQ.T)

	#print nR
	
	print "\nEnd time: %s" % time.strftime('%X %x %Z')