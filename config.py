from random import randint

# -------- Paths --------
sourceFolder = "./Source"
createPathFile = True
pathFileDir = "./Paths"


# ---- Visualisation ----
visualisationLineWidth = 2      # Default : 1
visualisationLineAlpha = 50		# Default : 50 (255 is darker)
visualisationWindowSize = 500 	# Default : 320
visualisationDebug = True


# ----- Calculation -----
numberOfNails = 262				# Default : 300 / 290 /262
minDist = 25					# Default : 30
maxLines = 2500					# Default : 2500
calculationLineWeight = 36		# Default : 40
sourcePhotoContrast = 0.5		# Default : 1 (0 is gray, no max)
sourcePhotoBrightness = 1.1		# Default : 1 (0 is black, no max)


# -------- Batch --------
batchLines = 		{"active": False, "data": [2000 ,2500]}
batchWeights = 		{"active": False, "data": [35 ,36 ,37]}
batchContrasts = 	{"active": False, "data": [(4 + i) / 10 for i in range(2)]}
batchBrignthess =	{"active": False, "data": [(10 + i) / 10 for i in range(2)]}
batchVariations = 0


# -------- Base image --------
imgPath = None


# --- Clémence ---
# imgPath = "./CroppedImages/Try.png"
# imgPath = "./CroppedImages/ClemenceJukata.png"
# imgPath = "./ClemencePath.txt"
# imgPath = "./lastPath.txt"



# --- Candice ---


# --- Parents ---
# imgPath = "./CroppedImages/Parents.png"
# imgPath = "./CroppedImages/Parents2.png"
# imgPath = "./CroppedImages/BackdropBlack2.png"
# imgPath = "./CroppedImages/Backdrop31921.png"  # 3500 / 30 / 1.2 / 1

# --- Lapins ---
# imgPath = "./PinPinUntouched.txt"
# imgPath = "./PinPinTouched.txt"
# imgPath = "./CroppedImages/PinPinTouched-copie.png"  # 2500 / 10 / 0.4 / 1.7
# imgPath = "./CroppedImages/Backdrop43924.png"  # 2500 / 36 / 0.5 / 1.1
imgPath = "./Paths/LapinPath.txt"

# --- Couple ---

#  --- Thomas ---
# imgPath = "./CroppedImages/Portrait3.png"
# imgPath = "./ThomasPath.txt"

# imgPath = "./Paths/HallOfFame/VisuPath.txt"



if __name__ == "__main__":

	batchSettings = [batchLines, batchWeights, batchContrasts, batchBrignthess]

	if batchVariations != 0:
		print("Creating Variations")
		import ThreadBatch
		ThreadBatch.variationPool(batchVariations)
	elif (True in [setting["active"] for setting in batchSettings]):
		print("Creating Batch")
		import ThreadBatch
		ThreadBatch.batchPool(batchSettings)
	else:
		print("Creating single")
		import ThreadPipeline
		ThreadPipeline.start()
