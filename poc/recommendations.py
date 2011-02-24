def loadMovieLens( path='../data/movielens' ):
	
	# Get movie titles
	movies={}
	for line in open( path + '/u.item' ):
		(id, title) = line.split( '|' )[0:2]
		movies[id]=title
	
	# Load data
	prefs={}
	for line in open( path + '/u.data' ):
		(user, movieid, rating, ts) = line.split('\t')
		prefs.setdefault( user, {} )
		prefs[user][movies[movieid]] = float( rating )
	
	return prefs

prefs = loadMovieLens()
for (m, r) in prefs['196'].items():
	print m, ":", r