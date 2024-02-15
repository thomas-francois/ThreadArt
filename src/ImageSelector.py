from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageEnhance, ImageOps
from ThreadArt import Config as config


class ImageSelector:

	def __init__(self):
		self.isRecording = False
		self.scroll = 1
		self.contrast = 1
		self.brightness = 1

	def start(self):
		self.filePath = self.__chooseFile()
		self.__setup()
		self.baseImage = self.__initiateImage()

		self.fenetre.mainloop()
		return self.outputImage

	def __chooseFile(self):
		validImageTypes = [
			("Image files", "*.jpg"),
			("PNG files", "*.png"),
			("GIF files", "*.gif"),
			("JPEG files", "*.jpeg"),
			("Webp files", "*.webp")
		]

		path = askopenfilename(initialdir=config.sourceFolder, message="Choisir une image", filetypes=validImageTypes)
		if not path:
			exit()
		return path

	def __setup(self):
		self.windowSize = windowSize = [800, 800]
		self.fenetre = Tk()
		self.fenetre.title("Image selector")
		self.fenetre.geometry(f"{windowSize[0]}x{windowSize[1]}+{1440 - windowSize[0]}+{872 - windowSize[1]}")
		self.canvas = Canvas(self.fenetre, height=windowSize[1], width=windowSize[0], bg="#FFF")
		self.canvas.place(x=-3, y=-3)

		style = ttk.Style()
		style.theme_use("clam")
		style.configure("Horizontal.TScale", troughcolor="#c0c0c0", sliderthickness=1, gripcount=0)

		self.canvas.create_text(675, 25, text="Brightness: 0", fill="#F27280", font=("Avenir", 20) ,justify = "center" ,tag = "brightness")
		sliderContrast = ttk.Scale(self.canvas, from_=-100, to=100, length=200, orient="horizontal",
									style="Horizontal.TScale" ,command = lambda event: self.__sliderMove(event ,"brightness"))
		sliderContrast.place(x = 575 ,y = 40)

		self.canvas.create_text(125, 25, text="Contrast: 0", fill="#F27280", font=("Avenir", 20) ,justify = "center" ,tag = "contrast")
		sliderExposure = ttk.Scale(self.canvas, from_=-100, to=100, orient="horizontal", length=200,
									style="Horizontal.TScale" ,command = lambda event: self.__sliderMove(event ,"contrast"))
		sliderExposure.place(x = 25 ,y = 40)

		self.fenetre.bind("<Button-2>", self.__delete)
		self.fenetre.bind("<Button-1>" ,self.__startRecording)
		self.fenetre.bind("<ButtonRelease-1>" ,self.__stopRecording)
		self.fenetre.bind("<Motion>" ,self.__motion)
		self.fenetre.bind("<MouseWheel>", self.__wheel)
		self.fenetre.bind("<Return>", self.__saveImage)

	def __initiateImage(self):
		baseImage = Image.open(self.filePath)
		baseImage = ImageOps.grayscale(baseImage)

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
		self.target = self.canvas.create_image(self.windowSize[0] / 2, self.windowSize[1] / 2, anchor="c", image=photo)
		self.canvas.tag_lower(self.target)

		self.canvas.image = photo

		radius = 300
		self.canvas.create_oval(self.windowSize[0] / 2 + radius, self.windowSize[1] / 2 + radius, self.windowSize[0] / 2 - radius, self.windowSize[1] / 2 - radius, fill = "" ,outline = "#F27280")
		self.canvas.create_rectangle(self.windowSize[0] / 2 + radius, self.windowSize[1] / 2 + radius, self.windowSize[0] / 2 - radius, self.windowSize[1] / 2 - radius, fill = "" ,outline = "#F27280")
		self.canvas.create_text(self.windowSize[0] / 2, 35, text = "Press return to accept", fill = "#F27280" ,font = ("Avenir" ,30))
		return baseImage

	def __adjustImage(self, image):
		contrastEnhancer = ImageEnhance.Contrast(image)
		image = contrastEnhancer.enhance(self.contrast)

		brightnessEnhancer = ImageEnhance.Brightness(image)
		image = brightnessEnhancer.enhance(self.brightness)

		return image

	def __refreshImage(self):
		width = int(self.baseImage.width * self.scroll)
		height = int(self.baseImage.height * self.scroll)

		image = self.baseImage.resize((width, height))
		image = self.__adjustImage(image)
		photo = ImageTk.PhotoImage(image)

		self.canvas.itemconfig(self.target, image=photo)
		self.canvas.image = photo

	def __saveImage(self, event):
		image = self.baseImage
		bbox = self.canvas.bbox(self.target)

		if bbox[0] <= 100 and bbox[1] < 100 and bbox[2] >= 700 and bbox[3] >= 700:
			corner1 = [int((100 - bbox[0]) / self.scroll) ,int((100 - bbox[1]) / self.scroll)]
			corner2 = [int(image.width - (bbox[2] - 700) / self.scroll) ,int(image.height - (bbox[3] - 700) / self.scroll)]

			# Check if it is squared
			if corner2[0] - corner1[0] == corner2[1] - corner1[1]:
				pass
			else:
				corner2[1] = corner2[0] - corner1[0] + corner1[1]


			image = image.crop((corner1[0], corner1[1], corner2[0], corner2[1]))
			self.__refreshImage()
			self.canvas.moveto(self.target, 100, 100)

			image = self.__adjustImage(image)
			self.outputImage = f'{config.sourceFolder}{self.filePath.split("/")[-1].split(".")[0]}-modified.png'
			config.imgPath = self.outputImage
			image.save(self.outputImage, "PNG")
			print(f'Image saved: {self.outputImage}')
			self.__delete()
		else:
			print("/!\\ Image not in place /!\\")

	def __sliderMove(self, event ,mode):
		if mode == "contrast":
			self.contrast = (float(event) + 100) / 100
			self.canvas.itemconfig("contrast" ,text = f"Contrast: {int(float(event))}")
		elif mode == "brightness":
			self.brightness = (float(event) + 100) / 100
			self.canvas.itemconfig("brightness" ,text = f"Brightness: {int(float(event))}")

		self.__refreshImage()

	def __startRecording(self, event):
		if event.y > 50:
			self.offset = self.canvas.bbox(self.target)
			self.offset = [self.offset[0] - event.x ,self.offset[1] - event.y]
			self.isRecording = True

	def __stopRecording(self, event):
		self.isRecording = False

	def __motion(self, event):
		if self.isRecording:
			self.canvas.moveto(self.target, event.x + self.offset[0], event.y + self.offset[1])

	def __wheel(self, event):
		if event.delta > 0:
			self.scroll *= 1.05
		else:
			self.scroll *= 0.95
		self.__refreshImage()

	def __delete(self, event = None):
		self.canvas.delete("all")
		self.fenetre.destroy()
