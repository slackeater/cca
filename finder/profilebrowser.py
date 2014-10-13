import crypto

class BrowserProfile(object):
	""" Holds browser profile information found """

	def __init__(self, profileName, fileList, credList):
		self.profileName = profileName
		self.fileList = fileList
		self.credentialList = credList
	
	@property
	def credentialList(self):
		return self._credentialList

	@credentialList.setter
	def credentialList(self, credentialList):
		self._credentialList = credentialList

	@property
	def fileList(self):
		return self._fileList

	@fileList.setter
	def fileList(self, fileList):
		self._fileList = fileList
		hashList = list()

		# compute the signatures of the files
		for f in fileList:
			fileHandler = open(f,"r")
			sign = f + ":" + crypto.sha256File(fileHandler)
			hashList.append(sign)

		self.fileListHashes = hashList

	@property
	def fileListHashes(self):
		return self._fileListHashes

	@fileListHashes.setter
	def fileListHashes(self, hashList):
		self._fileListHashes = hashList
