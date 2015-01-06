from django.conf import settings
import os,zipfile,sys,base64,binascii,subprocess,re
from subprocess import Popen, PIPE, STDOUT
from models import Download
from webapp import constConfig 
import requests,shlex
from webapp import crypto

class Verifier():
	""" This class represent the verification process where we store and sign the evidence with a digital timestampgin service """

	def __init__(self,download):
		self.download = download
		self.tsRequest = None
		self.tsResponse = None
		self._account = None
		self._pwd = None

	def verifyCredentials(self,uname,pwd):
		""" Verify the credentials by loggin in to the TSA (TimeStamp Authority) service """

		session = requests.Session()
		payload = {'j_username': uname,'j_password': pwd}
		session.get("https://www.digistamp.com/account/")
		session.post("https://www.digistamp.com/account/j_security_check",data=payload,allow_redirects=True)
		response = session.get("https://www.digistamp.com/account/view/subscription/")
		m = re.search(str(uname),response.text)

		if m is not None and m.group(0):
			#match, now logout
			session.get("https://www.digistamp.com/account/logOut.do",allow_redirects=True)
			self._pwd = pwd
			self._account = re.escape(uname)
			return constConfig.THREAD_VERIFY_CRED
		else: 
			raise Exception("Credentials for the timestamp authority are invalid")	

	def createZIP(self,extension = None):
		""" Create a ZIP file """

		if extension == None:
			ext = ".zip"
		else:
			ext = extension

		srcPath = os.path.join(settings.DOWNLOAD_DIR,self.download.folder)
		dstPath = os.path.join(settings.VERIFIED_ZIP,self.download.folder+ext)

		verificationZip = zipfile.ZipFile(dstPath,"w",zipfile.ZIP_DEFLATED)

		#walk the directory and create the zip
		for dirname,subdirs,files in os.walk(srcPath):
			verificationZip.write(dirname)

			for f in files:
				verificationZip.write(os.path.join(dirname,f))

		verificationZip.close()
		return dstPath

	def verificationProcess(self):
		""" Start a predefined list of steps in order to sign the ZIP with the TSA """

		zipVer = self.createZIPtoVerify()

		createTsReq = self.createTimestampRequest()

		tsReq = self.timestampRequest()

		ver = self.verifyTimestamp()

		if zipVer and createTsReq and tsReq and ver:
			#set download verified
			self.download.verified = True
			self.download.save()

			return constConfig.THREAD_TS
		else:
			raise Exception("A problem occured: zip cannot be created, timestamp request cannot be created or verification of timestamps failed")

	def createZIPtoVerify(self):
		""" Verify a ZIP by computing its signature """
		
		#the download has completed and there is not another ZIP verified
		if self.download.threadStatus == constConfig.THREAD_DOWN_FH and self.download.verificationZIP == False:
			dstPath = self.createZIP()
			
			#compute the rsa signature
			signature = crypto.rsaSignatureSHA256(dstPath,settings.PRIV_KEY,True)

			self.download.verificationZIP = True
			self.download.verificationZIPSignatureHash = crypto.sha256(signature).hexdigest()
			self.download.verificationZIPSignature = signature
			self.download.save()
			return True
		else: 
			raise Exception("Download not complete or ZIP already exists.")

	def createTimestampRequest(self):
		""" Create a timestamp request """

		dstRequest = os.path.join(settings.VERIFIED_ZIP,self.download.folder+".tsrequest")

		try:
			cmdline = '%s %s' % ("openssl ts","-query -sha256 -digest {} -cert -no_nonce -out {}".format(self.download.verificationZIPSignatureHash,dstRequest))
			subprocess.check_output(shlex.split(cmdline))

			#check that file exists
			if os.path.isfile(dstRequest):
				self.tsRequest = dstRequest

			return True

		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))

	def timestampRequest(self):
		""" Send the previously created timestamp request to the TSA """

		self.tsResponse = os.path.join(settings.VERIFIED_ZIP,self.download.folder+".p7s")
	
		try:
			#obtain a signed timestamp
			p1 = subprocess.Popen(["cat",self.tsRequest],stdout=subprocess.PIPE)
			p2 = subprocess.Popen(["curl","-s","-S","-H","Content-Type: application/timestamp-query#","--data-binary","@-","https://{}:{}@tsa1.digistamp.com/TSA".format(self._account,self._pwd,self.tsResponse)],stdin=p1.stdout,stdout=subprocess.PIPE)
			p1.stdout.close()

			output = p2.communicate()[0]
			
			with open(self.tsResponse,"wb") as f:
				f.write(output)

			return True
		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))

	def verifyTimestamp(self):
		""" Verify wether the created timestamp is correct or not """

		try:
			cmdline = '%s %s' % ("openssl ts","-verify -queryfile {} -in {} -CAfile {}".format(self.tsRequest,self.tsResponse,os.path.join(settings.VERIFIED_ZIP,"digistamp.pem")))
			subprocess.check_output(shlex.split(cmdline))
			return True
		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))
