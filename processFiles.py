import pandas as pd
import os.path

from keras.models import model_from_json

def saveCsv(fileName, force = False):
	if os.path.exists("generated/" + fileName + ".csv"):
		print("This file already exists. Can't save it")
		print("Use 'force' argument to override it")
		return

	csv.to_csv("generated/" + fileName + ".csv", index = False)

def readCsv():
	global csv
	if not os.path.exists("generated/data1.csv"):
		print("This generated/data1.csv file does not exists")
		return

	csv1 = pd.read_csv("generated/data1.csv")

	if not os.path.exists("generated/data2.csv"):
		print("This generated/data2.csv file does not exists")
		return
	csv2 = pd.read_csv("generated/data2.csv")

	csv = csv1.append(csv2)

def saveModel(model):
	model_json = model.to_json()

	with open("generated/model.json", "w") as json_file:
		json_file.write(model_json);

	model.save_weights("generated/model.h5")

def readModel():
	json_file = open("generated/model.json", "r")
	model_json = json_file.read()
	json_file.close()

	model = model_from_json(model_json)
	model.load_weights("generated/model.h5")
	return model
