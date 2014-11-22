from django.test.runner import DiscoverRunner
from django.test import TestCase
from django.conf import settings
from dbMaker import MakeDatabase


class CcaRunner(DiscoverRunner):

	def setup_databases(self,**kwargs):
		print "Creating and populating DB..."
		superDb = super(CcaRunner,self).setup_databases(**kwargs)
		db = MakeDatabase()
		db.populate()
		return superDb


	def teardown_databases(self,old_config,**kwargs):
		print "Disconnecting..."
		return super(CcaRunner,self).teardown_databases(old_config,**kwargs)
