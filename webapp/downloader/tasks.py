from __future__ import absolute_import

from celery import shared_task
from downloader.models import AccessToken,Download
from django.db import transaction
from .googleDownloader import GoogleDownloader
from .dropDownloader import DropboxDownloader
from webapp.exceptionFormatter import formatException
from webapp import constConfig

@shared_task
def download(downloadDB,uname,pwd):
	""" This function is used to start an asynchrounous download with celery """
	downloader = None

	if downloadDB.tokenID.serviceType == constConfig.CSP_GOOGLE:
		downloader = GoogleDownloader(downloadDB,uname,pwd)
	elif downloadDB.tokenID.serviceType == constConfig.CSP_DROPBOX:
		downloader = DropboxDownloader(downloadDB,uname,pwd)

	if downloader is not None:
		try:
			#reset
			downloadDB.threadMessage = "-"
			downloadDB.save()

			#do not mess up the order of these call
			downloader.verfiyCredentials()
			downloader.createService()
			downloader.downloadMetaData()
			downloader.computeDownload()

			with transaction.atomic():
				downloader.downloadFileHistory()
				downloader.verificationProcess()	

		except Exception as e:
			downloadDB.threadStatus = constConfig.THREAD_STOP
			downloadDB.threadMessage = formatException(e)
			downloadDB.save()
