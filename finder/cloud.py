#!/usr/bin/python

####
###
## Finds cloud services installed and get a signature of shared files
# 
##
###
####


import config, crypto, logger
import os, base64, sqlite3
import xml.etree.ElementTree as ET

def recurseDir(path):
	""" Recurse into directory """
	logger.log("Scanning " + path, "no")

	if type(path) is str:
		path = unicode(path)

	os.chdir(path)
	files = os.listdir(path)
	globalRes = list()

	for f in files:
		if os.path.isfile(f):
			sig = crypto.sha256File(open(f, "r"))
			fName = os.path.abspath(f).encode("UTF-8")
			entry = {fName:sig}
			logger.log("\t" + f.encode("UTF-8") + ": " + sig, "no")
			globalRes.append(entry)
		elif os.path.isdir(os.path.abspath(f)):
			globalRes = globalRes + recurseDir(os.path.abspath(f))

	os.chdir(os.path.dirname(os.getcwd()))
	return globalRes


def getCloudFileHash(cloudService):
	""" Get file in the cloud service sync directory and compute the hash of each one """
	res = list()

	logger.log("\n", "no")
	logger.log("===> Begin scan of " + cloudService + "<===")

	if cloudService == "Dropbox":
		# get Dropbox file folder
		cloudHome = open(os.path.join(config.DROPBOX,"host.db"), "r")
		
		for line in cloudHome:
			dec = base64.b64decode(line.strip("\n"))

			if(os.path.isdir(dec)):
				res = recurseDir(dec)
				return res

	elif cloudService == "GDrive":
		conn = sqlite3.connect(os.path.join(config.GDRIVE,"sync_config.db"))
		cursor = conn.cursor()
		query = "SELECT data_value FROM data WHERE entry_key = 'local_sync_root_path'"

		try:
			# select local sync path from gdrive sqlite database
			cursor.execute(query)
			# strange charaters are placed in fron of the path, strip them
			cloudHome = cursor.fetchone()[0].strip("\\\\?\\")

			if(os.path.isdir(cloudHome)):
				res = recurseDir(cloudHome)
				return res
		except sqlite3.Error as e:
			logger.log(e)
		finally:
			conn.close()

	elif cloudService == "OneDrive":
		#parse XML with configuration
		tree = ET.parse(os.path.join(config.ONEDRIVE,"settings","ApplicationSettings.xml"))
		root = tree.getroot()
		cloudHome = ""

		# find user id
		for setting in root[0][0].findall("setting"):
			if setting.attrib['name'] == "UserCid":
				userCid = setting[0].text

		# open file with onedrive path
		userConf = open(os.path.join(config.ONEDRIVE,"settings",userCid+".ini"),"r").read()

		# file is utf-16 encoded
		for l in userConf.decode("utf-16").split("\r\n"):
			if l.startswith("library"):
				# get the path in the string
				oneDrivePath = l.strip().split(" ")[-1]
				cloudHome = oneDrivePath[1:-1]
		
		if(os.path.isdir(cloudHome)):
			res = recurseDir(cloudHome)
			return res

def dropbox():
	""" Wrapper for Dropbox """
	if(os.path.isdir(config.DROPBOX)):
		dropDict = dict()
		dropDict["cloudSerivce"] = "Dropbox"
		dropDict["files"] = getCloudFileHash("Dropbox")
		return dropDict
	else:
		logger.error("No Google Drive directory found")

def gdrive():
	""" Wrapper for Google Drive """
	if(os.path.isdir(config.GDRIVE)):
		gdriveDict = dict()
		gdriveDict["cloudService"] = "Google Drive"
		gdriveDict["files"] = getCloudFileHash("GDrive")
		return gdriveDict
	else:
		logger.error("No Google Drive directory found")

def onedrive():
	""" Wrapper for OneDrive """
	if(os.path.isdir(config.ONEDRIVE)):
		onedriveDict = dict()
		onedriveDict["cloudService"] = "One Drive"
		onedriveDict["files"] = getCloudFileHash("OneDrive")
		return onedriveDict
	else:
		logger.error("No OneDrive directory found")
