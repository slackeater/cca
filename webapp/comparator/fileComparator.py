from django.conf import settings
from downloader.models import FileDownload,FileHistory, Download
import os,subprocess

def compareTwo(revOneID,revTwoID,diffFile,downloadFolder,token):

	#diff file full path
	diffPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,"history",diffFile.alternateName)

	#get the two file
	revOnePath = os.path.join(diffPath,diffFile.fileName+"_"+revOneID)
	revTwoPath = os.path.join(diffPath,diffFile.fileName+"_"+revTwoID)

	#diff name
	resultDiffName = "diff_"+str(token.id)+"_"+revOneID+"_"+revTwoID+".pdf"
	
	resultDiffPath = os.path.join(settings.DIFF_DIR,resultDiffName)

	#check if a diff already exists for this file
	if os.path.isfile(resultDiffPath):
		return resultDiffName

	#generate diff
	try:
		subprocess.check_output(["diff-pdf","--output-diff="+resultDiffPath+"",revOnePath,revTwoPath],stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		#necessary because diff-pdf always exits with 1, because of the message "No protocol specified" caused by the absence of the server X, even though the diff is generated
		if e.output.strip() != "No protocol specified":
			raise Exception("Error computing diff of PDF")
	
	return resultDiffName	

