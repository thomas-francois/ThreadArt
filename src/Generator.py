import math
from PIL import Image ,ImageEnhance
import numpy as np
from time import time
from ThreadArt import Config as config

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


class Generator:
    def __init__(self, imagePath):
        self.PINS = config.numberOfNails
        self.MIN_DISTANCE = config.minDist
        self.MAX_LINES = config.maxLines
        self.LINE_WEIGHT = config.calculationLineWeight
        self.IMG_PATH = imagePath
        self.IMG_SIZE = 0

    def start(self):
        t = time()
        # print("Importing File           ", end = "")
        self.SourceImage = self.__importPictureAndGetPixelArray()

        # print(" Done\nCalculating Pin Coords   ", end = "")
        self.__calculatePinCoords()

        # print(" Done\nCreating Lines Cache     ", end = "")
        self.__precalculateAllPotentialLines()

        # print(" Done\nCalculating path         ", end = "")
        sequence = self.__calculateLines()
        print(f"Finished in {round(time() - t, 2)}s")
        return sequence

    def __importPictureAndGetPixelArray(self):
        with open(self.IMG_PATH ,"rb") as imageFile:
            image = Image.open(imageFile).convert("L")

            contrastEnhancer = ImageEnhance.Contrast(image)
            image = contrastEnhancer.enhance(config.sourcePhotoContrast)

            brightnessEnhancer = ImageEnhance.Brightness(image)
            image = brightnessEnhancer.enhance(config.sourcePhotoBrightness)

            self.IMG_SIZE = image.size[0]

            return np.array(image).flatten()

    def __calculatePinCoords(self):
        self.pinCoords = []
        center = self.IMG_SIZE / 2
        radius = self.IMG_SIZE / 2 - 1
        for i in range(self.PINS):
            angle = 2 * math.pi * i / self.PINS

            self.pinCoords.append(Coord(math.floor(center + radius * math.cos(angle)),
                                    math.floor(center + radius * math.sin(angle))))

    def __precalculateAllPotentialLines(self):
        self.lineCache_y = np.empty((self.PINS * self.PINS), dtype = object)
        self.lineCache_x = np.empty((self.PINS * self.PINS), dtype = object)

        for i in range(PINS):
            for j in range(i + MIN_DISTANCE, PINS):
                x0 = self.pinCoords[i].x
                y0 = self.pinCoords[i].y
                x1 = self.pinCoords[j].x
                y1 = self.pinCoords[j].y

                dist = math.floor(math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
                xs = np.linspace(x0, x1, dist ,dtype = int)
                ys = np.linspace(y0, y1, dist ,dtype = int)

                self.lineCache_y[j * self.PINS + i] = ys
                self.lineCache_y[i * self.PINS + j] = ys
                self.lineCache_x[j * self.PINS + i] = xs
                self.lineCache_x[i * self.PINS + j] = xs

    def __calculateLines(self):
        error = np.subtract(np.multiply(np.ones(self.IMG_SIZE ** 2), 255), self.SourceImage)
        line_sequence = [0]
        currentPin = 0
        lastPins = [0] * 20

        for i in range(self.MAX_LINES):
            maxError = 0

            for offset in range(self.MIN_DISTANCE, self.PINS - self.MIN_DISTANCE):
                testPin = (currentPin + offset) % self.PINS
                if testPin in lastPins:
                    continue
                else:
                    innerIndex = testPin * self.PINS + currentPin
                    lineError = self.__getLineErr(error, self.lineCache_y[innerIndex], self.lineCache_x[innerIndex])
                    if lineError > maxError:
                        maxError = lineError
                        bestPin = testPin
                        index = innerIndex

            line_sequence.append(bestPin)
            coords1 = self.lineCache_y[index]
            coords2 = self.lineCache_x[index]

            for i in range(len(coords1)):
                v = int((coords1[i] * self.IMG_SIZE) + coords2[i])
                error[v] = error[v] - self.LINE_WEIGHT

            lastPins.append(bestPin)
            lastPins.pop(0)
            currentPin = bestPin

        return line_sequence

    def __getLineErr(self, errors, coords1, coords2):
        indices = (coords1 * self.IMG_SIZE + coords2).astype(int)
        sumError = errors[indices].sum()
        return sumError
