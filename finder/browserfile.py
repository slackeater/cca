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
import decrypter, logger
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
	return objProfiles
	
def mozillaFinder(mozProfile):
	""" Find useful file about firefox """
	if not  os.path.isdir(mozProfile):
		logger.error("No " + mozProfile + " folder found")

	# look in all profiles
	os.chdir(mozProfile)
	
	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + mozProfile + " <===")

	objProfiles = list()

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
	
	return objProfiles


def thunderbirdFinder():
	""" Thudnerbird wrapper for mozillaFinder """
	res = mozillaFinder(config.TH_PROFILE)
	resPrinter(res)
	return res

def firefoxFinder():
	""" Firefox wrapper for mozillaFinder """
	res = mozillaFinder(config.FF_PROFILE)
	resPrinter(res)
	return res
