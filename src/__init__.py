from .modeling import *
from .processing import *

import pandas as pd
import os

def saveCsv(csv, fileName, force = False):
	if os.path.exists("data/generated/" + fileName + ".csv"):
		print("This file already exists. Can't save it")
		print("Use 'force' argument to override it")
		return

	csv.to_csv("data/generated/" + fileName + ".csv", index = False)

def readCsv(fileName = "data_full.csv"):
	if not os.path.exists("data/generated/" + fileName):
		print("This data/generated/" + fileName + " file does not exists")
		return

	return pd.read_csv("data/generated/" + fileName)

print("""-------------------------------
readCsv(optional fileName):
	return the generated data from fileName

saveCsv(csv, fileName, optional force):
	Save csv in data/generated/fileName.csv
	If the file does already exists, you can force the Save with "force = True"
-------------------------------""")
