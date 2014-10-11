#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##  Generates signatures.
###
####

from ctypes import *
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

GCHROME_LOGIN_FILE = "Login Data"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"
WIN_DECRYPTER = "C:\\Users\\John\\Documents\\Visual Studio 2012\\Projects\\ConsoleApplication3\\Debug\\ConsoleApplication3.exe"

### End Constants and globals

def getPasswords(loginFile, profile, nss = None, opsys = None):
	""" Select password from relative SQLite database """

	cred = list()

	if not os.path.isfile(loginFile):
		logger.error("Login file " + loginFile + " does not exists.")
		return cred

	conn = sqlite3.connect(loginFile)

	if loginFile is GCHROME_LOGIN_FILE:
		#chrome on windows, run Windows C application
		if opsys == "Windows":
			logger.log("Attempting to decrypt Windows Chrome logins")

			query = "SELECT origin_url, username_value, hex(password_value) FROM logins"

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

		#chrome on linux, clear text password or encrypted with key chain, simply return the value we found
		elif opsys == "Linux":
			query = "SELECT origin_url, username_value, quote(password_value) FROM logins"

			for row in conn.execute(query):
				cred.append(Credentials(row[0], row[1], row[2], profile))

	elif loginFile is MOZ_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"
		
		for row in conn.execute(query):
			  #firefox/thunderbird on linux/windows, use NSS library to decrypt
			  credentials = decryptMozilla(row[1],row[2], nss)
			  cred.append(Credentials(row[0], credentials[0], credentials[1], profile))	

	conn.close()
	return cred
		
def decryptMozilla(username, password, libnss):
	""" Decrypt mozilla login, based on ffpwdcracker.py """
	
	decItems = ["",""]

	if libnss is None:
	  logger.error("No nss given")
	  return decItems
	
	# code from ffpwdcracker.py
	nss = CDLL(libnss)
	
	if nss.NSS_Init(os.getcwd()) != 0:
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
	
def readLoginsJSON(loginFileJSON, profile, nss):
	""" Read the JSON of Firefox login data """

	cred = list()

	if not os.path.isfile(loginFileJSON):
		logger.error("JSON file " + loginFileJSON + " does not exist.")
		return cred

	data = json.loads(open(loginFileJSON).read())

	for login in data['logins']:
		credentials = decryptMozilla(login['encryptedUsername'],login['encryptedPassword'], nss)
		cred.append(Credentials(login['hostname'], credentials[0], credentials[1], profile))	

	return cred

def readMozillaLogins(sw, profileDir, nss):
	""" Read and parse the login file of thunderbird or firefox """

	# initialize variable used for return 
	cred = list()	

	logger.log("\n","no")
	logger.log(sw.upper())

	#get first default profile directory
	os.chdir(profileDir)

	#open and read profiles.ini
	profiles = open("profiles.ini", "r")

	for line in profiles:
		# get profile directory
		if line.startswith("Path="): 
			p = line.split("=")[1].strip("\n")
			logger.log("Found profile directory " + p)
			os.chdir(p)

			# look for signons.sqlite
			cred =  cred + getPasswords(MOZ_LOGIN_FILE_DB, p, nss)

			# look for logins.json
			cred = cred + readLoginsJSON(MOZ_LOGIN_FILE_JSON, p, nss)

			#go up one directory
			os.chdir(os.path.dirname(os.getcwd()))

	return cred

def readChromeLogins(chromeProfile, opsys):
	""" Read and parse the login file of chrome """
	
	# initialize variable used for return 
	cred = list()	

	logger.log("\n","no")
	logger.log("GOOGLE CHROME")

	os.chdir(chromeProfile)

	#look in default profile
	if os.path.isdir("Default"):
		os.chdir("Default")
		logger.log("Found profile directory Default")
		cred = cred + getPasswords(GCHROME_LOGIN_FILE, "Default", None, opsys)

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	#look for other profiles (Profile 1, Profile 2, Profile 3, ...)
	profiles = glob.glob("Profile *")

	for profile in profiles:
		os.chdir(profile)
		logger.log("Found profile directory " + profile)
		cred = cred + getPasswords(GCHROME_LOGIN_FILE, profile, None, opsys)

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	return cred
