import urllib2
import json

class API:
	
	def get_video( self, id ):		
		url = "http://api.webmedia.qa02.globoi.com/videos/%s.json" % (id)		
		request = urllib2.Request ( url )
		response = urllib2.urlopen(request)		
		v_json = response.read()
		
		return json.loads( v_json )