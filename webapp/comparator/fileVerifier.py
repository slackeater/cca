import os,sys
from webapp.func import *
from webapp import constConfig
from webapp import crypto
from downloader.verifier import DTAVerifier
import binascii
from webapp.databaseInterface import DbInterface
from django.conf import settings

class Verifier(object):
	""" This class is used to perform verification on file and metadata """

	def __init__(self,token):
		self.t = token
		self.d = Download.objects.get(tokenID=self.t)
		
		baseDir = os.path.join(settings.DOWNLOAD_DIR,self.d.folder)
		self.historyFolder = os.path.join(baseDir,"history")
		self.filesFolder = os.path.join(baseDir,"files")
		
	def verifyFileDownload(self,resType):
		""" Verify the files of a token """

		hList = list()
		downloadFolder = self.d.folder

		for f in FileDownload.objects.filter(tokenID=self.t):
			hashName = crypto.sha256(f.fileName+crypto.HASH_SEPARATOR+f.alternateName).hexdigest()
			path = os.path.join(self.filesFolder,hashName+"_"+f.alternateName)
			isFile = os.path.isfile(path)

			if isFile:
				#first compute the hash
				h = crypto.sha256File(path)

				#now verify the hash
				sourceSignature = f.fileHash

				verification = crypto.verifyRSAsignatureSHA256(h,sourceSignature,settings.PUB_KEY)

				#history only if specified
				if resType == constConfig.VERIFY_CHOICE_FILESHISTORY:
					historyVerification = self.verifyHistory(f)
				else:
					historyVerification = None

				hList.append({'fID': f.id,'fName':f.fileName,'fSig':crypto.sha256(f.fileHash).hexdigest(),'verificationResult':verification,'history':historyVerification})
			elif not isFile:
				hList.append({'fID': f.id,'fName':f.fileName,'fSig':"File does not exists on disk",'verificationResult':-1,'history': list()})

		return hList

	def verifyMetadata(self):
		""" Verifiy the file metadata """

		hList = list()
		meta = FileMetadata.objects.get(tokenID=self.t)

		metaFile = meta.metadata
		mTime = getTimestamp(meta.metaTime)

		#compute hash
		h = crypto.sha256(metaFile+crypto.HASH_SEPARATOR+mTime)

		#verify
		verification = crypto.verifyRSAsignatureSHA256(h,meta.metadataHash,settings.PUB_KEY)

		sig = crypto.rsaSignatureSHA256(metaFile+crypto.HASH_SEPARATOR+mTime,settings.PRIV_KEY)

		#metadata hash
		mSig = crypto.sha256(meta.metadataHash).hexdigest()

		return ({'metaID': meta.id,'verificationResult': verification,'mSig':mSig})

	def verifyHistory(self,fileDownload):
		""" Verify file history """

		hList = list()

		for fh in FileHistory.objects.filter(fileDownloadID=fileDownload):
			#verification of revision metadata
			revMeta = fh.revisionMetadata
			revDownTime = getTimestamp(fh.downloadTime)
			h = crypto.sha256(revMeta+crypto.HASH_SEPARATOR+revDownTime)
			verification = crypto.verifyRSAsignatureSHA256(h,fh.revisionMetadataHash,settings.PUB_KEY)

			hashName = crypto.sha256(fileDownload.fileName+crypto.HASH_SEPARATOR+fh.revision).hexdigest()
			path = os.path.join(self.historyFolder,fileDownload.alternateName,hashName+"_"+fh.revision)

			isPath = os.path.isfile(path)

			if isPath:
				#verification of file history 
				fHash = crypto.sha256File(path)
				verificationFile = crypto.verifyRSAsignatureSHA256(fHash,fh.fileRevisionHash,settings.PUB_KEY)

				hList.append({'hID': fh.id,'revID':fh.revision,'metadataVerificationResult': verification,'fileVerificationResult':verificationFile})
			else:
				hList.append({'hID': fh.id,'revID':fh.revision,'metadataVerificationResult': verification,'fileVerificationResult':"File does not exists on disk"})

		return hList
	
	def verifyZIP(self):
		""" Verify the signature and the digital timestamp """
		
		d = DbInterface.getDownload(self.t)
		folderName = d.folder

		#path of signature files
		request = os.path.join(settings.VERIFIED_ZIP,folderName+constConfig.EXTENSION_REQUEST)
		signature = os.path.join(settings.VERIFIED_ZIP,folderName+constConfig.EXTENSION_SIGNATURE)
		zipData = os.path.join(settings.VERIFIED_ZIP,folderName+constConfig.EXTENSION_ZIP)

		zipHash = d.verificationZIPSignatureHash
		zipHashBase64 = binascii.b2a_base64(binascii.unhexlify(zipHash))
		signatureDownloadPath = "/verSign/" + folderName + constConfig.EXTENSION_SIGNATURE				

		if os.path.isfile(request) and os.path.isfile(signature):
			dtaVer = DTAVerifier(None)
			res = dtaVer.verifyTimestamp(request,signature)
			return {'res':res,'zipHashBase64':zipHashBase64,'zipHash':zipHash,'downLink': signatureDownloadPath ,'reqName': folderName+constConfig.EXTENSION_REQUEST,'sigName':folderName+constConfig.EXTENSION_SIGNATURE}
