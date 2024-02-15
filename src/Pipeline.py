from ThreadArt import Config as config
from src.ImageSelector import ImageSelector
from src.Generator import Generator
from src.Visualization import Visualization
from src.Batching import Batching, Variation


class Generate:

	def __init__(self, humanPath = False, forceSingle = False):
		self.humanPath = humanPath
		self.forceSingle = forceSingle
		self.__dispach()

	def __dispach(self):
		batchSettings = [config.batchLines, config.batchWeights, config.batchContrasts, config.batchBrignthess]

		if self.forceSingle or config.imgPath is None:
			self.run()
		elif int(config.batchVariations) > 1:
			print("Creating Variations...")
			Variation()
		elif (True in [setting["active"] for setting in batchSettings]):
			print("Creating Batch...")
			Batching(batchSettings)
		else:
			print("Creating Single...")
			self.run()


	def run(self):
		file = config.imgPath

		if file is None:
			file = ImageSelector().start()

		if not file.endswith(".txt"):
			sequence = Generator(file).start()
			if config.createPathFile:
				self.createPath(sequence)
		else:
			with open(file ,"r") as f:
				sequence = f.read().replace("\n" ,"").split(", ")[:-1]

		Visualization(sequence).start()


	def createPath(self, sequence):
		if config.createPathFile:
			with open(config.pathFolder + "lastPath.txt" ,"w") as textFile:
				nbrPerLine = 20
				for i in range(0 ,len(sequence)):
					textFile.write(str(sequence[i]) + ", ")

					if (i + 1) % nbrPerLine == 0:
						textFile.write("\n")
