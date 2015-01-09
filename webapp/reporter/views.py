from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.conf import settings
import sys, os, json
from datetime import date
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.contrib.auth.decorators import login_required
from django import forms
from webapp.exceptionFormatter import formatException
from webapp import constConfig
from reportGenerator import ReportGenerator

@login_required
def generateReport(request,cloudItemID,tokenID):

	ci = None
	token = None
	error = False

	try:
		ci = checkCloudItem(cloudItemID,request.user.id)
		token = checkAccessToken(tokenID,ci)

		if request.method == 'POST':
			rg = ReportGenerator(token.id)
			return rg.genPDF()

	except Exception as e:
		error = formatException(e)

	return render_to_response("dashboard/reporter/reporterHome.html", {'showToken': True,'objID':ci.id,'tokenID':token.id,'error': error}, context_instance=RequestContext(request))

