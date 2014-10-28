import dropbox
import config

def authorizeURL():
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.app_key, config.app_secret)
	authorizeUrl = flow.start()
	return authorizeUrl

def accessToken(code):
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config.app_key, config.app_secret)
	accessToken, userID = flow.finish(code) 
	return  accessToken, userID

