#!/usr/bin/python

####
### Pack the results using JSON
##
#
##
###
####

import json, crypto, platform
import time
from profilebrowser import BrowserProfileEncoder

def browserPack(browserDict):
	""" Encode the list of file for a browser into a dictionary """

	jsonProfile = ""
	browserNewDict = dict()
	profileEnc = list()

	for profile in browserDict["profiles"]:
		benc = BrowserProfileEncoder()
		profileEnc.append(benc.default(profile))

	browserNewDict["name"] = browserDict['name']
	browserNewDict["profiles"] = profileEnc
	return browserNewDict

def browserContainer(packedBrowsersList):
	""" Put all the browser found together """

	mainPack = dict()
	mainPack["category"] = "Browser"
	mainPack["objects"] = packedBrowsersList

	return json.dumps(mainPack, sort_keys=True, indent=4)

def cloudContainer(packedCloudList):
	""" Encode the list of file for a cloud service into JSON """

	mainPack = dict()
	mainPack["category"] = "Cloud"
	mainPack["objects"] = packedCloudList

	return json.dumps(mainPack, sort_keys=True, indent=4)

def headerPacker():
	""" Create the header of the JSON with some useful information """
	
	reportTime = (time.ctime())
	machineInfo = platform.uname()
	reportID = crypto.md5(str(time.time()))

	infoDict = dict()
	infoDict["id"] = reportID
	infoDict["info"] = machineInfo
	infoDict["time"] = reportTime
	
	mainPack = dict()
	mainPack["category"] = "attributes"
	mainPack["objects"] = infoDict

	return json.dumps(mainPack, sort_keys=True, indent=4)

def mainPacker(browserList, cloudList):
	jsonFile = "[\n"

	jsonFile += headerPacker()+","

	# encode each dictionary of each browser
	packedBrowsersList = list()

	for b in browserList:
		packedBrowsersList.append(browserPack(b))

	# JSONify browser results
	jsonFile += browserContainer(packedBrowsersList)+","

	# JSONify cloud result
	jsonFile += cloudContainer(cloudList)

	jsonFile += "\n]"

	return jsonFile
