import googledrive
import md5
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

def isAuhtenticated(request):
	""" Check if a user is authenticated """
	return request.user.is_authenticated()

@dajaxice_register
def metadataAnalysis(request,tokenID, update, platform):
	""" Analyise the metadata of services """

	if not isAuhtenticated(request):
		return None

	t = int(tokenID)

	if not t > 0:
		return None
	
	dajax = Dajax()

	#try:
	parsedTable = None

	try:
		if platform == "google":
			parsedTable = googledrive.metadataAnalysis(request, update, t)

		dajax.assign("#metaAnalysis","innerHTML", parsedTable)
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML",e)

	return dajax.json()
