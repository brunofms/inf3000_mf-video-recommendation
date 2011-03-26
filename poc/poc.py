from dataset import bbb_data
from recommendations import matrix_factorization
import numpy

if __name__ == "__main__":
	R = [
	[5,3,0,1],
	[4,0,0,1],
	[1,1,0,5],
	[1,0,0,4],
	[0,1,5,4],
	]

	R = numpy.array(R)

	N = len(R)
	M = len(R[0])
	K = 2

	P = numpy.random.rand(N,K)
	Q = numpy.random.rand(M,K)

	nP, nQ = matrix_factorization(R, P, Q, K)

	print nP
	print nQ