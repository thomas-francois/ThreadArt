import multiprocessing
from random import randint
import config
from itertools import product


def batchWorker(setting):
	if setting[0] is not None:
		config.maxLines = int(setting[0])
	if setting[1] is not None:
		config.calculationLineWeight = int(setting[1])
	if setting[2] is not None:
		config.sourcePhotoContrast = float(setting[2])
	if setting[3] is not None:
		config.sourcePhotoBrightness = float(setting[3])
	import ThreadPipeline
	ThreadPipeline.start()


def batchPool(batchSettings):
	settings = []
	for setting in batchSettings:
		if setting["active"]:
			settings.append(setting["data"])
		else:
			settings.append([None])
	differentSettings = [list(combination) for combination in product(*settings)]

	processes = []
	for s in differentSettings:
		process = multiprocessing.Process(target = batchWorker ,args = (s, ))
		processes.append(process)
		process.start()

	for process in processes:
		process.join()


def variationWorker():
	config.maxLines += randint(-750 ,750)
	config.calculationLineWeight += randint(-15 ,15)
	config.sourcePhotoContrast += randint(-5 ,5) / 10.
	config.sourcePhotoBrightness += randint(-5 ,5) / 10.
	import ThreadPipeline
	ThreadPipeline.start()


def variationPool(nbr):
	processes = []
	for _ in range(nbr):
		process = multiprocessing.Process(target = variationWorker)
		processes.append(process)
		process.start()

	for process in processes:
		process.join()
