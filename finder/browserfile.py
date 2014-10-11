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

GCHROME_PROFILE_WIN = r'C:\Users\\" + UNAME + "\AppData\Local\Google\Chrome\User Data'
FF_PROFILE_WIN = r'C:\Users\\" + UNAME + "\AppData\Roaming\Mozilla\Firefox'
TH_PROFILE_WIN = r'C:\Users\\" + UNAME + "\AppData\Roaming\Thunderbird'
LIBNSS_WIN = "nss3.dll"

GCHROME_PROFILE_LINUX = "/home/" + UNAME + "/.config/google-chrome"
FF_PROFILE_LINUX = "/home/" + UNAME + "/.mozilla/firefox"
TH_PROFILE_LINUX = "/home/" + UNAME + "/.thunderbird"
LIBNSS_LINUX = "libnss3.so"

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
	
	ffCred = decrypter.readMozillaLogins("firefox",ffProfile, libnss)

	logger.log("\n === Credentials for firefox found: === ","no")

	for c in ffCred:
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
