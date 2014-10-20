#!/usr/bin/python

####
### Collect browser files to be passed to the analyzer
##
#
##
###
####

import config
import os, glob
import decrypter, logger, crypto, subprocess
from credentials import Credentials
from profilebrowser import BrowserProfile

#detect os and set profile folders
if config.OP_SYS == "Linux":
	ffProfile = config.FF_PROFILE_LINUX
	thProfile = config.TH_PROFILE_LINUX
elif config.OP_SYS == "Windows":
	ffProfile = config.FF_PROFILE_WIN
	thProfile = config.TH_PROFILE_WIN

def resPrinter(profileObjects):
	""" Print in a readable manner the results """ 

	for obj in profileObjects: 
		logger.log("-> Profile " + obj.profileName,"no")
		logger.log("Credentials", "no")
		for c in obj.credentialList:
			logger.log("\t" + c.hostname + ", " + c.username + ", " + c.password + ", " + c.profile,"no")
			logger.log("\t=>" + c.signature,"no")
			logger.log("\n", "no")
		
		logger.log("Files","no")

		for f in obj.fileListHashes:
			logger.log("\t" + f,"no")

def chromeFinder():
	""" Find useful file about google chrome """
	if not os.path.isdir(config.GCHROME_PROFILE):
		logger.log("No google chrome profile folder found")

	objProfiles = list()

	os.chdir(config.GCHROME_PROFILE)
	chromeDict = dict()
	gchromeVersion = "Google Chrome"

	# get chrome version
	if(config.OP_SYS == "Windows"):
		try:
			gchromeVersionToParse = subprocess.check_output('reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v DisplayVersion', shell=True)
			gchromeVersion = "Google Chrome " + gchromeVersionToParse.split("\r\n")[2].split("    ")[-1]
		except Error as e:
			logger.error(e)
	elif(config.OP_SYS == "Linux"):
		try:
			gchromePath = subprocess.check_output(["which", "google-chrome-stable"]).strip(" \n")
			gchromeVersion = subprocess.check_output([gchromePath, " --version"]).strip(" \n")
		except Error as e:
			logger.error(e)

	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + config.GCHROME_PROFILE + " <===")

	#look in default profile
	if os.path.isdir("Default"):
		cred = list()
		usefulFile = list()
		os.chdir("Default")
		cred = decrypter.getPasswords(config.GCHROME_LOGIN_FILE, "Default")

		if os.path.isfile(config.BOOKMARKS):
			usefulFile.append(os.path.abspath(config.BOOKMARKS))
		
		if os.path.isfile(config.GCHROME_COOKIES):
			usefulFile.append(os.path.abspath(config.GCHROME_COOKIES))

		if os.path.isfile(config.HISTORY):
			usefulFile.append(os.path.abspath(config.HISTORY))

		if os.path.isfile(config.WEB_DATA):
			usefulFile.append(os.path.abspath(config.WEB_DATA))

		objProfiles.append(BrowserProfile("Default", usefulFile, cred))

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	profiles = glob.glob("Profile *")

	for profile in profiles:
		cred = list()
		usefulFile = list()
		os.chdir(profile)
		cred = decrypter.getPasswords(config.GCHROME_LOGIN_FILE, profile)

		if os.path.isfile(config.BOOKMARKS):
			usefulFile.append(os.path.abspath(config.BOOKMARKS))
		
		if os.path.isfile(config.GCHROME_COOKIES):
			usefulFile.append(os.path.abspath(config.GCHROME_COOKIES))

		if os.path.isfile(config.HISTORY):
			usefulFile.append(os.path.abspath(config.HISTORY))

		if os.path.isfile(config.WEB_DATA):
			usefulFile.append(os.path.abspath(config.WEB_DATA))

		objProfiles.append(BrowserProfile(profile, usefulFile, cred))

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	resPrinter(objProfiles)

	chromeDict["name"] = gchromeVersion
	chromeDict["profiles"] = objProfiles
	return chromeDict
	
def mozillaFinder(mozProfile):
	""" Find useful file about mozilla firefox / thunderbird """
	if not  os.path.isdir(mozProfile):
		logger.error("No " + mozProfile + " folder found")

	# look in all profiles
	os.chdir(mozProfile)
	
	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + mozProfile + " <===")

	objProfiles = list()
	browserDict = dict()

	for profile in open("profiles.ini", "r"):
		cred = list()
		usefulFile = list()
		#get profile dir
		if profile.startswith("Path="):
			p = profile.split("=")[1].strip("\n")
			os.chdir(p)

			## passwords
			cred = decrypter.getPasswords(config.MOZ_LOGIN_FILE_DB,p)
			cred = cred + decrypter.readLoginsJSON(config.MOZ_LOGIN_FILE_JSON, p)

			##useful file
			if os.path.isfile(config.FF_COOKIES):
				usefulFile.append(os.path.abspath(config.FF_COOKIES))

			if os.path.isfile(config.PLACES):
				usefulFile.append(os.path.abspath(config.PLACES))

			if os.path.isfile(config.FORM_HISTORY):
				usefulFile.append(os.path.abspath(config.FORM_HISTORY))
			
			objProfiles.append(BrowserProfile(p,usefulFile,cred))

			os.chdir(os.path.dirname(os.getcwd()))
			cred = list()
			usefulFile = list()

	browserDict["profiles"] = objProfiles
	return browserDict


def thunderbirdFinder():
	""" Thudnerbird wrapper for mozillaFinder """
	res = mozillaFinder(config.TH_PROFILE)
	res['name'] = mozillaVersionFinder("thunderbird")
	resPrinter(res["profiles"])
	return res

def firefoxFinder():
	""" Firefox wrapper for mozillaFinder """
	res = mozillaFinder(config.FF_PROFILE)
	res['name'] = mozillaVersionFinder("firefox")
	resPrinter(res["profiles"])
	return res

def mozillaVersionFinder(sw):
	""" Find the version of either firefox or thunderbird """

	swName = "Mozilla Firefox" if sw == "firefox" else "Mozilla Thunderbird"
	mozVersion = swName

	if config.OP_SYS == "Windows":
		mozVersionToParse = subprocess.check_output("reg query \"HKEY_LOCAL_MACHINE\Software\Mozilla\\" + swName +"\" /v CurrentVersion", shell=True)
		mozVersion = mozVersion + " " + mozVersionToParse.split("\r\n")[2].split("    ")[-1]
		return mozVersion
	elif config.OP_SYS == "Linux":
		mozPath = subprocess.check_output(["/usr/bin/which", sw]).strip(" \n")
		mozVersionToParse = subprocess.check_output([mozPath, "--version"]).strip(" \n")
		return mozVersionToParse

	return mozVersion
