from math import sin, cos, pi
from PIL import Image, ImageDraw
from ThreadArt import Config as config


class Visualization:

	def __init__(self, sequence, maxLines = -1):
		self.sequence = sequence
		self.size = config.visualisationWindowSize
		self.baseImage = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 255))
		self.maxLines = maxLines

	def start(self):
		print("Starting visualisation...")

		nailsCoords = []
		radius = self.size / 2 - 10
		for i in range(config.numberOfNails):
			x = round(radius * cos(-i * 2 * pi / config.numberOfNails + pi) + self.size / 2)
			y = round(radius * sin(-i * 2 * pi / config.numberOfNails + pi) + self.size / 2)
			nailsCoords.append([x, y])

		last = 0
		for nailIndex in self.sequence[1:self.maxLines]:
			self.__addTransparentLine(self.baseImage ,nailsCoords[int(last)] ,nailsCoords[int(nailIndex)] ,config.visualisationLineAlpha)
			last = nailIndex

		if config.visualisationDebug:
			self.baseImage = self.__addInfos(self.baseImage)
		self.baseImage.show()
		if config.createResultImage:
			sourceName = config.imgPath.split("/")[-1].split(".")[0]
			self.baseImage.save(f"{config.resultFolder}{sourceName}.png", "PNG")
		print("Finished")

	def __addTransparentLine(self, image ,start ,end ,alpha):
		overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
		draw = ImageDraw.Draw(overlay)
		draw.line([tuple(start), tuple(end)], fill = (0, 0, 0, alpha), width = config.visualisationLineWidth)
		self.baseImage = Image.alpha_composite(image, overlay)

	def __addInfos(self, image):
		textTop = f"Source: {config.imgPath}\nLines: {config.maxLines}\nWeight: {config.calculationLineWeight}"
		textBottom = f"Contrast: {config.sourcePhotoContrast}\nBrightness: {config.sourcePhotoBrightness}"
		draw = ImageDraw.Draw(image)
		draw.text((0, 0), textTop ,fill = "red")
		draw.text((0, config.visualisationWindowSize - 30), textBottom ,fill = "red")
		return image
