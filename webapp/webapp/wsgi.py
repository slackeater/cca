"""
WSGI config for webapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os,sys

#sys.path.append("/var/www/cca/toolkit/")
#sys.path.append("/var/www/cca/toolkit/webapp")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
os.environ["HTTPS"] = "on"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
