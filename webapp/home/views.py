from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.

def main_page(request):
	if request.user.is_authenticated():
		return render_to_response('home/home.html', { 'uname': request.user.username})
				                        
	else:
		return HttpResponse("no...")
