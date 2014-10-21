#!/usr/bin/python

####
### Collect browser files to be passed to the analyzer
##
#
##
###
####

import config
import os, glob, shutil
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
		logger.log("\n-> Profile " + obj.profileName,"no")
		logger.log("Credentials", "no")
		for c in obj.credentialList:
			logger.log("\t" + c.hostname + ", " + c.username + ", " + c.password + ", " + c.profile,"no")
			logger.log("\t=>" + c.signature,"no")
			logger.log("\n", "no")
		
		logger.log("Files","no")

		for f in obj.fileListHashes:
			logger.log("\t" + f,"no")

def fileCheckerCopy(fileName, reportFolder):
	""" Check if the file exists and copy it to the report folder """

	absPath = os.path.abspath(fileName)

	if os.path.isfile(absPath):
		dstFile = os.path.join(reportFolder, fileName)
		logger.log("Copying\n\t" + absPath + "\n\t" + dstFile, "no")
	
		# check that the hash if the same
		fSrc = open(absPath)
		hashSrc = crypto.sha256File(fSrc)

		shutil.copy(absPath, os.path.join(reportFolder, fileName))

		fDst = open(dstFile)
		hashDst = crypto.sha256File(fDst)

		# compare the source and destination file hashes
		if hashSrc == hashDst:
			logger.log("\n\t Hash are the same (" + hashSrc + ")", "no")
			absPath = absPath + ":" + hashSrc
			return absPath
		else:
			logger.log("\n\t Hash do not coincide (" + hashSrc + " != " + hashDst + ")", "no")
			absPath = absPath + ":<no hash>"
			return absPath

	else:
		logger.log("No " + absPath + " found")
		return None

def chromeFinder(reportFolder):
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
		except Exception as e:
			logger.error(e)
	elif(config.OP_SYS == "Linux"):
		try:
			gchromePath = subprocess.check_output(["which", config.GCHROME_EXEC_LINUX]).strip(" \n")
			gchromeVersion = subprocess.check_output([gchromePath, " --version"]).strip(" \n")
		except Exception as e:
			logger.error(e)

	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + config.GCHROME_PROFILE + " <===")

	chromeUsefulList = list()
	chromeUsefulList.append(config.BOOKMARKS)
	chromeUsefulList.append(config.GCHROME_COOKIES)
	chromeUsefulList.append(config.HISTORY)
	chromeUsefulList.append(config.WEB_DATA)

	#look in default profile
	if os.path.isdir("Default"):
		cred = list()
		usefulFile = list()
		os.chdir("Default")
		cred = decrypter.getPasswords(config.GCHROME_LOGIN_FILE, "Default")

		# copy file to report folder and add to browser profile object
		reportProfile = os.path.join(reportFolder, "Default")
		os.mkdir(reportProfile)

		for f in chromeUsefulList:
			absPath = fileCheckerCopy(f, reportProfile) 
			
			if absPath is not None:
				usefulFile.append(absPath)	

		objProfiles.append(BrowserProfile("Default", usefulFile, cred))

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	profiles = glob.glob("Profile *")

	for profile in profiles:
		cred = list()
		usefulFile = list()
		os.chdir(profile)
		cred = decrypter.getPasswords(config.GCHROME_LOGIN_FILE, profile)
		
		# copy file to report folder and add to browser profile object
		reportProfile = os.path.join(reportFolder, profile)
		os.mkdir(reportProfile)

		for f in chromeUsefulList:
			absPath = fileCheckerCopy(f, reportProfile) 
			
			if absPath is not None:
				usefulFile.append(absPath)	

		objProfiles.append(BrowserProfile(profile, usefulFile, cred))

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	resPrinter(objProfiles)

	chromeDict["name"] = gchromeVersion
	chromeDict["profiles"] = objProfiles
	return chromeDict
	
def mozillaFinder(mozProfile, reportFolder):
	""" Find useful file about mozilla firefox / thunderbird """
	if not  os.path.isdir(mozProfile):
		logger.error("No " + mozProfile + " folder found")

	# look in all profiles
	os.chdir(mozProfile)
	
	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + mozProfile + " <===")

	objProfiles = list()
	browserDict = dict()

	mozUsefulList = list()
	mozUsefulList.append(config.FF_COOKIES)
	mozUsefulList.append(config.PLACES)
	mozUsefulList.append(config.FORM_HISTORY)

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

			# copy file to report folder and add to browser profile object
			reportProfile = os.path.join(reportFolder, p)
			os.mkdir(reportProfile)

			for f in mozUsefulList:
				absPath = fileCheckerCopy(f, reportProfile) 

				if absPath is not None:
					usefulFile.append(absPath)	
			
			objProfiles.append(BrowserProfile(p,usefulFile,cred))

			os.chdir(os.path.dirname(os.getcwd()))
			cred = list()
			usefulFile = list()

	browserDict["profiles"] = objProfiles
	return browserDict


def thunderbirdFinder(reportFolder):
	""" Thudnerbird wrapper for mozillaFinder """
	res = mozillaFinder(config.TH_PROFILE, reportFolder)
	res['name'] = mozillaVersionFinder("thunderbird")
	resPrinter(res["profiles"])
	return res

def firefoxFinder(reportFolder):
	""" Firefox wrapper for mozillaFinder """
	res = mozillaFinder(config.FF_PROFILE, reportFolder)
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
		mozPath = subprocess.check_output(["which", sw]).strip(" \n")
		mozVersionToParse = subprocess.check_output([mozPath, "--version"]).strip(" \n")
		return mozVersionToParse

	return mozVersion
