from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext


# Create your views here.

def gdriveViewer(request):
	""" Display the function page """
	if request.user.is_authenticated():
		return render_to_response("gdrivecloud/gdrive.html", {}, context_instance=RequestContext(request))
	else:
		return redirect("/login/")

