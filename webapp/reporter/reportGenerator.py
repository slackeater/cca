from webapp.databaseInterface import DbInterface
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,PageBreak,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()


class ReportGenerator():

	def __init__(self,tokenID):
		self.t = DbInterface.getToken(tokenID)

	def accessTokenInfo(self,story):
		strID = str(self.t.id)
		p1 = Paragraph("Access Token ID: <b>" + strID+"</b>", styles['Normal'])
		p2 = Paragraph("User ID: <b>" + str(self.t.userID) + "</b>",styles['Normal'])
		p3 = Paragraph("Stored at: <b>" + str(self.t.tokenTime) + "</b>",styles['Normal'])

		data = [[p1],[p2],[p3]]
		t = Table(data)

		story.append(t)
		story.append(PageBreak())
		return story



	def genPDF(self):
		def myFirstPage(canvas, doc):
				pageinfo = "example"
				canvas.saveState()
				canvas.setFont('Times-Bold',16)
				canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, "Report for access token " + str(self.t.id))
				canvas.setFont('Times-Roman',12)
				canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
				canvas.restoreState()

		def myLaterPages(canvas, doc):
			pageinfo = "example"
			canvas.saveState()
			canvas.setFont('Times-Roman',9)
			canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
			canvas.restoreState()

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
		pageinfo = "platypus example"
		doc = SimpleDocTemplate(response)
		Story = [Spacer(1,2*inch)]
		style = styles["Normal"]

		Story = self.accessTokenInfo(Story)

		for i in range(100):
			bogustext = ("This is Paragraph number %s. " % i) *20
			p = Paragraph(bogustext, style)
			Story.append(p)
			Story.append(Spacer(1,0.2*inch))
			Story.append(p)
			Story.append(PageBreak())


		doc.build(Story,onFirstPage=myFirstPage,onLaterPages=myLaterPages)

		return response

			
		"""fileName = "report"+str(self.t.id)+".pdf"
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
		c = canvas.Canvas(response)	
		text = c.beginText()
		text.setTextOrigin(inch,2.5*inch)
		c.drawText(text)
		c.showPage()
		c.save()
		return response"""

	def tokenInfo():
		pass

