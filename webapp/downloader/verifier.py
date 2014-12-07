from django.conf import settings
import os,zipfile,sys,base64,binascii,subprocess,re
from subprocess import Popen, PIPE, STDOUT
from models import Download
from webapp import constConfig 
import requests,shlex

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

class Verifier():

	def __init__(self,token):
		self.t = token
		self.tsRequest = None
		self._account = None
		self._pwd = None

	def verifyCredentials(self,uname,pwd):
		
		session = requests.Session()
		payload = {'j_username': uname,'j_password': pwd}
		session.get("https://www.digistamp.com/account")
		session.post("https://www.digistamp.com/account/j_security_check",data=payload,allow_redirects=True)
		response = session.get("https://www.digistamp.com/account/userChoice.jsp")
		m = re.search('Account '+str(uname),response.text)

		if m is not None and m.group(0):
			#match, now logout
			session.get("https://www.digistamp.com/account/logOut.do",allow_redirects=True)
			self._pwd = pwd
			self._account = re.escape(uname)
			return True
		else: 
			raise Exception("Credentials for the timestamp authority are invalid")	

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

	def verificationProcess(self):
		#get new download first
		self.download = Download.objects.get(tokenID=self.t)

		self.createZIPtoVerify()

		self.createTimestampRequest()

		self.timestampRequest()

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
		else: 
			raise Exception("Download not complete or ZIP already exists.")

	def createTimestampRequest(self):
		
		folder = self.download.folder
		dstRequest = os.path.join(settings.VERIFIED_ZIP,folder+".tsrequest")

		try:
			cmdline = '%s %s' % ("openssl ts","-query -sha256 -digest {} -cert -no_nonce -out {}".format(self.download.verificationZIPSignatureHash,dstRequest))
			subprocess.check_output(shlex.split(cmdline))

			#check that file exists
			if os.path.isfile(dstRequest):
				self.tsRequest = dstRequest

		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))

	def timestampRequest(self):

		tsResponse = os.path.join(settings.VERIFIED_ZIP,self.download.folder+".p7s")
	
		try:
			p1 = subprocess.Popen("cat {}".format(self.tsRequest),stdout=subprocess.PIPE)
			p2 = subprocess.Popen("curl -s -S -H 'Content-Type: application/timestamp-query' --data-binary @- https://{}:{}@tsa1.digistamp.com/TSA -o {}".format(self._account,self._pwd,tsResponse),stdin=p1.stdout,stdout=subprocess.PIPE)
			p1.stdout.close()

			outout = p2.communicate()[0]


			print "cat {} | curl -s -S -H 'Content-Type: application/timestamp-query' --data-binary @- https://{}:{}@tsa1.digistamp.com/TSA -o {}".format(self.tsRequest,self._account,self._pwd,tsResponse)
		except subprocess.CalledProcessError as e:
			raise Exception(str(e.returncode) + " " + str(e.cmd) + " " + str(e.output))
