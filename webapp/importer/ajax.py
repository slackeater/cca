from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json, zipfile

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
del cryptoPath

import crypto

@dajaxice_register
def decrypt(request):
	
	dajax = Dajax()
	
	try:
		fileName = request.session['fileName']
		fileCont = open(os.path.join(settings.UPLOAD_DIR,fileName), "r")
		jsonParsed = json.load(fileCont)
		cont = jsonParsed['enc']
		k = jsonParsed['k']

		#decrypt AES key
		aes = crypto.decryptRSA(k)
		
		#decrypt ZIP - first write encrypted cont into a temp file, read it, decrypt it and store the ZIP
		tempFileName = os.path.join(settings.UPLOAD_DIR, fileName+".tmp")
		open(tempFileName, "w+b").write(cont)
		
		# fernet wants "bytes" as token
		fileBytes = crypto.decryptFernetFile(open(tempFileName, "rb").read(), aes)
		#write decrypted file
		decZipFile = os.path.join(settings.UPLOAD_DIR, fileName.strip(".enc"))
		open(decZipFile, "w+b").write(fileBytes)
		
		#delete temp file
		os.remove(tempFileName)

		aes = None
		del aes

		msg = "File decrypted correctly"

		try:
			fileZip = zipfile.ZipFile(decZipFile)
			fileZip.extractall(settings.UPLOAD_DIR)
			
			msg += "<br />ZIP extracted correctly"
			dajax.assign("#parseStatus","innerHTML",msg)
			return dajax.json()
		except Exception as e:
			dajax.assign("#parseStatus","innerHTML",str(e.message))
			return dajax.json()
	except Exception as e:
		dajax.assign("#parseStatus","innerHTML",str(e.message))
		return dajax.json()
