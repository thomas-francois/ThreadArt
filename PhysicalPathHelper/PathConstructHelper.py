from tkinter import *
from time import time


def main():
    global canvas ,fenetre ,windowSize ,sequence ,index ,startTime
    windowSize = [750 ,100]
    fenetre = Tk()
    fenetre.title("Path Construction Helper")
    fenetre.geometry(str(windowSize[0]) + "x" + str(windowSize[1]) + "+" + str(1440 - windowSize[0]) + "+" + str(872 - windowSize[1]))
    canvas = Canvas(fenetre ,height = windowSize[1] ,width = windowSize[0] ,bg = "#303841")
    canvas.place(x = -3 ,y = -3)

    with open("LapinPath.txt" ,"r") as f:
        fileContent = f.read()
        sequence = fileContent.split("-")
        print("Sequence length :", len(sequence))

    canvas.create_text(75 ,50 ,text = "288" ,fill = "#556373",font = ("Arial" ,60) ,tag = "-2")
    canvas.create_text(225 ,50 ,text = "288" ,fill = "#8398B0",font = ("Arial" ,65) ,tag = "-1")
    canvas.create_text(375 ,50 ,text = "288" ,fill = "#D4E2F3",font = ("Arial" ,70) ,tag = "+0")
    canvas.create_text(525 ,50 ,text = "288" ,fill = "#8398B0",font = ("Arial" ,65) ,tag = "+1")
    canvas.create_text(675 ,50 ,text = "288" ,fill = "#556373",font = ("Arial" ,60) ,tag = "+2")
    index -= 1
    changeDisplay(index)
    startTime = time()

    fenetre.bind("<space>" ,forward)
    fenetre.bind("<Right>" ,forward)
    fenetre.bind("<Left>" ,back)
    fenetre.protocol("WM_DELETE_WINDOW", onClosing)
    fenetre.mainloop()


def forward(event):
    global index
    index += 1
    changeDisplay(index)
    fenetre.title("Point : " + str(index))


def back(event):
    global index
    index -= 1
    changeDisplay(index)
    fenetre.title("Point : " + str(index))


def changeDisplay(index):
    canvas.itemconfigure("-2" ,text = str(sequence[index - 2]))
    canvas.itemconfigure("-1" ,text = str(sequence[index - 1]))
    canvas.itemconfigure("+0" ,text = str(sequence[index + 0]))
    canvas.itemconfigure("+1" ,text = str(sequence[index + 1]))
    canvas.itemconfigure("+2" ,text = str(sequence[index + 2]))


def onClosing():
    print("Index :", index)
    print("Time spent :", round((time() - startTime) / 60 ,2), "min")
    fenetre.destroy()


if __name__ == '__main__':
    index = [160, 461, 667, 1012, 1175, 1343][-1]
    timesInMin = [23, 42, 27, 47, 25, 41]
    main()

# Clémence:
# Threads = [201, 446 ,774 ,978, 1304 ,1601 ,1841 ,2209 ,2399 ,2459]
# Interval = [47 ,37 ,41 ,26 ,44 ,42 ,36 ,51 ,29 ,16]
