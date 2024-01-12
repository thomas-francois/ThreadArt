from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance ,ImageOps
import config


def chooseFile():
	validImageTypes = [
		("Image files", "*.jpg"),
		("PNG files", "*.png"),
		("GIF files", "*.gif"),
		("JPEG files", "*.jpeg")
	]

	path = askopenfilename(initialdir=config.sourceFolder,
							message="Choisir une image",
							filetypes=validImageTypes)
	if not path:
		exit()
	return path


def main():
	global canvas, fenetre, windowSize
	global file ,isRecording ,scroll ,contrast ,brightness ,endFile

	file = chooseFile()
	isRecording = False
	scroll = 1
	contrast = 1
	brightness = 1
	endFile = None

	windowSize = [800, 800]
	fenetre = Tk()
	fenetre.title("Image selector")
	fenetre.geometry(str(windowSize[0]) + "x" + str(windowSize[1]) + "+"
					+ str(1440 - windowSize[0]) + "+" + str(872 - windowSize[1]))
	canvas = Canvas(fenetre, height=windowSize[1], width=windowSize[0], bg="#FFF")
	canvas.place(x=-3, y=-3)

	setupImage()
	createSliders()

	fenetre.bind("<Button-2>", delete)
	fenetre.bind("<Button-1>" ,startRecording)
	fenetre.bind("<ButtonRelease-1>" ,stopRecording)
	fenetre.bind("<Motion>" ,motion)
	fenetre.bind("<MouseWheel>", wheel)
	fenetre.bind("<Return>", saveImage)
	fenetre.mainloop()
	return endFile


def setupImage():
	global target ,baseImage

	baseImage = Image.open(file)
	# baseImage = ImageOps.invert(baseImage)
	original_width, original_height = baseImage.size
	if original_width < original_height:
	    new_width = 800
	    new_height = int(original_height * (800 / original_width))
	else:
	    new_height = 800
	    new_width = int(original_width * (800 / original_height))

	# Resize the image to the new dimensions
	baseImage = baseImage.resize((new_width, new_height), Image.ANTIALIAS)

	photo = ImageTk.PhotoImage(baseImage)
	target = canvas.create_image(windowSize[0] / 2, windowSize[1] / 2, anchor="c", image=photo)

	canvas.image = photo

	radius = 300
	canvas.create_oval(windowSize[0] / 2 + radius, windowSize[1] / 2 + radius, windowSize[0] / 2 - radius, windowSize[1] / 2 - radius, fill = "" ,outline = "#F27280")
	canvas.create_rectangle(windowSize[0] / 2 + radius, windowSize[1] / 2 + radius, windowSize[0] / 2 - radius, windowSize[1] / 2 - radius, fill = "" ,outline = "#F27280")
	canvas.create_text(windowSize[0] / 2, 35, text = "Press return to accept", fill = "#F27280" ,font = ("Avenir" ,30))


def createSliders():
	style = ttk.Style()
	style.theme_use("clam")
	style.configure("Horizontal.TScale", troughcolor="#c0c0c0", sliderthickness=1, gripcount=0)

	canvas.create_text(675, 25, text="Brightness: 0", fill="#F27280", font=("Avenir", 20) ,justify = "center" ,tag = "brightness")
	sliderContrast = ttk.Scale(canvas, from_=-100, to=100, length=200, orient="horizontal",
								style="Horizontal.TScale" ,command = lambda event: sliderMove(event ,"brightness"))
	sliderContrast.place(x = 575 ,y = 40)

	canvas.create_text(125, 25, text="Contrast: 0", fill="#F27280", font=("Avenir", 20) ,justify = "center" ,tag = "contrast")
	sliderExposure = ttk.Scale(canvas, from_=-100, to=100, orient="horizontal", length=200,
								style="Horizontal.TScale" ,command = lambda event: sliderMove(event ,"contrast"))
	sliderExposure.place(x = 25 ,y = 40)


def sliderMove(event ,mode):
	global contrast ,brightness
	if mode == "contrast":
		contrast = (float(event) + 100) / 100
		canvas.itemconfig("contrast" ,text = f"Contrast: {int(float(event))}")
	elif mode == "brightness":
		brightness = (float(event) + 100) / 100
		canvas.itemconfig("brightness" ,text = f"Brightness: {int(float(event))}")

	updateImage()


def startRecording(event):
	global isRecording ,offset
	if event.y > 50:
		offset = canvas.bbox(target)
		offset = [offset[0] - event.x ,offset[1] - event.y]
		isRecording = True


def stopRecording(event):
	global isRecording
	isRecording = False


def motion(event):
	global offset
	if isRecording:
		canvas.moveto(target, event.x + offset[0], event.y + offset[1])


def wheel(event):
	global scroll
	if event.delta > 0:
		scroll *= 1.05
	else:
		scroll *= 0.95
	updateImage()


def updateImage():
	width = int(baseImage.width * scroll)
	height = int(baseImage.height * scroll)

	image = baseImage.resize((width, height))
	image = adjustImage(image)
	photo = ImageTk.PhotoImage(image)

	canvas.itemconfig(target, image=photo)
	canvas.image = photo


def adjustImage(image):
	contrastEnhancer = ImageEnhance.Contrast(image)
	image = contrastEnhancer.enhance(contrast)

	brightnessEnhancer = ImageEnhance.Brightness(image)
	image = brightnessEnhancer.enhance(brightness)

	return image


def saveImage(event):
	global baseImage ,endFile

	bbox = canvas.bbox(target)
	if bbox[0] <= 100 and bbox[1] < 100 and bbox[2] >= 700 and bbox[3] >= 700:
		corner1 = [int((100 - bbox[0]) / scroll) ,int((100 - bbox[1]) / scroll)]
		corner2 = [int(baseImage.width - (bbox[2] - 700) / scroll) ,int(baseImage.height - (bbox[3] - 700) / scroll)]

		# Check if it is squared
		if corner2[0] - corner1[0] == corner2[1] - corner1[1]:
			pass
		else:
			corner2[1] = corner2[0] - corner1[0] + corner1[1]


		baseImage = baseImage.crop((corner1[0], corner1[1], corner2[0], corner2[1]))
		updateImage()
		canvas.moveto(target, 100, 100)

		baseImage = adjustImage(baseImage)
		baseImage.save("./ColorVisualisation/" + file.split("/")[-1].split(".")[0] + ".png", "PNG")
		endFile = "./CroppedImages/" + file.split("/")[-1].split(".")[0] + ".png"
		print(f"Image saved: {endFile}")
		delete("")

	else:
		print("/!\\ Image not in place /!\\")


def delete(event):
	canvas.delete("all")
	fenetre.destroy()


if __name__ == '__main__':
	main()
