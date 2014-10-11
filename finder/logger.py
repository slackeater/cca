#!/usr/bin/python


####
###
##
#	Logger
##
###
####

import time


def formattedTime():
	return time.asctime(time.localtime(time.time()))

def init():
	print("Log initialized " + formattedTime())

def log(message, date = "yes"):
	if date != "yes":
		print(message)
	else: 
		msg = formattedTime() + ": " + str(message)
		print(msg)	

def error(message):
	print "==> Problem: ",
	log(message) 
