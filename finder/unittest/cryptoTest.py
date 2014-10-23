#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.insert(0, '../')

import unittest
import crypto


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

			self.assertEquals(hashString, crypto.sha256(string))

	def test_sha256File(self):
		""" Test sha-256 of file """
		# hash precomputed with console sha256sum
		precomputed = dict()
		precomputed["file1.txt"] = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
		precomputed["file2.txt"] = "a635bbfe8cfe3f0a34c486a9f3a06aa55d1ad93c9beed7d11645822319cdc9dc"
		precomputed["file3.txt"] = "54ad54758b4975ae8235db588dedeef041b637d34ccb4f9f26b26dd2f283c3dd"

		for key in precomputed:
			self.assertEquals(precomputed[key], crypto.sha256File(key))

	def test_md5(self):
		""" Test md5 of string """
		precomputed = dict()
		precomputed[0] = "python|test:96391226d553838ffa15113e1ebedfe3"
		precomputed[1] = "summer|winter|autumn|spring:ad4be9bb779f0f33b3b6fdafcf692738"
		precomputed[2] = "berner|fach|hoch|schule:768975d9aaa218e33faeeffbad43d148"
		precomputed[3] = "ÈÈÈ|‡‡‡|$$$:c0baf33eccd30680261909c752e22e87"
		precomputed[4] = "--|--|''''|???:88ff8f10e4bd1f374072cfd3f4d8e665"

		for key in precomputed:
			split = precomputed[key].split(":")
			string = split[0]
			hashString = split[1]

			self.assertEquals(hashString, crypto.md5(string))
		
if __name__ == '__main__':
	unittest.main()
