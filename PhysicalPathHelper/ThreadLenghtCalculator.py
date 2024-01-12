from math import sin, cos, sqrt ,pi


sequenceFile = "./LapinPath.txt"

radius = 270			# In mm
nailDiameter = 1.8		# In mm


def showInfos(sequenceFile):

	print("Circle diameter :", int(radius / 5) ,"cm")
	print("Nail Diameter :", nailDiameter ,"mm")

	with open(sequenceFile ,"r") as textFile:
		sequence = textFile.read().split("-")[:-1][:-1]

	for i in range(len(sequence)):
		sequence[i] = int(sequence[i])

	nailsCoords = []
	nbrOfNails = max(sequence) + 1
	print("Number of nails :", nbrOfNails)
	print("Number of lines :" ,len(sequence) - 1 ,"\n")
	for i in range(nbrOfNails):
		x = radius * cos(i * 2 * pi / nbrOfNails)
		y = radius * sin(i * 2 * pi / nbrOfNails)
		nailsCoords.append([x, y])



	totalDist = 0
	for i in range(1 ,len(sequence)):
		x = (nailsCoords[sequence[i - 1]][0] - nailsCoords[sequence[i]][0]) ** 2
		y = (nailsCoords[sequence[i - 1]][1] - nailsCoords[sequence[i]][1]) ** 2
		dist = sqrt(x + y)
		totalDist += dist


	AverageDist = round(totalDist / len(sequence))

	print("Average Distance :" ,AverageDist ,"mm")

	totalDist += pi * nailDiameter * len(sequence)
	print("Total lenght :", str(round(totalDist) / 1000) ,"m\n")


	nailsDict = {}
	for i in sequence:
		if i not in nailsDict:
			nailsDict[i] = 1
		else:
			nailsDict[i] += 1


	maxLoops = max(nailsDict.values())
	minLoops = min(nailsDict.values())
	averageLoops = round(sum(nailsDict.values()) / nbrOfNails)
	print(f"Loops by nails : Max = {maxLoops}, Min = {minLoops} ,average = {averageLoops}\n")


if __name__ == '__main__':
	showInfos(sequenceFile)
