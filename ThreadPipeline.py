import config
import ThreadImageSelector
import StringCustom
import ThreadVisuClean
from PIL import Image


def getBaseImage():
	if config.imgPath is None:
		choosenFile = ThreadImageSelector.main()
	elif config.imgPath[-4:] == ".txt":
		with open(config.imgPath ,"r") as textFile:
			sequence = textFile.read().replace("\n" ,"").split(", ")[:-1]
		ThreadVisuClean.createVisu(sequence)
		exit()
	else:
		choosenFile = config.imgPath

	StringCustom.IMG_PATH = choosenFile


	with open(choosenFile ,"rb") as imageFile:
		image = Image.open(imageFile).convert("L")
		StringCustom.IMG_SIZE = image.size[0]


def createPath(sequence):
	if config.createPathFile:
		with open(config.pathFileDir + "/lastPath.txt" ,"w") as textFile:
			nbrPerLine = 20
			for i in range(0 ,len(sequence)):
				textFile.write(str(sequence[i]) + ", ")

				if (i + 1) % nbrPerLine == 0:
					textFile.write("\n")


def createHumanPath(sequence):
	if config.createPathFile:
		with open(config.pathFileDir + "/lastPath.txt" ,"w") as textFile:
			nbrPerLine = 20
			for i in range(0 ,len(sequence)):
				if i == nbrPerLine / 2:
					textFile.write("--")

				if (i + 1) % nbrPerLine == 0:
					textFile.write(str(sequence[i]).rjust(3 ," ") + "\n")
				else:
					textFile.write(str(sequence[i]).rjust(3 ," ") + " | ")

				if ((i + 1) % nbrPerLine) == nbrPerLine / 2:
					textFile.write("-- | ")
				textFile.write(str(sequence[i]) + "-")


def start():
	getBaseImage()
	sequence = StringCustom.main()
	createPath(sequence)
	ThreadVisuClean.createVisu(sequence)


if __name__ == '__main__':
	start()
