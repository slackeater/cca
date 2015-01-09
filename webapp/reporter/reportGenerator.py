from webapp.databaseInterface import DbInterface
from webapp.func import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm,landscape
from reportlab.lib.units import inch
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,PageBreak,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from webapp import constConfig
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from comparator.fileVerifier import Verifier
import math,os,binascii
from clouditem.models import CloudItem 

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

import webapp.crypto

class ReportGenerator():
	""" This class is used to generate report """

	def __init__(self,tokenID):
		self.t = DbInterface.getToken(tokenID)
		self.normalStyle = styles['Normal']
		self.wrappedStyle = styles["BodyText"]

		self.response = HttpResponse(content_type='application/pdf')
		self.response['Content-Disposition'] = 'attachment; filename="report'+str(self.t.id)+'.pdf"'

		self.reportId = str(binascii.hexlify(os.urandom(32)))
		self.genTime = str(timezone.localtime(timezone.now()))

		self.doc = SimpleDocTemplate(self.response,pagesize=landscape(A4))
		self.story = [Spacer(1,2*inch)]


	def firstPage(self):
		""" Generate the firs page of the report """
		
		self.story.append(Paragraph("Report <b>" + self.reportId + "</b>",ParagraphStyle(name="mystyle",fontSize=12,alignment=TA_CENTER)))
		self.story.append(Paragraph("",ParagraphStyle(name="mystyle",fontSize=12,alignment=TA_CENTER)))
		self.story.append(Paragraph("<b>" + self.genTime + "</b>",ParagraphStyle(name="mystyle",fontSize=12,alignment=TA_CENTER)))

	def investigator(self):
		""" Generate the page for the investigator """

		investigator = CloudItem.objects.get(id=self.t.cloudItem.id).reporterID

		self.story.append(Paragraph("Investigator Information",styles['Heading1']))

		data = []
		data.append([Paragraph("Username: <b>" + investigator.username + "</b>",self.normalStyle)])
		data.append([Paragraph("Name: <b>" + investigator.first_name + " " + investigator.last_name +  "</b>",self.normalStyle)])
		data.append([Paragraph("E-Mail: <b>" + investigator.email + "</b>",self.normalStyle)])
			
		t = Table(data)
		t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
				      ]
				     )
			)

		self.story.append(t)

	def downloadInfo(self):
		""" Displays the information about the download """

		self.story.append(Paragraph("Download Information",styles['Heading1']))
		
		d = DbInterface.getDownload(self.t)
		zipVerification = Verifier(self.t).verifyZIP()
		mbSize = float(d.finalFileSize) / math.pow(2,20)

		startT = str(timezone.localtime(d.downTime))
		endT = str(timezone.localtime(d.endDownTime))

		data = []
		data.append([Paragraph("Start Time: <b>" + startT + "</b>",self.normalStyle)])
		data.append([Paragraph("End Time: <b>" + endT + "</b>",self.normalStyle)])
		data.append([Paragraph("Size: <b>" + str(mbSize) + " MB </b>",self.normalStyle)])
		data.append([Paragraph("ZIP Signature Hash: <b>" + d.verificationZIPSignatureHash + " (" + zipVerification['zipHashBase64']  + ")</b>",self.normalStyle)])
		data.append([Paragraph("Digital Timestamp Authoritiy: <b>" + str("https://www.digistamp.com")+ "</b>",self.normalStyle)])

		t = Table(data)
		t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
				      ]
				     )
			)

		self.story.append(t)


	def accessTokenInfo(self):
		""" Displays information about the access token """

		self.story.append(Paragraph("Account and Access Token Summary",styles['Heading1']))
		data = []

		pHead = [Paragraph("<b>Access Token Info</b>",ParagraphStyle(name="mySytle",alignment=TA_CENTER))]
		p1 = Paragraph("Access Token ID: <b>" + str(self.t.id)+"</b>", self.normalStyle)
		p3 = Paragraph("Stored at: <b>" + str(timezone.localtime(self.t.tokenTime)) + "</b>", self.normalStyle)
		data = [[pHead],[p1],[p3]]
		
		userData =  dataDecoder(self.t.userInfo)

		data.append([Paragraph("<b>Account Info</b>",ParagraphStyle(name="mySytle",alignment=TA_CENTER))])

		if self.t.serviceType == constConfig.CSP_DROPBOX:
			data.append([Paragraph("UID: <b>" + str(userData['uid']) + "</b>",self.normalStyle)])	
			data.append([Paragraph("Display Name: <b>" + userData['display_name'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("E-Mail: <b>" + userData['email'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("E-Mail Verified: <b>" + str(userData['email_verified']) + "</b>",self.normalStyle)])	
			data.append([Paragraph("Country: <b>" + userData['country'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("Quota: <b>" + str(userData['quota_info']['quota']) + "(" + str(userData['quota_info']['shared']) + ") shared</b>",self.normalStyle)])	
		elif self.t.serviceType == constConfig.CSP_GOOGLE:
			data.append([Paragraph("UID: <b>" + userData['id'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("Display Name: <b>" + userData['name'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("E-Mail: <b>" + userData['email'] + "</b>",self.normalStyle)])	
			data.append([Paragraph("E-Mail Verified: <b>" + str(userData['verified_email']) + "</b>",self.normalStyle)])	
			data.append([Paragraph("Gender: <b>" + userData.get('gender',"Not set") + "</b>",self.normalStyle)])	
			data.append([Paragraph("Locale: <b>" + userData['locale'] + "</b>",self.normalStyle)])	


		t = Table(data)
		t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
				      ]
				     )
			)

		self.story.append(t)

	def fileInfo(self):
		""" Displays information about the downloaded files """

		history = []
		
		self.story.append(Paragraph("Downloaded Files",styles['Heading1']))
		
		#files
		files = DbInterface.getAllFileDownload(self.t)
		
		data = [[Paragraph("<b>ID</b>",self.normalStyle),
			Paragraph("<b>File Name</b>",self.normalStyle),
			Paragraph("<b>Download Time</b>",self.normalStyle),
			Paragraph("<b>Signature</b>",self.normalStyle)]]

		for f in files:
			line = [Paragraph(str(f.id),self.normalStyle),
				Paragraph(f.fileName,self.wrappedStyle),
				Paragraph(str(timezone.localtime(f.downloadTime)),self.wrappedStyle),
				Paragraph(crypto.sha256(f.fileHash).hexdigest(),self.wrappedStyle)
				]

			data.append(line)
			history.append([f.id,DbInterface.getHistoryForFile(f)])
		
		t = Table(data, colWidths=(2*cm,9*cm,5*cm,8.5*cm))
		t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
				      ]
				     )
			)

		self.story.append(t)
		self.story.append(PageBreak())

		#history
		self.story.append(Paragraph("History",styles['Heading1']))

		histData = [[Paragraph("<b>File ID</b>",self.normalStyle),
			Paragraph("<b>ID</b>",self.normalStyle),
			Paragraph("<b>Revision</b>",self.normalStyle),
			Paragraph("<b>Download Time</b>",self.normalStyle),
			Paragraph("<b>Signature Hash</b>",self.normalStyle)
			]]
		
		for h in history:
			fID = str(h[0])
			fHist = h[1]
			for hist in fHist:
				histData.append([Paragraph(fID,self.normalStyle),
						Paragraph(str(hist.id),self.normalStyle),
						Paragraph(hist.revision,self.normalStyle),
						Paragraph(str(timezone.localtime(hist.downloadTime)),self.normalStyle),
						Paragraph(crypto.sha256(hist.fileRevisionHash).hexdigest(),self.normalStyle)
						])


		t = Table(histData, colWidths=(2*cm,1.5*cm,8*cm,5*cm,8*cm))
		t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
				      ]
				     )
			)
		self.story.append(t)

	def genPDF(self):
		""" Generate the PDF """
		def myFirstPage(canvas, doc):
			canvas.saveState()
			#canvas.setFont('Times-Bold',16)
			#canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, "Report for access token " + str(self.t.id))
			canvas.restoreState()

		def myLaterPages(canvas, doc):
			canvas.saveState()
			canvas.setFont("Helvetica",8.5)
			canvas.drawString(inch, 0.55 * inch, "Page %d" % (doc.page))
			canvas.drawString(7*inch,0.55*inch, self.reportId)
			canvas.restoreState()

		#generation
		self.firstPage()
		self.story.append(PageBreak())
		self.investigator()
		self.story.append(PageBreak())
		self.accessTokenInfo()
		self.story.append(PageBreak())
		self.downloadInfo()
		self.story.append(PageBreak())
		self.fileInfo()
		self.story.append(PageBreak())

		self.doc.build(self.story,onFirstPage=myFirstPage,onLaterPages=myLaterPages)

		return self.response

