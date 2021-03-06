from django.conf import settings
from downloader.models import FileDownload,FileHistory, Download, FileMetadata
from clouditem.models import CloudItem
import os,subprocess,magic,sys,shutil,Image,base64
from django.utils.dateformat import format
from webapp.thumbnailer import Thubmnailer
from webapp import constConfig
from webapp.func import openReport
from webapp import crypto

class Comparator(object):
	""" This class is used to perform file comparison """

	def __init__(self,token):
		self.t = token

        def displaySingle(self,title,altName,downAltName,fileFolder):
            """ Display a single file """ 
            
            if fileFolder == "file" or altName == downAltName:
                f = constConfig.DOWNLOAD_FILES_FOLDER
            elif fileFolder == "history":
                f = os.path.join(constConfig.DOWNLOAD_HISTORY_FOLDER,downAltName)
            
            name = crypto.sha256(title+crypto.HASH_SEPARATOR+altName).hexdigest() + "_" + altName
            downloadFolder = Download.objects.get(tokenID=self.t,threadStatus = constConfig.THREAD_TS).folder
            fullPath = os.path.join(settings.DOWNLOAD_DIR, downloadFolder,f,name)
            
            print os.path.isfile(fullPath)
            print fullPath

            mime = magic.Magic(mime=True)
            mimeType = mime.from_file(fullPath)

            if mimeType in constConfig.ALLOWED_MIME_TYPE[1:-1]:
                t = Thubmnailer()
                t.cacheImg(fullPath,os.path.join(settings.DIFF_DIR,name+".thumbnail"))
                return {'name': name,'mime':mimeType}
            elif mimeType == constConfig.ALLOWED_MIME_TYPE[0]:
                dest = os.path.join(settings.DIFF_DIR,name)
               
                if not os.path.isfile(dest):
                    shutil.copy(fullPath, dest)

                return {'name': name, 'mime':constConfig.ALLOWED_MIME_TYPE[0]}

	def compareTwo(self,revOneID,revTwoID,altName):
		""" Compare two revision of the same file and check for diff """
			
		finalDiffName = None
		downloadFolder = Download.objects.get(tokenID=self.t,threadStatus = constConfig.THREAD_TS).folder
		diffFile = FileDownload.objects.get(tokenID=self.t,alternateName=altName)

		#diff file full path
		diffPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,constConfig.DOWNLOAD_HISTORY_FOLDER,diffFile.alternateName)

		#get the two file
		nameOne = crypto.sha256(diffFile.fileName+crypto.HASH_SEPARATOR+revOneID).hexdigest()
		nameTwo = crypto.sha256(diffFile.fileName+crypto.HASH_SEPARATOR+revTwoID).hexdigest()
		revOnePath = os.path.join(diffPath,nameOne+"_"+revOneID)
		revTwoPath = os.path.join(diffPath,nameTwo+"_"+revTwoID)
		
		#check if dropbox that one of the file is not the original
		if self.t.serviceType == constConfig.CSP_DROPBOX:
			#try to get the revision from the filedownload table
			if diffFile.alternateName == revOneID:
				assumeNameOne = crypto.sha256(diffFile.fileName+crypto.HASH_SEPARATOR+diffFile.alternateName).hexdigest()
				assumedPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,constConfig.DOWNLOAD_FILES_FOLDER,assumeNameOne+"_"+diffFile.alternateName)
				#overwrite revOnePath only if the path exists in the files folder, otherwise is in the deleted folder
				if os.path.isfile(assumedPath):
					revOnePath = assumedPath

			elif diffFile.alternateName == revTwoID:
				assumeNameTwo = crypto.sha256(diffFile.fileName+crypto.HASH_SEPARATOR+diffFile.alternateName).hexdigest()
				assumedPath = os.path.join(settings.DOWNLOAD_DIR,downloadFolder,constConfig.DOWNLOAD_FILES_FOLDER,assumeNameTwo+"_"+diffFile.alternateName)
				if os.path.isfile(assumedPath):
					revTwoPath = assumedPath

		#check that the two path actually exists. This because the actual file in dropbox (rightmost in the file history time line) does not exists if it has been deleted. So we will have an entry in the timeline for a version of a file that does not exist.
		if not os.path.isfile(revOnePath) or not os.path.isfile(revTwoPath):
			raise Exception("One of the two file does not exist. (Is this a deleted file on Dropbox?)")	
                
                print revOnePath
                print revTwoPath

		#check allowed mime
		mime = magic.Magic(mime=True)
		mimeOne = mime.from_file(revOnePath)
		mimeTwo = mime.from_file(revTwoPath)

		if mimeOne not in constConfig.ALLOWED_MIME_TYPE or mimeTwo not in constConfig.ALLOWED_MIME_TYPE:
			raise Exception("File type not supported")

		data = None
		mimeList = list()
	
		#pdf files
		if mimeOne == mimeTwo == constConfig.ALLOWED_MIME_TYPE[0]:
			resultDiffName = "diff_"+str(self.t.id)+"_"+revOneID+"_"+revTwoID+".pdf"
			diffName = self.pdfDiff(revOnePath,revTwoPath,diffPath,resultDiffName)
			data = {"diffName":diffName}
			mimeList.append(constConfig.ALLOWED_MIME_TYPE[0])
		#images 	
		elif mimeOne and mimeTwo in constConfig.ALLOWED_MIME_TYPE[1:-1]:
			hash1,hash2 = self.imgDiff(revOnePath,revTwoPath)
			mimeList.append(mime.from_file(revOnePath))
			mimeList.append(mime.from_file(revTwoPath))

			#build data dictionary
			data = {'hash1': hash1,'hash2': hash2, 'file1':diffFile.fileName+"_"+revOneID,'file2':diffFile.fileName+"_"+revTwoID} 

		return {"filename": diffFile.fileName,"mime": mimeList, "data": data}


	def pdfDiff(self,pdfOne,pdfTwo,diffPath,pdfName):
		""" Perform the diff of two PDF """

		resultDiffPath = os.path.join(settings.DIFF_DIR,pdfName)

		#check if a diff already exists for this file
		if os.path.isfile(resultDiffPath):
			return pdfName

		#generate diff
		try:
			subprocess.check_output(["diff-pdf","--output-diff="+resultDiffPath+"",pdfOne,pdfTwo],stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			#necessary because diff-pdf always exits with 1, because of the message "No protocol specified" caused by the absence of the server X, even though the diff is generated
                        print e
			if e.output.strip() != "":
				raise Exception("Error computing diff of PDF")

		return pdfName

	def imgDiff(self,imgOne,imgTwo):
		""" Perform the diff of two images """

		thumb = Thubmnailer()
		hashes = list()

		#compute an hash of each image over the content
		for img in [imgOne,imgTwo]:
			hashImg = crypto.sha256File(img).hexdigest()
			imgDiffPath = os.path.join(settings.DIFF_DIR,hashImg+".thumbnail")
			
			#copy images into cache folder
			thumb.cacheImg(img,imgDiffPath)

			hashes.append(hashImg)

		return hashes[0],hashes[1]

	def compareFromReport(self):
		""" Compare the file found in the report with the ones downloaded """

		res = list()

		#get the report
		report = openReport(self.t.cloudItem)

		if report is not None:
			cloudFiles = report[2]['objects']
			
			if cloudFiles is not None:
			
				#compute the hash of the downloaded files:
				#get the files of the token
				files = FileDownload.objects.filter(tokenID=self.t)
				downFolder = Download.objects.get(tokenID=self.t).folder

				for f in files:
					localRes = list()
					fileName = crypto.sha256(f.fileName+crypto.HASH_SEPARATOR+f.alternateName).hexdigest()
					basePath = os.path.join(settings.DOWNLOAD_DIR,downFolder,"files")
					fullPath = os.path.join(basePath,fileName+"_"+f.alternateName)

					if os.path.isfile(fullPath):

						fileDigest = crypto.sha256File(fullPath).hexdigest()
						
						for cloud in cloudFiles:
							#check if the CSP of the token is in the report
							if self.t.serviceType in cloud['cloudService'].lower():

								#now check if in the report we have the same file
								for cloudFile in cloud['files']:
									
									if cloudFile['hash'] == fileDigest:
										localRes.append({'csp':cloud['cloudService'],'files':cloudFile})				
						res.append({'file':f,'comparableFiles':localRes})

		return res
