import json,base64,time
from downloader.models import FileMetadata

def constructLineItem(item):

	date = item['modified']
	parsedDate = time.strptime(date,"%a, %d %b %Y %H:%M:%S +0000")
	print parsedDate


def formTimeline(cloudItem,token,resType,mimeType):

	retval = list()

	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))

	for f in meta:
		for c in f['contents']:
			if resType == 0:
				if 'is_deleted' in c:
					constructLineItem(c)
			elif resType == 2:
					constructLineItem(c)

	return retval
