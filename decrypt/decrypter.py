#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##
###
####

import getpass, platform, sqlite3, os, json

### Constants

GCHROME_LOGIN_FILE = "Login Data"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"

username = getpass.getuser()

GCHROME_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Local\Google\Chrome\User Data"
FF_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Mozilla\Firefox\Profiles"
TH_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Thunderbird\Profiles"

GCHROME_PROFILE_LINUX = "/home/" + username + "/.config/google-chrome/Default"
FF_PROFILE_LINUX = "/home/" + username + "/.mozilla/firefox"
TH_PROFILE_LINUX = "/home/" + username + "/.thunderbird"

### End Constants

### Def

def getPasswords(loginFile):
	""" Select password from relative database """
	print "Opening " + loginFile
	conn = sqlite3.connect(loginFile)

	if loginFile is GCHROME_LOGIN_FILE:
		query = "SELECT username_value, quote(password_value), origin_url FROM logins"
	elif loginFile is MOZ_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"

	for row in conn.execute(query):
		print row


def readLoginsJSON(loginFileJSON):
	""" Read the JSON of Firefox login data """
	data = json.loads(open(loginFileJSON).read())
	print data['logins'][0]['hostname'] + ", " + data['logins'][0]['encryptedUsername'] + ", " + data['logins'][0]['encryptedPassword']

def readMozillaLogins(sw, profileDir):
	""" Read and parse the login file of thunderbird or firefox """
	
	print "===> Attempting to read " + sw + " login file"

	#get first default profile directory
	os.chdir(profileDir)

	#open and read profiles.ini
	profiles = open("profiles.ini", "r")
	
	for line in profiles:
		# get profile directory
		if line.startswith("Path="): 
			p = line.split("=")[1].strip("\n")
			print "Found profile directory " + p
			os.chdir(p)

			# look for signons.sqlite
			getPasswords(MOZ_LOGIN_FILE_DB) if os.path.isfile(MOZ_LOGIN_FILE_DB) else None
			
			# look for logins.json
			readLoginsJSON(MOZ_LOGIN_FILE_JSON) if os.path.isfile(MOZ_LOGIN_FILE_JSON) else None
			
			#go up one directory
			os.chdir(os.path.dirname(os.getcwd()))

### End Def

### Code

#detect os and look in specific folders
if platform.system() == "Linux":
	chromeProfile = GCHROME_PROFILE_LINUX
	ffProfile = FF_PROFILE_LINUX
	thProfile = TH_PROFILE_LINUX
elif platform.system() == "Windows":
	chromeProfile = GCHROME_PROFILE_LINUX
	ffProfile = FF_PROFILE_LINUX
	thProfile = TH_PROFILE_LINUX
	
#google-chrome
os.chdir(chromeProfile)
print "===> Attempting to read chrome login file"
getPasswords(GCHROME_LOGIN_FILE)

#firefox & thunderbird
readMozillaLogins("firefox", ffProfile)
readMozillaLogins("thunderbird", thProfile)

### End Code
