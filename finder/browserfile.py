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
			filePath = f['path']
			fileHash = f['hash']
			logger.log("\t" + filePath+":"+fileHash,"no")

def fileCheckerCopy(profileDir, fileName, reportFolder):
	""" Check if the file exists and copy it to the report folder """

	wholePath = os.path.join(profileDir, fileName)

	if os.path.isfile(wholePath):
		dstFile = os.path.join(reportFolder, fileName)
		logger.log("Copying\n\t" + wholePath + "\n\t" + dstFile, "no")
	
		# check that the hash is the same
		hashSrc = crypto.sha256File(wholePath).hexdigest()

		shutil.copy2(wholePath, reportFolder)

		hashDst = crypto.sha256File(dstFile).hexdigest()

		# compare the source and destination file hashes
		if hashSrc == hashDst:
			logger.log("\n\t Hash are the same (" + hashSrc + ")", "no")
			return { "path": wholePath, "hash": hashSrc }
		else:
			logger.log("\n\t Hash do not coincide (" + hashSrc + " != " + hashDst + ")", "no")
			return { "path": wholePath, "hash": "<no hash>" } 
	else:
		logger.log("No " + wholePath + " found")
		return None

def chromeFinder(reportFolder):
	""" Find useful file about google chrome """
	if not os.path.isdir(config.GCHROME_PROFILE):
		logger.log("No google chrome profile folder found")

	objProfiles = list()
	chromeDict = dict()
	gchromeVersion = "Google Chrome"

	# get chrome version
	try:
		if(config.OP_SYS == "Windows"):
			gchromeVersionToParse = subprocess.check_output('reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v DisplayVersion', shell=True)
			gchromeVersion = "Google Chrome " + gchromeVersionToParse.split("\r\n")[2].split("    ")[-1]
		elif(config.OP_SYS == "Linux"):
			gchromeVersionToParse = subprocess.check_output(["which", config.GCHROME_EXEC_LINUX]).strip(" \n")
			gchromeVersion = subprocess.check_output([gchromeVersionToParse, " --version"]).strip(" \n")
	except Exception as e:
		logger.error(e)

	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + config.GCHROME_PROFILE + " <===")

	chromeUsefulList = [config.BOOKMARKS, config.GCHROME_COOKIES, config.HISTORY, config.WEB_DATA]

	profiles = [os.path.join(config.GCHROME_PROFILE,"Default")]
	profiles += glob.glob(os.path.join(config.GCHROME_PROFILE,"Profile *"))
	
	for p in profiles:
		cred = list()
		usefulFile = list()

		#profile name
		profile = os.path.basename(os.path.normpath(p))
		
		# copy file to report folder for the profile 
		reportProfile = os.path.join(reportFolder, profile)
		os.mkdir(reportProfile)
		
		logger.log("Now in " + os.path.abspath(p))
		cred = decrypter.getPasswords(os.path.join(p,config.GCHROME_LOGIN_FILE), profile)

		for f in chromeUsefulList:
			absPath = fileCheckerCopy(p, f, reportProfile) 
			
			if absPath is not None:
				usefulFile.append(absPath)	

		objProfiles.append(BrowserProfile(profile, usefulFile, cred))

	resPrinter(objProfiles)

	chromeDict["name"] = gchromeVersion
	chromeDict["profiles"] = objProfiles
	return chromeDict
	
def mozillaFinder(mozProfile, reportFolder):
	""" Find useful file about mozilla firefox / thunderbird """
	if not  os.path.isdir(mozProfile):
		logger.error("No " + mozProfile + " folder found")

	logger.log("\n", "no")
	logger.log("===> Beginning scan of " + mozProfile + " <===")

	objProfiles = list()
	browserDict = dict()

	mozUsefulList = [config.FF_COOKIES, config.PLACES, config.FORM_HISTORY]

	for profile in open(os.path.join(mozProfile,"profiles.ini"), "r"):
		cred = list()
		usefulFile = list()
		
		#get profile dir
		if profile.startswith("Path="):
			p = profile.split("=")[1].strip("\n")

			## passwords
			cred = decrypter.getPasswords(os.path.join(mozProfile,p,config.MOZ_LOGIN_FILE_DB),p)
			cred = cred + decrypter.readLoginsJSON(os.path.join(mozProfile,p,config.MOZ_LOGIN_FILE_JSON), p)

			# windows stores profiles as Profiles\...., so take only last part as profile name
			pNew = p if config.OP_SYS == "Linux" else p.split("/")[1] 
			# copy file to report folder and add to browser profile object
			reportProfile = os.path.join(reportFolder, pNew)
			os.mkdir(reportProfile)

			for f in mozUsefulList:
				absPath = fileCheckerCopy(os.path.join(mozProfile,p),f, reportProfile) 

				if absPath is not None:
					usefulFile.append(absPath)	
			
			objProfiles.append(BrowserProfile(p,usefulFile,cred))

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
