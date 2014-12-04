from django.conf import settings
import os,zipfile,sys,base64,binascii,subprocess
from subprocess import Popen, PIPE, STDOUT
from models import Download
from webapp import constConfig 


# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

class Verifier():

	def __init__(self,token):
		self.download = Download.objects.get(tokenID=token)

	def createZIP(self,extension = None):

		folder = self.download.folder

		if extension == None:
			ext = ".zip"
		else:
			ext = extension

		srcPath = os.path.join(settings.DOWNLOAD_DIR,folder)
		dstPath = os.path.join(settings.VERIFIED_ZIP,folder+ext)

		verificationZip = zipfile.ZipFile(dstPath,"w",zipfile.ZIP_DEFLATED)

		#walk the directory and create the zip
		for dirname,subdirs,files in os.walk(srcPath):
			verificationZip.write(dirname)

			for f in files:
				verificationZip.write(os.path.join(dirname,f))

		verificationZip.close()
		return dstPath

	def createZIPtoVerify(self):
		""" Verify a ZIP by computing its """
		
		#the download has completed and there is not another ZIP verified
		if self.download.threadStatus == constConfig.THREAD_PHASE_3 and self.download.verificationZIP == False:
			dstPath = self.createZIP()
			
			#compute the rsa signature
			signature = crypto.rsaSignatureSHA256(dstPath,settings.PRIV_KEY,True)

			self.download.verificationZIP = True
			self.download.verificationZIPSignatureHash = crypto.sha256(signature).hexdigest()
			self.download.verificationZIPSignature = signature
			self.download.save()
		

	def createTimestampRequest(self):
		
		folder = self.download.folder
		dstRequest = os.path.join(settings.VERIFIED_ZIP,folder+".tsrequest")

		try:
			subprocess.check_output(["openssl ts -query -digest {} -sha256 -cert -no_nonce -out {}".format(self.download.verificationZIPSignatureHash,dstRequest)],shell=True)
		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))

		


	def timestampRequest(self):
		pass



