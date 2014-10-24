from django.shortcuts import render, redirect

# Create your views here.


def importer(request):
	if request.user.is_authenticated():
		print "in"
	else:
		return redirect("/login/")
