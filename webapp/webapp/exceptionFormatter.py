import traceback
import sys
from django.template.loader import render_to_string

def formatException(exception):
	ex_type, ex, tb = sys.exc_info()
	
	tbInfo = traceback.extract_tb(tb)

	msgList = list()
	msgList.append(ex)
	msgList.append(tbInfo[0][0])
	msgList.append(tbInfo[0][2])
	msgList.append(tbInfo[0][1])

	excFormatted = render_to_string("exceptions.html",{'info': msgList})
	return excFormatted
