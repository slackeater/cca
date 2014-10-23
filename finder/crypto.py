#/usr/bin/python

####
### Cryptographical operations
##
#
##
###
####

import hashlib, base64, hmac
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import config, os, logger, struct
from cryptography.fernet import Fernet

HASH_SEPARATOR = "|"

def sha256(string):
	""" Hash of a string """

	#encode string to UTF-8
	if type(string) is str:
		enc = string.decode('iso-8859-1').encode('utf-8')
	else:
		enc = string

	return hashlib.sha256(enc).hexdigest() 

def sha256File(fileName, hmacKey = None):
	""" Hash of a file (http://www.pythoncentral.io/hashing-files-with-python/) """
	
	BLOCKSIZE = 65536

	if hmacKey is None:
		hasher = hashlib.sha256()
	else:
		hasher = hmac.new(hmacKey, None, hashlib.sha256)

	with open(fileName, "r") as myFile:
		buf = myFile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = myFile.read(BLOCKSIZE)
	return hasher.hexdigest()

def md5(string):
	""" MD5 hash of a string """
	
	if type(string) is str:
		enc = string.decode('iso-8859-1').encode("utf-8")
	else:
		enc = string
	return hashlib.md5(enc).hexdigest()

def encryptRSA(text):
	""" Encrypt a string using the given public key !!! ONLY 128 Bits at time can be encrypted with PyCrypto"""
	
	# if pub key exists and is readable
	if os.path.isfile(config.PUB_KEY_RSA) and os.access(config.PUB_KEY_RSA, os.R_OK):
		try:
			key = RSA.importKey(open(config.PUB_KEY_RSA, "rb").read())
			cipher = PKCS1_OAEP.new(key)
			cipertext = cipher.encrypt(text)
			return base64.b64encode(cipertext)
		except Exception as e:
			logger.log(e)
			return None
	else:
		logger.log("No public key found")

def decryptRSA(ciphertext):
	""" Decrypt a previously encrypted text using RSA """

	privKey = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "privkey.pem"))
	
	if os.path.isfile(privKey) and os.access(privKey, os.R_OK):
		try:
			key = RSA.importKey(open(privKey, 'rb').read(), "mypass")
			cipher = PKCS1_OAEP.new(key)
			text = cipher.decrypt(base64.b64decode(ciphertext))
			return text
		except Exception as e:
			logger.log(e)
		return None
	else:
		logger.log("No private key found")


def encryptFernetFile(fileIn, key):
	""" Encrypt a file using Fernet """

	#get file bytes
	fileBytes = open(fileIn, "rb").read()

	#encrypt
	f = Fernet(key)
	enc = f.encrypt(fileBytes)

	#write
	return enc

	#logger.log("Writing to " + fileOut)

def decryptFernetFile(fileBytes, key):
	""" Decrypt a file using Fernet """

	#decrypt
	f = Fernet(key)
	dec = f.decrypt(fileBytes)

	return dec
