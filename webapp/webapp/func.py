
def isAuthenticated(request):
	""" Check if a user is authenticated """
	if request.user.is_authenticated():
		return True

	return False

def parseAjaxParam(param):
	""" Force a cast to int of get parameters """
	return int(param)
