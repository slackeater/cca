import os,shutil,Image

class Thubmnailer():

	def cacheImg(self,imgSrc,imgDest,maxHeigth = 800, maxWidth= 600):
		if not os.path.isfile(imgDest):
			shutil.copy2(imgSrc,imgDest)	

		#resize images
		im = Image.open(imgDest)
		startWidth,startHeight = im.size
		newWidth,newHeight = self.computeThumbnailSize(startWidth, startHeight,float(maxHeigth),float(maxWidth))
		im.thumbnail((newWidth,newHeight),Image.ANTIALIAS)
		im.save(imgDest,"PNG")

	def computeThumbnailSize(self,startWidth,startHeight,maxHeight,maxWidth):
		maxHeight = maxHeight
		maxWidth = maxWidth
		ratio = float(0)
		newHeight = 0

		if startWidth > maxWidth:
			newWidth = (startWidth-(startWidth-maxWidth))
			ratio = float(newWidth/startWidth)
		else:
			newWidth = startWidth

		if ratio != 0:
			newHeight = startHeight-(startHeight*ratio)
		elif ratio == 0 and startHeight > maxHeight:
			newHeight = (startHeight-(startHeight-maxHeight))

		return int(newWidth),int(newHeight)
