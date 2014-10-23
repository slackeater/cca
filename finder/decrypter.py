#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##  Generates signatures.
###
####

from ctypes import *
import config
import sqlite3, os, json, subprocess, base64, glob
import crypto, logger
from credentials import Credentials

### Code from ffpwdcracker.py

#Password structures
class SECItem(Structure):
	_fields_ = [('type',c_uint),('data',c_void_p),('len',c_uint)]

class secuPWData(Structure):
	_fields_ = [('source',c_ubyte),('data',c_char_p)]

(SECWouldBlock,SECFailure,SECSuccess)=(-2,-1,0)
(PW_NONE,PW_FROMFILE,PW_PLAINTEXT,PW_EXTERNAL)=(0,1,2,3)

### End code from ffpwdcracker.py

### Constants and globals

WIN_DECRYPTER = "C:\\Users\\John\\Documents\\Visual Studio 2012\\Projects\\ConsoleApplication3\\Debug\\ConsoleApplication3.exe"

### End Constants and globals

def getPasswords(loginFile, profile):
	""" Select password from relative SQLite database """

	cred = list()

	# get file name
	baseName = os.path.basename(os.path.normpath(loginFile))
	print "BASENAME " + baseName

	if not os.path.isfile(loginFile):
		return cred

	conn = sqlite3.connect(loginFile)

	if baseName == config.GCHROME_LOGIN_FILE:
		#chrome on windows, run Windows C application
		if config.OP_SYS == "Windows":
			logger.log("Attempting to decrypt Windows Chrome logins")

			query = "SELECT origin_url, username_value, hex(password_value) FROM logins"
			
			try:		
				for row in conn.execute(query):
					try:
						pwd = row[2]
						#execute windows decrypt helper with password as parameter
						retval = subprocess.check_output([WIN_DECRYPTER, pwd])

						if retval == "<decryption failed>":
							pwd = ""
						else:
							pwd = retval

						cred.append(Credentials(row[0], row[1], pwd, profile))
					except subprocess.CalledProcessError as e:
						logger.error(format(e.errno, e.strerror))
			except sqlite3.OperationalError as e:
				logger.error(e)
		#chrome on linux, clear text password or encrypted with key chain, simply return the value we found
		elif config.OP_SYS == "Linux":
			query = "SELECT origin_url, username_value, quote(password_value) FROM logins"
			
			try:
				for row in conn.execute(query):
					cred.append(Credentials(row[0], row[1], row[2], profile))
			except sqlite3.Error as e:
				logger.error(e)
			finally:
				conn.close()

	elif baseName == config.MOZ_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"
	
		try:
			for row in conn.execute(query):
				  #firefox/thunderbird on linux/windows, use NSS library to decrypt
				  credentials = decryptMozilla(row[1],row[2], config.LIBNSS, os.path.dirname(loginFile))
				  cred.append(Credentials(row[0], credentials[0], credentials[1], profile))	
		except sqlite3.Error as e:
			logger.error(e)
		finally:
			conn.close()

	
	return cred
		
def decryptMozilla(username, password, libnss, profileFolder):
	""" Decrypt mozilla login, based on ffpwdcracker.py """
	
	decItems = ["",""]

	if libnss is None:
	  logger.error("No nss given")
	  return decItems
	
	# code from ffpwdcracker.py
	nss = CDLL(libnss)
	
	if nss.NSS_Init(profileFolder) != 0:
		logger.error("Error initializing NSS")
		logger.error(nss.PORT_GetError())
		return decItems

	#prepare data structures
	pwdata = secuPWData()
	pwdata.source = PW_NONE
	pwdata.data=0

	uname = SECItem()
	passwd = SECItem()
	dectext = SECItem()

	uname.data = cast(c_char_p(base64.b64decode(username)),c_void_p)
	uname.len = len(base64.b64decode(username))

	passwd.data = cast(c_char_p(base64.b64decode(password)),c_void_p)
	passwd.len = len(base64.b64decode(password))

	#decrypt
	if nss.PK11SDR_Decrypt(byref(uname),byref(dectext),byref(pwdata))==-1:
		logger.error("Error decrypting")
		logger.error(nss.PORT_GetError())
		return decItems 

	decUsername = string_at(dectext.data,dectext.len)

	if nss.PK11SDR_Decrypt(byref(passwd),byref(dectext),byref(pwdata))==-1:
		logger.error("Error decrypting")
		logger.error(nss.PORT_GetError())
		return decItems

	decPassword = string_at(dectext.data,dectext.len)
	
	decItems = [decUsername, decPassword]
	nss.NSS_Shutdown()

	return decItems
	
def readLoginsJSON(loginFileJSON, profile):
	""" Read the JSON of Firefox login data """

	cred = list()

	if not os.path.isfile(loginFileJSON):
		return cred

	data = json.loads(open(loginFileJSON).read())

	for login in data['logins']:
		credentials = decryptMozilla(login['encryptedUsername'],login['encryptedPassword'], config.LIBNSS,os.path.dirname(loginFileJSON))
		cred.append(Credentials(login['hostname'], credentials[0], credentials[1], profile))	

	return cred
