'''
User-based recommendation with SVD

Port of the ruby code presented here:
http://www.igvita.com/2007/01/15/svd-recommendation-system-in-ruby/

Since I'm not a python expert, refactoring suggestions are appreciated.
'''

from scipy import *
from numpy import *
from math import *

def cosine_distance(u, v):
	"""
	Returns the cosine of the angle between vectors v and u. This is equal to u.v / |u||v|.
	"""
	return dot( u, v.T ) / (sqrt( dot( u, u.T ) ) * sqrt( dot( v, v.T ) ))

def

users = { 1 : "Ben", 2 : "Tom", 3 : "John", 4 : "Fred" }

m = mat( [
           #Ben, Tom, John, Fred,  Bob
			[5,5,0,5], # season 1  5
			[2,0,3,4], # season 2  5
			[1,4,0,3], # season 3  0
			[0,0,5,3], # season 4  0
			[5,4,4,5], # season 5  0
			[5,4,5,5]  # season 6  5
            ] )

# Compute the SVD Decomposition
u, s, v = linalg.svd( m )
vt = v.transpose()

# Take the 2-rank approximation of the Matrix
#   - Take first and second columns of u  (6x2)
#   - Take first and second columns of vt (4x2)
#   - Take the first two eigen-values (2x2)
u2 = column_stack( (u[:,0], u[:,1]) )
v2 = column_stack( (vt[:,0], vt[:,1]) )
eig2 = diag(s)[:2,:2]

# Here comes Bob, our new user
bob = mat( [[5,5,0,0,0,5]] )
bobEmbed = bob * u2 * linalg.inv(eig2)

# Compute the cosine similarity between Bob and every other User in our 2-D space
user_sim, count = {}, 1
for user in v2:
	user_sim[count] =  cosine_distance( bobEmbed, user )
	count += 1

# Remove all users who fall below the 0.90 cosine similarity cutoff and sort by similarity
similar_users = [(s, u) for u, s in user_sim.items()] # if s > 0.9]
similar_users.sort()
similar_users.reverse()
similar_users = [(u, s) for s, u in similar_users]

for u, s in similar_users:
	print '%s (ID: %d, Similarity: %.3f)' % (users[u], u, s.item())

# We'll use a simple strategy in this case:
#   1) Select the most similar user
#   2) Compare all items rated by this user against your own and select items that you have not yet rated
#   3) Return the ratings for items I have not yet seen, but the most similar user has rated
#similarUsersItems = m.column(similar_users[0][0]-1).transpose.to_a.flatten
similar_users_items = m[:,similar_users[0][0]-1]
bob_items = bob.transpose()

not_seen_yet = {}
for i in range( len( bob_items ) ):
	if bob_items[i] == 0 and similar_users_items[i] != 0:
		not_seen_yet[i+1] = similar_users_items[i]

print '\n%s recommends:' % (users[similar_users[0][0]])

not_seen_yet = [(r, s) for s, r in not_seen_yet.items()]
not_seen_yet.sort()
not_seen_yet.reverse()
not_seen_yet = [(s, r) for r, s in not_seen_yet]

for s, r in not_seen_yet:
	print 'Season %d .. I gave it a rating of %d' % (s, r.item())

if len(not_seen_yet) == 0 : print 'We\'ve seen all the same seasons, bugger!'