import md5

def isAuthenticated(request):
	""" Check if a user is authenticated """
	if request.user.is_authenticated():
		return True

	return False

def parseAjaxParam(param):
	""" Force a cast to int of get parameters """
	return int(param)

def sessionName(identifier):
	""" Return a session name for a give identifer """
	return md5.new(str(identifier)).hexdigest()
