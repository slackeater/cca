from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import drop
from models import DropboxToken, DropboxFileMetadata
import dropbox
from importer.models import Upload
import time, base64, pickle, StringIO

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

		dajax.assign("#analysisRes", "innerHTML", str(metaInfo).decode("utf-8"))
	except Exception as e:
		dajax.assign("#statusMeta","innerHTML", str(e))
	except dropbox.rest.ErrorResponse as e:
		dajax.assign("#statusMeta","innerHTML", str(e))

	return dajax.json()

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
