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


def recurseDir(path):
	""" Recurse into directory """
	logger.log("Scanning " + path)

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
			logger.log(fName + ": " + sig, "no")
			globalRes.append(entry)
		elif os.path.isdir(os.path.abspath(f)):
			print "\n"
			globalRes = globalRes + recurseDir(os.path.abspath(f))
	
	os.chdir(os.path.dirname(os.getcwd()))
	return globalRes


def getCloudFileHash(cloudService):
	""" Get file in the cloud service sync directory and compute the hash of each one """
	res = list()

	logger.log("===> Begin scan of " + cloudService)

	if cloudService == "Dropbox":
		if config.OP_SYS == "Linux":
			dropfolder = config.DROPBOX_LINUX
		elif config.OP_SYS == "Windows":
			dropfolder = config.DROPBOX_WIN

		# get Dropbox file folder
		cloudHome = open(dropfolder + os.sep + "host.db", "r")
		
		for line in cloudHome:
			dec = base64.b64decode(line.strip("\n"))

			if(os.path.isdir(dec)):
				res = recurseDir(dec)
				print res

	elif cloudService == "GDrive":
		conn = sqlite3.connect(config.GDRIVE + "\\sync_config.db")
		cursor = conn.cursor()
		query = "SELECT data_value FROM data WHERE entry_key = 'local_sync_root_path'"

		try:
			# select local sync path from gdrive sqlite database
			cursor.execute(query)
			cloudHome = cursor.fetchone()[0].strip("\\\\?\\")

			if(os.path.isdir(cloudHome)):
				res = recurseDir(cloudHome)
				print res
		except sqlite3.Error as e:
			logger.log(e)
		finally:
			conn.close()

	elif cloudService == "OneDrive":
		print "Microzoz"



getCloudFileHash("Dropbox")
getCloudFileHash("GDrive")
