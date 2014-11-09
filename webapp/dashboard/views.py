from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import dash

# Create your views here.


def showdash(request):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	if request.user.is_authenticated():
		index = int(request.GET.get('i', 0))

		if index > 0:
			s = request.GET.get('s', 'null')

			if s == "display":
				data = dash.importViewer(index)
				tmpl = "viewer.html"
			elif s == "cloud":
				data = dash.cloudDownloader(index)
				tmpl = "cloud.html"
			elif s == "dropbox" or s == "google" or s == "onedrive":
				tokenID = int(request.GET.get("t",0))
				
				if tokenID == 0:
					return redirect("/dashboard/?i="+str(index)+"&s=cloud")

				data = cloudService(request,s)
				tmpl = "clouservice/cloudHome.html"
			
			data['objID'] = index
			return render_to_response("dashboard/" + tmpl, data, context_instance=RequestContext(request))
		else: 
			return redirect("/import/")
	else:
		return redirect("/login/")
