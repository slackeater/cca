from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import drop
import json
from models import DropboxToken, DropboxFileMetadata
import dropbox
from importer.models import Upload
import time, base64, pickle, StringIO
from django.template.loader import render_to_string
from forms import DropMetaSearch
from dajaxice.utils import deserialize_form

@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """
	dajax = Dajax()
	
	try:
		token = drop.accessToken(code)
		dropTkn = DropboxToken(importID=Upload.objects.get(id=5), accessToken=token[0], userID=token[1])
		dropTkn.save()
		dajax.assign("#stat","innerHTML",str("Access Token: " + token[0] + "<br />User ID: " + token[1]))
	except dropbox.rest.ErrorResponse as e:
		dajax.assign("#stat","innerHTML",str(e.status) + ", " + str(e.reason) + ", " + str(e.error_msg))
	except Exception as e:
		dajax.assign("#stat","innerHTML", str(e.message))
	return dajax.json()

@dajaxice_register
def openFolder(request, resName, tokenID):
	""" Open a folder """
	dajax = Dajax() 
	
	try:
		#get token
		t = DropboxToken.objects.get(id=tokenID)
		c = dropbox.client.DropboxClient(t.accessToken)

		try:
			# check if we already have parsed this tree with the actual token
			getMeta = DropboxFileMetadata.objects.get(tokenID=t)
			metaInfo = pickle.loads(base64.b64decode(getMeta.metadata))
			dajax.assign("#statusMeta","innerHTML", str("Showing analysis of ") + str(getMeta.metaTime))
		except DropboxFileMetadata.DoesNotExist:
			getMeta = None

		if getMeta is None:
			dajax.assign("#statusMeta","innerHTML", str("Downloaded from Dropbox now."))
			#parse directory tree
			data = c.metadata("/", include_deleted=True, include_media_info=True)	
			pickledMetaInfo= StringIO.StringIO()
			metaInfo = recurseDropTree(data, c, 5);
			pickle.dump(metaInfo, pickledMetaInfo)
			
			#store this result
			metastore = DropboxFileMetadata(metadata=base64.b64encode(pickledMetaInfo.getvalue()), tokenID=t)
			metastore.save()

		dirCount, fileSize, fileCount, fileType, deletedFile = parseDropTree(metaInfo)
		data = { 'dC': dirCount, 'fS': fileSize, 'fC': fileCount, 'dF': deletedFile, 'types': fileType}
		table = render_to_string('dashboard/dropMetaTable.html',data)	
		dajax.assign("#analysisRes", "innerHTML", table)
	except Exception as e:
		dajax.assign("#statusMeta","innerHTML", str(e))
	except dropbox.rest.ErrorResponse as e:
		dajax.assign("#statusMeta","innerHTML", str(e))

	return dajax.json()

@dajaxice_register
def searchMetaData(request, form, tokenID):
	""" Search files over meta data """

	dajax = Dajax()
	desForm = DropMetaSearch(deserialize_form(form))

	if desForm.is_valid():
		try:
			# get metadata and decode it
			token = DropboxToken.objects.get(id=tokenID)
			getMetaInfo = DropboxFileMetadata.objects.get(tokenID=token)
			metaInfo = pickle.loads(base64.b64decode(getMetaInfo.metadata))
			res = list()
			t = int(desForm.cleaned_data['resType'][0])

			for folder in metaInfo:
				for cnt in folder['contents']:
					#deleted 
					if t == 0:
						try:
							if cnt['is_deleted']:
								res.append(cnt)
						except KeyError as e:
							None
					#MIME Type
					elif t == 1:
						None
					# Last modified
					elif t == 2:
						None
			print res
			table = render_to_string("dashboard/dropSearchTable.html", {'res': res})
			dajax.assign("#searchRes","innerHTML", table)
		except DropboxFileMetadata.DoesNotExist, DropboxToken.DoesNotExist:
			dajax.assign("#resStatus","innerHTML", "There is a problem with your search :(")
	
	else:
		dajax.assign("#resStatus","innerHTML", "Please fill in all fields")

	return dajax.json()
	# TODO
	



def recurseDropTree(folderMetadata, client, depth):
	""" Recurse in each folder """
	res = list()
	
	if folderMetadata['is_dir'] and depth > 0:

		res.append(folderMetadata)

		#get content
		for c in folderMetadata['contents']:
			if c['is_dir']:
				metadata = client.metadata(c['path'])
				# go down one level in the tree
				myres = recurseDropTree(metadata, client, depth-1)
				res += myres
				
		return res

	elif folderMetadata['is_dir'] and depth == 0:
		res.append(folderMetadata)
		return res

def parseDropTree(contList):
	""" Parse the list of file metadata """

	dirCount = len(contList)
	fileSize = 0
	fileCount = 0
	fileType = dict()
	deletedFile = 0

	for c in contList:
		for dirCont in c['contents']:
			if not dirCont['is_dir']:
				fileCount += 1
				fileSize += float(dirCont['bytes'])

				key = dirCont['mime_type']#.replace("/","_")
				fileType.setdefault(key, 0)
				fileType[key] += 1

				try:
					if dirCont['is_deleted']:
						deletedFile += 1
				except KeyError as e:
					None

	fileSize = fileSize/(1024*1024)
	return dirCount, fileSize, fileCount, fileType, deletedFile