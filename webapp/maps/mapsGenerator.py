from downloader.models import FileMetadata, FileHistory, FileDownload
from dashboard.models import MimeType

import base64,json

class MapsFinder():

	def __init__(self,token):
		self.t = token

	def decodeMetaData(self,metadata):
		decodedMetadata = base64.b64decode(metadata)
		jsonMetadata = json.loads(decodedMetadata)
		return jsonMetadata

	def findExif(self):

		r = None

		if self.t.serviceType == "google":
			r = self.googleExifFinder()
		elif self.t.serviceType == "dropbox":
			r = self.dropboxExifFinder()

		return r

	def googleExifFinder(self):
		meta = self.decodeMetaData(FileMetadata.objects.get(tokenID=self.t).metadata)

		res = list()

		for f in meta:
			if "imageMediaMetadata" in f:
				if "location" in f["imageMediaMetadata"]:
					lat = f["imageMediaMetadata"]["location"]["latitude"]
					lon = f["imageMediaMetadata"]["location"]["longitude"]
					res.append({"title":f['title'],"lat":lat,"lon":lon})

		return res

	def dropboxExifFinder(self):
		meta = self.decodeMetaData(FileMetadata.objects.get(tokenID=self.t).metadata)

		res = list()

		# for each folder
		for r in meta:
			#for each file in the folder
			for f in r['contents']:
				if "photo_info" in f:
					if f["photo_info"]["lat_long"] is not None:
						lat = f["photo_info"]["lat_long"][0]
						lon = f["photo_info"]["lat_long"][1]
						res.append({"title":f['path'],"lat":lat,"lon":lon})

		return res

	def mailRelator(self):

		r = None

		if self.t.serviceType == "google":
			r = self.googleMailFinder()

		return r

	def googleMailFinder(self):
		meta = self.decodeMetaData(FileMetadata.objects.get(tokenID=self.t).metadata)

		#get e-mail in access token, start node
		atEmail = json.loads(base64.b64decode(self.t.accessToken))["id_token"]["email"]

		owners = dict()
		sharingUser = dict()
		lastModifyingUser = dict()
		res = dict()

		#add main user to dict

		for r in meta:
			#search in owners and must not be a folder
			if "owners" in r and r['mimeType'] != MimeType.objects.get(id=1340).mime:
				#look for all owners
				for o in r['owners']:
					#add owner email
					ownerEmail = o['emailAddress']

					if ownerEmail != atEmail:
						res[ownerEmail] = res.get(ownerEmail,float(0)) + float(1)
						
					#now look for the history of the file to found modification by users
					downFile = FileDownload.objects.filter(fileName=r['title'],alternateName=r['id'])

					#take each entry on the history 
					for h in FileHistory.objects.filter(fileDownloadID=downFile):
						historyMeta = self.decodeMetaData(h.revisionMetadata);
						
						if historyMeta.get("lastModifyingUser") != None:
							lastModifyingEmail = historyMeta['lastModifyingUser']['emailAddress']
					
							if lastModifyingEmail != atEmail:
								res[lastModifyingEmail] = res.get(lastModifyingEmail,float(0)) + 0.2

		
		return {'mainNode': atEmail, 'linkedNodes':res}
