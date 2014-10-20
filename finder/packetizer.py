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

def browserPack(browserDict, browserName):
	""" Encode the list of file for a browser into JSON """

	jsonProfile = ""
	browserNewDict = dict()
	profileEnc = list()

	for profile in browserDict["profiles"]:
		benc = BrowserProfileEncoder()
		profileEnc.append(benc.default(profile))

	browserNewDict["name"] = browserDict['name']
	browserNewDict["profiles"] = profileEnc
	print json.dumps(browserNewDict, sort_keys=True, indent=4)

