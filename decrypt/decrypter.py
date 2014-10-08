#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##
###
####

import getpass, platform, sqlite3, os, glob, json

def getPasswords(loginFile):
	""" Select password from relative database """
	conn = sqlite3.connect(loginFile)

	if loginFile is GCHROME_LOGIN_FILE:
		query = "SELECT username_value, quote(password_value), origin_url FROM logins"
	elif loginFile is FF_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"

	for row in conn.execute(query):
		print row


def readLoginsJSON(loginFileJSON):
	""" Read the JSON of Firefox login data """
	data = json.loads(open(loginFileJSON).read())
	print data['logins'][0]['encryptedUsername']
	print data['logins'][0]['encryptedPassword']
	print data['logins'][0]['hostname']

GCHROME_LOGIN_FILE = "Login Data"
FF_LOGIN_FILE_DB = "signons.sqlite"
FF_LOGIN_FILE_JSON = "logins.json"

username = getpass.getuser()

GCHROME_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Local\Google\Chrome\User Data"
FF_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Mozilla\Firefox\Profiles"
TH_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Thunderbird\Profiles"

GCHROME_PROFILE_LINUX = "/home/" + username + "/.config/google-chrome/Default"
FF_PROFILE_LINUX = "/home/" + username + "/.mozilla/firefox"
TH_PROFILE_WIN = "/home/" + username + "/.thunderbird"

#detect os and look in specific folders

if platform.system() == "Linux":
	#google-chrome
	os.chdir(GCHROME_PROFILE_LINUX)
	getPasswords(GCHROME_LOGIN_FILE)

	#firefox
	#get first default profile directory
	os.chdir(FF_PROFILE_LINUX)
	listing = glob.glob(FF_PROFILE_LINUX+"/*")
	
	for profileDir in listing:
		if not profileDir.endswith("profiles.ini"):
			
			os.chdir(profileDir)

			# look for signons.sqlite
			if os.path.isfile(FF_LOGIN_FILE_DB):
				getPasswords(FF_LOGIN_FILE_DB)
			
			# look for logins.json
			if os.path.isfile(FF_LOGIN_FILE_JSON):
				readLoginsJSON(FF_LOGIN_FILE_JSON)
			
			#go up one directory
			os.chdir(os.path.dirname(os.getcwd()))
	
elif platform.system() == "Windows":
	print "Win"
