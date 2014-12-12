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
from Crypto.Hash import SHA256
import config, os, logger, struct, binascii
from Crypto.Signature import PKCS1_PSS
from cryptography.fernet import Fernet

HASH_SEPARATOR = "|"

def sha256(string):
	""" Hash of a string """

	#print string

	#encode string to UTF-8
	if type(string) is str:
		enc = string.decode('iso-8859-1').encode('utf-8')
	else:
		enc = string.encode("utf-8")

	hasher = SHA256.new()

	hasher.update(enc)
	return hasher

def sha256File(fileName):
	""" Hash of a file (http://www.pythoncentral.io/hashing-files-with-python/) """
	
	BLOCKSIZE = 65536

	hasher = SHA256.new()

	with open(fileName, "r") as myFile:
		buf = myFile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = myFile.read(BLOCKSIZE)

	return hasher

def md5(string):
	""" MD5 hash of a string """
	
	if type(string) is str:
		enc = string.decode('iso-8859-1').encode("utf-8")
	else:
		enc = string
	return hashlib.md5(enc).hexdigest()

def rsaSignatureSHA256(data,privkey,isFile=False):

	if os.path.isfile(privkey) and os.access(privkey, os.R_OK):
		try:
			h = None

			if isFile is True:
				h = sha256File(data)
			else:
				h = sha256(data)
			
			key = RSA.importKey(open(privkey,"rb").read(),"mypass")
			signer = PKCS1_PSS.new(key)
			
			#signature = binascii.hexlify(signer.sign(h))
			signature = base64.b64encode(signer.sign(h))

			return signature
		except Exception as e:
			logger.log(e)
			return None
	else: 
		logger.log("No private key found")

def verifyRSAsignatureSHA256(hashObject,sourceSignature,pubkey):

	if os.path.isfile(pubkey) and os.access(pubkey, os.R_OK):
		try:
			key = RSA.importKey(open(pubkey,"rb").read())
			verifier = PKCS1_PSS.new(key)
			
			if verifier.verify(hashObject,base64.b64decode(sourceSignature)): 
				return True
			else:
				return False
		except Exception as e:
			logger.log(e)
			return None

	else:
		logger.log("No public key found")


def encryptRSA(text, pubkey = None):
	""" Encrypt a string using the given public key !!! ONLY 128 Bits at time can be encrypted with PyCrypto"""
	
	rsaPubKey = pubkey if pubkey is not None else config.PUB_KEY_RSA

	# if pub key exists and is readable
	if os.path.isfile(rsaPubKey) and os.access(rsaPubKey, os.R_OK):
		try:
			key = RSA.importKey(open(rsaPubKey, "rb").read())
			cipher = PKCS1_OAEP.new(key)
			cipertext = cipher.encrypt(text)
			return base64.b64encode(cipertext)
		except Exception as e:
			logger.log(e)
			return None
	else:
		logger.log("No public key found")

def decryptRSA(ciphertext, privKey = None, passphrase = None):
	""" Decrypt a previously encrypted text using RSA """

	rsaPrivKey = privKey if privKey is not None else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "privkey.pem"))
	rsaPassphrase = passphrase if passphrase is not None else "mypass"	

	if os.path.isfile(rsaPrivKey) and os.access(rsaPrivKey, os.R_OK):
		try:
			key = RSA.importKey(open(rsaPrivKey, 'rb').read(), rsaPassphrase) 
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
	key = None
	del key
	
	#write
	return enc

	#logger.log("Writing to " + fileOut)

def decryptFernetFile(fileBytes, key):
	""" Decrypt a file using Fernet """

	#decrypt
	f = Fernet(key)
	dec = f.decrypt(fileBytes)
	key = None
	del key

	return dec
