#!/usr/bin/python

####
### Pack the results using JSON
##
#
##
###
####

import json
from profilebrowser import BrowserProfileEncoder

def browserPack(browserDict):
	""" Encode the list of file for a browser into JSON """

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

