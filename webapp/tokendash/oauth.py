import dropbox
import config
from django.conf import settings
import os
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
import logging
#logging.basicConfig(filename=os.path.join(settings.BASE_DIR,"debug.log"),level=logging.DEBUG)

def dropboxAuthorizeURL():
	""" Generate the authorization URl for Dropbox login """
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.DROPBOX_APP_KEY, config.DROPBOX_APP_SECRET)
	authorizeUrl = flow.start()
	return authorizeUrl

def dropboxAccessToken(code):
	""" Get the access token for Dropbox """
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.DROPBOX_APP_KEY, config.DROPBOX_APP_SECRET)
	accessToken, userID = flow.finish(code) 
	return  accessToken, userID

def googleAuthorizeURL():
	""" Generate the authorization URl for Google Login """

	flow = OAuth2WebServerFlow(config.GOOGLE_CLIENT_ID,config.GOOGLE_CLIENT_SECRET,config.GOOGLE_OAUHT_SCOPE,config.GOOGLE_REDIRECT_URI)
	return flow.step1_get_authorize_url()

def googleAccessToken(code):
	""" Get the access token for Google """

	flow = OAuth2WebServerFlow(config.GOOGLE_CLIENT_ID,config.GOOGLE_CLIENT_SECRET,config.GOOGLE_OAUHT_SCOPE,config.GOOGLE_REDIRECT_URI)
	credentials = flow.step2_exchange(code)
	return credentials
