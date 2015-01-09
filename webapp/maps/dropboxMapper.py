from downloader.models import FileDownload,FileHistory
import os,sys
from django.conf import settings
from abstractMaps import AbstractMaps
from webapp.thumbnailer import Thubmnailer
import json,base64
from dashboard.models import MimeType
from webapp.func import dropboxAlternateName

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)

del cryptoPath

import crypto

class DropboxMapper(AbstractMaps):
	""" This class represent a Dropbox mapper """

	def __init__(self,token):
		AbstractMaps.__init__(self,token)

	def findExif(self):
		res = list()

		# for each folder
		for r in self.metadata:
			#for each file in the folder
			for f in r['contents']:
				if "photo_info" in f:
					if f["photo_info"]["lat_long"] is not None:
						lat = f["photo_info"]["lat_long"][0]
						lon = f["photo_info"]["lat_long"][1]

						#compute file name
						altName = dropboxAlternateName(f['path'],f['modified'])
						fName = crypto.sha256(os.path.basename(f['path'])+crypto.HASH_SEPARATOR+altName).hexdigest()+"_"+altName

						#copy src img to thumbnail folder
						srcDir = os.path.join(settings.DOWNLOAD_DIR,self.d.folder,"files",fName)
						dstDir = os.path.join(settings.DIFF_DIR,fName+".thubmnail")

						#generate thumbnail
						thumb = Thubmnailer()
						thumb.cacheImg(srcDir,dstDir,250,250)

						res.append({"title":f['path'],"lat":lat,"lon":lon,'fName':fName+".thubmnail"})

		return res

	def mailFinder(self):
		#not supported by drobpox 
		return None
