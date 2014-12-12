#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.insert(0, '../')

import unittest
import crypto, base64
from cryptography.fernet import Fernet
from Crypto.Hash import SHA256

class CryptoTest(unittest.TestCase):

	def test_sha256(self):
		""" Test sha-256 of text string """
		precomputed = dict()
		precomputed[0] = "python|test:dba9e76e92cfd0e09ec192bec8ea6b8e7ce48857bad498c5a6d19300ebd7f1bd"
		precomputed[1] = "summer|winter|autumn|spring:a4a8064b9781f1ea0107d8644e2d7ab266a3f66cb84f5590d2f6495d9eb62db1"
		precomputed[2] = "berner|fach|hoch|schule:48fb694fa1c17a4dee36c300e60ed2719300e45a9e19d1fb2521bb289630b745"
		precomputed[3] = "ÈÈÈ|‡‡‡|$$$:4b472ac5d71b4e5836666b6e7b2b979ce66a2f4d6fd09bf8a06c388621d4ac19"
		precomputed[4] = "--|--|''''|???:e9feaa5e40796a040b6f7c1482395232999d4caf96bfdaf20ba353358bf774a4"

		for key in precomputed:
			split = precomputed[key].split(":")
			string = split[0]
			hashString = split[1]

			self.assertEquals(hashString, crypto.sha256(string).hexdigest())


		print crypto.sha256("Syst\u00e8me d'autorisation").hexdigest()

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(CryptoTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
