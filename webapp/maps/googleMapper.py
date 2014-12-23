from downloader.models import FileDownload,FileHistory
import os,sys
from django.conf import settings
from abstractMaps import AbstractMaps
from webapp.thumbnailer import Thubmnailer
import json,base64
from dashboard.models import MimeType

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)

del cryptoPath

import crypto

class GoogleMapper(AbstractMaps):

	def __init__(self,token):
		AbstractMaps.__init__(self,token)
		self.relationModificationWeight = float(0.2)
		self.relationShareWeight = float(1.0)

	def findExif(self):
		res = list()

		for f in self.metadata:
			if "imageMediaMetadata" in f:
				if "location" in f["imageMediaMetadata"]:
					lat = f["imageMediaMetadata"]["location"]["latitude"]
					lon = f["imageMediaMetadata"]["location"]["longitude"]

					#compute file name
					fName = crypto.sha256(f['title']+crypto.HASH_SEPARATOR+f['id']).hexdigest()+"_"+f['id']

					#copy src img to thumbnail folder
					srcDir = os.path.join(settings.DOWNLOAD_DIR,self.d.folder,"files",fName)
					dstDir = os.path.join(settings.DIFF_DIR,fName+".thubmnail")

					#generate thumbnail
					thumb = Thubmnailer()
					thumb.cacheImg(srcDir,dstDir,250,250)

					res.append({"title":f['title'],"lat":lat,"lon":lon,'fName': fName+".thubmnail"})

		return res

	def mailFinder(self):
		#get e-mail in access token, start node
		atEmail = json.loads(base64.b64decode(self.t.accessToken))["id_token"]["email"]

		owners = dict()
		sharingUser = dict()
		lastModifyingUser = dict()
		res = dict()

		#add main user to dict
		for r in self.metadata:
			#search in owners and must not be a folder
			if "owners" in r and r['mimeType'] != MimeType.objects.get(id=1340).mime:
				#look for all owners
				for o in r['owners']:
					#add owner email
					ownerEmail = o['emailAddress']

					if ownerEmail != atEmail:
						res[ownerEmail] = res.get(ownerEmail,float(0)) + self.relationShareWeight

					#now look for the history of the file to found modification by users
					try:
						downFile = FileDownload.objects.get(fileName=r['title'],alternateName=r['id'],tokenID=self.t)
						print downFile
						#take each entry on the history 
						for h in FileHistory.objects.filter(fileDownloadID=downFile,status=200):
							historyMeta = json.loads(base64.b64decode(h.revisionMetadata))

							if historyMeta.get("lastModifyingUser") != None and historyMeta.get("lastModifyingUser").get("emailAddress") != None:

								lastModifyingEmail = historyMeta['lastModifyingUser']['emailAddress']
								if lastModifyingEmail != atEmail:
									res[lastModifyingEmail] = res.get(lastModifyingEmail,float(0)) + self.relationModificationWeight
					except FileDownload.DoesNotExist as e:
						print e

		return {'mainNode': atEmail, 'linkedNodes':res}
