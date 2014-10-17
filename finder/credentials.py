import crypto

class Credentials(object):
	""" Holds credentials and signature """

	def __init__(self, hostname, username, password, profile):
		self._hostname = hostname
		self._username = username
		self._password = password
		self._profile = profile

		if self.hostname and self.username and self.password:
			self._signature = crypto.sha256(self.hostname + crypto.HASH_SEPARATOR + self.username + crypto.HASH_SEPARATOR + self.password)
		else:
			self._signature = "empty signature"

	@property
	def hostname(self):
		return self._hostname
	
	@property
	def username(self):
		return self._username
	
	@property
	def password(self):
		return self._password
	
	@property
	def signature(self):
		return self._signature
	
	@property
	def profile(self):
		return self._profile
