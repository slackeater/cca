from downloader.models import FileMetadata
import base64,json

class MapsFinder():

	def __init__(self,token):
		self.t = token

	def decodeMetaData(self):
		decodedMetadata = base64.b64decode(FileMetadata.objects.get(tokenID=self.t).metadata)
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
		meta = self.decodeMetaData()

		res = list()

		for f in meta['items']:
			if "imageMediaMetadata" in f:
				lat = f["imageMediaMetadata"]["location"]["latitude"]
				lon = f["imageMediaMetadata"]["location"]["longitude"]
				res.append({"title":f['title'],"lat":lat,"lon":lon})

		return res

	def dropboxExifFinder(self):
		meta = self.decodeMetaData()

		res = list()

		# for each folder
		for r in meta:
			#for each file in the folder
			for f in r['contents']:
				if "photo_info" in f:
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
		meta = self.decodeMetaData()

		#get e-mail in access token, start node
		atEmail = json.loads(base64.b64decode(self.t.accessToken))["id_token"]["email"]

		owners = dict()
		sharingUser = dict()
		lastModifyingUser = dict()
		res = dict()

		#add main user to dict

		for r in meta['items']:
			#search in owners
			if "owners" in r:
				#look for all owners
				for o in r['owners']:
					#add owner email
					ownerEmail = o['emailAddress']

					if ownerEmail != atEmail:
						res[ownerEmail] = res.get(ownerEmail,0) + 1

		
			"""if "sharingUser" in r:
				shareEmail = r['sharingUser']['emailAddress']

				if shareEmail != atEmail:
					res[shareEmail] = res.get(shareEmail,0) + 1
					"""
		return {'mainNode': atEmail, 'linkedNodes':res}
