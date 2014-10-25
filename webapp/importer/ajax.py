from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions

@dajaxice_register
def upload(request):
	dajax = Dajax()
	dajax.assign('#status','innerHTML','clicked')
	return dajax.json()

