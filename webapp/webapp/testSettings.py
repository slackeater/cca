from settings import *

# make tests faster
SOUTH_TESTS_MIGRATE = False
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'my_db',
		'USER': 'my_user',
		'PASSWORD': '',
		'HOST': '127.0.0.1',
		'PORT': '3307'
	}
}
