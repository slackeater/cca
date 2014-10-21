#!/usr/bin/python


####
### Main script
##
#
##
###
####

import cloud, browserfile, config, packetizer, crypto, logger, getpass
import os, subprocess, time, json, zipfile

def main():

	# report name and path
	reportName = crypto.md5(str(time.time()))
	completeReportPath = os.path.join(config.START_PATH, reportName)
	
	# create directory used for report files
	os.mkdir(completeReportPath)

	# find passwords and browser files
	chromeReportFolder = os.path.join(completeReportPath, config.GCHROME_COPY_FOLDER)
	os.mkdir(chromeReportFolder)
	chrome = browserfile.chromeFinder(chromeReportFolder)

	ffReportFolder = os.path.join(completeReportPath, config.FF_COPY_FOLDER)
	os.mkdir(ffReportFolder)
	ffList = browserfile.firefoxFinder(ffReportFolder)

	thReportFolder = os.path.join(completeReportPath, config.TH_COPY_FOLDER)
	os.mkdir(thReportFolder)
	thList = browserfile.thunderbirdFinder(thReportFolder)

	browserPackList = list()
	browserPackList.append(chrome)
	browserPackList.append(ffList)
	browserPackList.append(thList)

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
	jsontext = packetizer.mainPacker(browserPackList, cloudPackList)
	logger.log(jsontext, "no")

	crypt = crypto.makeReport(crypto.encryptAES(jsontext))
	
	# save into a file
	os.chdir(completeReportPath)
	fileName = reportName + ".report"
	f = open(fileName,"w+")
	f.write(json.dumps(crypt, sort_keys=True, indent=4))
	f.close()

	
	# change to start directory if not already in it	
	if os.getcwd() != config.START_PATH:
		os.chdir(config.START_PATH)
	
	# create  ZIP 
	zipFile = zipfile.ZipFile(reportName + ".zip", "w")

	for dirname, subdirs, files in os.walk(reportName):
		zipFile.write(dirname)

		for filename in files:
			zipFile.write(os.path.join(dirname, filename))
	
	zipFile.close()
		
	logger.log("Report file written to " + os.path.join(config.START_PATH,reportName + ".zip"))
	
	
	# hmac signature of zip
	pa = getpass.getpass("Password:")
	
	hmacDigest = crypto.sha256File(open(os.path.join(config.START_PATH,reportName + ".zip")), pa)
	hmacFile = open(os.path.join(config.START_PATH, reportName + ".zip.sig"), "w+")
	hmacFile.write(hmacDigest)
	hmacFile.close()

	# uncomment for final version
	#os.rmdir(completeReportPath)

if __name__ == "__main__":
	main()
