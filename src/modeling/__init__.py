from .listModels import *
from .NNModel import *

from sklearn.model_selection import train_test_split

def newNNModel(model_func, csv, cols, test_size = 0.3):
	x_train, x_test, y_train, y_test = train_test_split(csv[cols.drop("pub")], csv.pub, test_size = test_size, random_state = 42)

	NN = NNModel(model_func(len(cols) - 1))
	NN.fit(x_train, y_train, 150, 10)
	y_pred = NN.predict(x_test)

	NN.printScore(y_test, y_pred)

	return NN

def importNNModel(csv, cols, test_size = 0.3):
	x_train, x_test, y_train, y_test = train_test_split(csv[cols.drop("pub")], csv.pub, test_size = test_size, random_state = 42)

	NN = NNModel()
	NN.read("model")

	return NN

print("""-------------------------------
newNNModel(model_func, csv, cols, optional test_size):
	model_func is whatever which Neural Network model you want. You can use one of listModels.py
	csv is the dataframe
	cols are the columns used in csv (include "pub" too)
	test_size is the ratio between train size and test size
-------------------------------""")