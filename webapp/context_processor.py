
def global_vars(request):
	return { 'isAuthenticated': request.user.is_authenticated(), 'uname': request.user.username }
