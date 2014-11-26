from django.conf import settings
from downloader.models import FileDownload,FileHistory, Download
import os,subprocess,magic

def compareTwo(revOneID,revTwoID,diffFile,downloadFolder,token):

	finalDiffName = None

	#diff file full path
	diffPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,"history",diffFile.alternateName)

	#get the two file
	revOnePath = os.path.join(diffPath,diffFile.fileName+"_"+revOneID)
	revTwoPath = os.path.join(diffPath,diffFile.fileName+"_"+revTwoID)

	#diff name without extension, this will be determined by the mime type
	resultDiffName = "diff_"+str(token.id)+"_"+revOneID+"_"+revTwoID

	mime = magic.Magic(mime=True)

	if mime.from_file(revOnePath) == mime.from_file(revTwoPath) == "application/pdf":
		finalDiffName = pdfDiff(revOnePath,revTwoPath,diffPath,resultDiffName)

	return finalDiffName	

def pdfDiff(pdfOne,pdfTwo,diffPath,diffName):

	pdfName = diffName + ".pdf"

	resultDiffPath = os.path.join(settings.DIFF_DIR,pdfName)

	#check if a diff already exists for this file
	if os.path.isfile(resultDiffPath):
		return pdfName

	#generate diff
	try:
		subprocess.check_output(["diff-pdf","--output-diff="+resultDiffPath+"",pdfOne,pdfTwo],stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		#necessary because diff-pdf always exits with 1, because of the message "No protocol specified" caused by the absence of the server X, even though the diff is generated
		if e.output.strip() != "No protocol specified":
			raise Exception("Error computing diff of PDF")

	return pdfName
	
