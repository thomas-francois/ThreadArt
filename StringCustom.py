import math
from PIL import Image ,ImageEnhance
import numpy as np
from time import time
import multiprocessing
from ProgressBar import ProgressBar
import config

PINS = config.numberOfNails
MIN_DISTANCE = config.minDist
MAX_LINES = config.maxLines
LINE_WEIGHT = config.calculationLineWeight


# Only for manual testing:
IMG_PATH = "./CroppedImages/Try.png"
IMG_SIZE = 375


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    t = time()
    print("Importing File           ", end = "")
    importPictureAndGetPixelArray()

    print(" Done\nCalculating Pin Coords   ", end = "")
    calculatePinCoords()

    print(" Done\nCreating Lines Cache     ", end = "")
    precalculateAllPotentialLines()

    print(" Done\nCalculating path         ", end = "")
    sequence = calculateLines()
    print(f" Done\nTime : {round(time() - t, 2)}s")
    return sequence


def importPictureAndGetPixelArray():
    global SourceImage

    with open(IMG_PATH ,"rb") as imageFile:
        image = Image.open(imageFile).convert("L")

        contrastEnhancer = ImageEnhance.Contrast(image)
        image = contrastEnhancer.enhance(config.sourcePhotoContrast)

        brightnessEnhancer = ImageEnhance.Brightness(image)
        image = brightnessEnhancer.enhance(config.sourcePhotoBrightness)

        SourceImage = np.array(image).flatten()


def calculatePinCoords():
    global pinCoords
    pinCoords = []
    center = IMG_SIZE / 2
    radius = IMG_SIZE / 2 - 1
    for i in range(PINS):
        angle = 2 * math.pi * i / PINS

        pinCoords.append(Coord(math.floor(center + radius * math.cos(angle)),
                                math.floor(center + radius * math.sin(angle))))


def precalculateAllPotentialLines():
    global lineCache_y ,lineCache_x
    lineCache_y = np.empty((PINS * PINS), dtype = object)
    lineCache_x = np.empty((PINS * PINS), dtype = object)

    for i in range(PINS):
        for j in range(i + MIN_DISTANCE, PINS):
            x0 = pinCoords[i].x
            y0 = pinCoords[i].y
            x1 = pinCoords[j].x
            y1 = pinCoords[j].y

            dist = math.floor(math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
            xs = np.linspace(x0, x1, dist ,dtype = int)
            ys = np.linspace(y0, y1, dist ,dtype = int)

            lineCache_y[j * PINS + i] = ys
            lineCache_y[i * PINS + j] = ys
            lineCache_x[j * PINS + i] = xs
            lineCache_x[i * PINS + j] = xs


def calculateLines():
    global lineCache_y ,lineCache_x

    error = np.subtract(np.multiply(np.ones(IMG_SIZE ** 2), 255), SourceImage)
    line_sequence = [0]
    currentPin = 0
    lastPins = [0] * 20

    for i in range(MAX_LINES):
        maxError = 0

        for offset in range(MIN_DISTANCE, PINS - MIN_DISTANCE):
            testPin = (currentPin + offset) % PINS
            if testPin in lastPins:
                continue
            else:
                innerIndex = testPin * PINS + currentPin
                lineError = getLineErr(error, lineCache_y[innerIndex], lineCache_x[innerIndex])
                if lineError > maxError:
                    maxError = lineError
                    bestPin = testPin
                    index = innerIndex

        line_sequence.append(bestPin)
        coords1 = lineCache_y[index]
        coords2 = lineCache_x[index]

        for i in range(len(coords1)):
            v = int((coords1[i] * IMG_SIZE) + coords2[i])
            error[v] = error[v] - LINE_WEIGHT

        lastPins.append(bestPin)
        lastPins.pop(0)
        currentPin = bestPin

    return line_sequence


def getLineErr(errors, coords1, coords2):
    indices = (coords1 * IMG_SIZE + coords2).astype(int)
    sumError = errors[indices].sum()
    return sumError


def profile():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="Profile2.prof")


count = 0
if __name__ == "__main__":
    # main()
    profile()

# Based on https://github.com/halfmonty/StringArtGenerator
