import multiprocessing
from random import randint
from itertools import product
from ThreadArt import Config as config
import src.Pipeline as Pipeline


class Variation:

	def __init__(self):
		config.createPathFile = False
		config.createResultImage = False
		self.start()

	def variationWorker(self):
		config.maxLines += randint(-750 ,750)
		config.calculationLineWeight += randint(-15 ,15)
		config.sourcePhotoContrast += randint(-5 ,5) / 10.
		config.sourcePhotoBrightness += randint(-5 ,5) / 10.
		Pipeline.Generate(forceSingle = True)

	def start(self):
		processes = []
		for _ in range(config.batchVariations):
			process = multiprocessing.Process(target = self.variationWorker)
			processes.append(process)
			process.start()

		for process in processes:
			process.join()


class Batching:

	def __init__(self, batchSettings):
		config.createPathFile = False
		config.createResultImage = False
		self.batchSettings = batchSettings
		self.start()

	def batchWorker(self, setting):
		if setting[0] is not None:
			config.maxLines = int(setting[0])
		if setting[1] is not None:
			config.calculationLineWeight = int(setting[1])
		if setting[2] is not None:
			config.sourcePhotoContrast = float(setting[2])
		if setting[3] is not None:
			config.sourcePhotoBrightness = float(setting[3])
		Pipeline.Generate(forceSingle = True)

	def start(self):
		settings = []
		for setting in self.batchSettings:
			if setting["active"]:
				settings.append(setting["data"])
			else:
				settings.append([None])
		differentSettings = [list(combination) for combination in product(*settings)]

		processes = []
		for s in differentSettings:
			process = multiprocessing.Process(target = self.batchWorker ,args = (s, ))
			processes.append(process)
			process.start()

		for process in processes:
			process.join()
