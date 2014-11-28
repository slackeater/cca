from django.conf import settings
from downloader.models import FileDownload,FileHistory, Download
import os,subprocess,magic,sys,shutil,Image,sha

ALLOWED_MIME = ("application/pdf","image/jpeg","image/png","image/gif","image/bmp")

def compareTwo(revOneID,revTwoID,diffFile,downloadFolder,token):
	
	finalDiffName = None

	#diff file full path
	diffPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,"history",diffFile.alternateName)

	#get the two file
	revOnePath = os.path.join(diffPath,diffFile.fileName+"_"+revOneID)
	revTwoPath = os.path.join(diffPath,diffFile.fileName+"_"+revTwoID)

	#check if dropbox that one of the file is not the original
	if token.serviceType == "dropbox":
		#try to get the revision from the filedownload table
		if diffFile.alternateName == revOneID:
			assumedPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,"files",diffFile.fileName+"_"+diffFile.alternateName)
			#overwrite revOnePath only if the path exists in the files folder, otherwise is in the deleted folder
			if os.path.isfile(assumedPath):
				revOnePath = assumedPath

		elif diffFile.alternateName == revTwoID:
			assumedPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,"files",diffFile.fileName+"_"+diffFile.alternateName)
			if os.path.isfile(assumedPath):
				revTwoPath = assumedPath

	#check that the two path actually exists. This because the actual file in dropbox (rightmost in the file history time line) does not exists if it has been deleted. So we will have an entry in the timeline for a version of a file that does not exist.
	if not os.path.isfile(revOnePath) or not os.path.isfile(revTwoPath):
		raise Exception("One of the two file does not exist. (Is this a deleted file on Dropbox?)")	

	#check allowed mime
	mime = magic.Magic(mime=True)
	mimeOne = mime.from_file(revOnePath)
	mimeTwo = mime.from_file(revTwoPath)

	if mimeOne not in ALLOWED_MIME or mimeTwo not in ALLOWED_MIME:
		raise Exception("Only PDF and images are supported")

	data = None
	mimeList = list()

	if mimeOne == mimeTwo == "application/pdf":
		resultDiffName = "diff_"+str(token.id)+"_"+revOneID+"_"+revTwoID+".pdf"
		diffName = pdfDiff(revOnePath,revTwoPath,diffPath,resultDiffName)
		data = {"diffName":diffName}
		mimeList.append("application/pdf")
	elif mimeOne and mimeTwo in ("image/jpeg","image/png","image/gif","image/bmp"):
		hash1,hash2 = imgDiff(revOnePath,revTwoPath)
		mimeList.append(mime.from_file(revOnePath))
		mimeList.append(mime.from_file(revTwoPath))

		#build data dictionary
		data = {'hash1': hash1,'hash2': hash2, 'file1':diffFile.fileName+"_"+revOneID,'file2':diffFile.fileName+"_"+revTwoID} 

	return {"mime": mimeList, "data": data}

def pdfDiff(pdfOne,pdfTwo,diffPath,pdfName):

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

def imgDiff(imgOne,imgTwo):

	#import crypto for hash
	cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

	if not cryptoPath in sys.path:
		sys.path.insert(1, cryptoPath)
		del cryptoPath

	import crypto

	#compute an hash of each image over the content
	hash1 = crypto.sha256File(imgOne)
	hash2 = crypto.sha256File(imgTwo)

	img1DiffPath = os.path.join(settings.DIFF_DIR,hash1+".thumbnail")
	img2DiffPath = os.path.join(settings.DIFF_DIR,hash2+".thumbnail")
	
	#copy images into cache folder
	cacheImg(imgOne,img1DiffPath)
	cacheImg(imgTwo,img2DiffPath)

	return hash1,hash2


def cacheImg(imgSrc,imgDest):
	if not os.path.isfile(imgDest):
		shutil.copy2(imgSrc,imgDest)	

		#resize images
		im = Image.open(imgDest)
		startWidth,startHeight = im.size
		newWidth,newHeight = computeThumbnailSize(startWidth, startHeight)
		im.thumbnail((newWidth,newHeight),Image.ANTIALIAS)
		im.save(imgDest,"PNG")

def computeThumbnailSize(startWidth,startHeight):
	maxHeight = float(800)
	maxWidth = float(600)
	ratio = float(0)
	newHeight = 0

	if startWidth > maxWidth:
		newWidth = (startWidth-(startWidth-maxWidth))
		ratio = float(newWidth/startWidth)
	else:
		newWidth = startWidth

	if ratio != 0:
		newHeight = startHeight-(startHeight*ratio)
	elif ratio == 0 and startHeight > maxHeight:
		newHeight = (startHeight-(startHeight-maxHeight))

	return int(newWidth),int(newHeight)
