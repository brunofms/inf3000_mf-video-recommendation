from operator import itemgetter
import webmedia

#
# carrega o dataset da globo.com
#
def loadGloboCom( path='../data/globocom/bbb' ):
	
	# Load data
	views={}
	
	for line in open( path + '/bbb.mar.1000000.data' ):
		
		try:
			(ts, video_id, user) = line.strip().split( '\t' )
			views.setdefault( user, {} )
			views[user][video_id] = 1.0
			
		except 	Exception, why:
			pass
	
	return views

#
# remove usuarios que viram menos que MIN videos
#
def filterByMinViews( view_data, min=20 ):
	
	#Load data
	filtered_views={}
	
	for u, v in view_data.items():
		try:
			if len(v) > min:
				filtered_views.setdefault( u, {} )
				filtered_views[u] = v
		except:
			pass
				
	
	return filtered_views

#
# verifica a distribuicao da quantidade de videos pela quantidade de usuarios
#
def arrangeViewedDistributionPerUser ( view_data ):
	
	user_count = {}
	viewed_count = {}
	
	for user, videos in view_data.items():
		try:
			user_count[user] = user_count.get( user, 0 ) + len(videos)
		except:
			pass
			
	for user, viewed in user_count.items():
		try:
			viewed_count[viewed] = viewed_count.get( viewed, 0 ) + 1
		except:
			pass
	
	f = open( '../data/globocom/file.txt', 'w' )
	
	for viewed, count in viewed_count.items():
		f.write( str(viewed) + "\t" + str(count) + "\n" )
	
	f.close()

#
# carrega o dataset da movielens
#
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

#prefs = loadMovieLens()
#for (m, r) in prefs['196'].items():
#	print m, ":", r

bbb_data = filterByMinViews( loadGloboCom() )
#arrangeViewedDistributionPerUser ( raw_data )

#api = webmedia.API()
# users = 0
# ratings = 0
# for u, v in views.items():
# 	try:
# 		users = users + 1
# 		for v, r in v.items():
# 			ratings = ratings + 1
#				print u, v, r
#				video = api.get_video(v)
#				print u, "::", video['title'], "::", r
# 	except:
# 		pass
# 
# print "no. users = ", users
# print "no. ratings = ", ratings