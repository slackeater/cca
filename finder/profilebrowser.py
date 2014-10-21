import crypto, json
from credentials import CredentialsEncoder

class BrowserProfile(object):
	""" Holds browser profile information found """

	def __init__(self, profileName, fileList, credList):
		self.profileName = profileName
		hashList = list()
		self.fileListHashes = fileList
		self.credentialList = credList
	
	@property
	def credentialList(self):
		return self._credentialList

	@credentialList.setter
	def credentialList(self, credentialList):
		self._credentialList = credentialList

	@property
	def fileListHashes(self):
		return self._fileListHashes

	@fileListHashes.setter
	def fileListHashes(self, hashList):
		self._fileListHashes = hashList

class BrowserProfileEncoder(json.JSONEncoder):
	def default(self, obj):
		if not isinstance(obj, BrowserProfile):
			return super(BrowserProfile, self).default(obj)

		val = dict()

		for key, value in obj.__dict__.iteritems():
			if key == "_credentialList":
				val[key] = json.dumps(value, cls=CredentialsEncoder)
			else:
				val[key] = value

		return val



