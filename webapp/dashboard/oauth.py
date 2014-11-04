import dropbox
import config
from oauth2client.client import OAuth2WebServerFlow

def dropboxAuthorizeURL():
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.DROPBOX_APP_KEY, config.DROPBOX_APP_SECRET)
	authorizeUrl = flow.start()
	return authorizeUrl

def dropboxAccessToken(code):
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.DROPBOX_APP_KEY, config.DROPBOX_APP_SECRET)
	accessToken, userID = flow.finish(code) 
	return  accessToken, userID

def googleAuthorizeURL():
	flow = OAuth2WebServerFlow(config.GOOGLE_CLIENT_ID,config.GOOGLE_CLIENT_SECRET,config.GOOGLE_OAUHT_SCOPE,config.GOOGLE_REDIRECT_URI)
	return flow.step1_get_authorize_url()
