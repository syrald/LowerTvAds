import pandas as pd

from sklearn import metrics

# Model part
from sklearn.model_selection import train_test_split
def split(cols, test_size = 0.3):
	global x_train, x_test, y_train, y_test
	x_train, x_test, y_train, y_test = train_test_split(csv[cols], csv.pub, test_size = test_size, random_state = 42)

def trainModel(model_func):
	# Construct model
	print("Train the model")

	global model
	model = model_func(x_train, y_train, x_train.columns)
	y_pred = model.predict(x_test)

	global score
	score = metrics.confusion_matrix(y_test.round(), y_pred.round())
	print("accuracy: " + str((score[0][0] + score[1][1]) / len(x_test)) + "%")
	precision = score[1][1] / (score[0][1] + score[1][1])
	print("precision: " + str(precision) + "%")
	recall = score[1][1] / (score[1][1] + score[1][0])
	print("recall: " + str(recall) + "%")
	print("f1-score: " + str(2 * (precision * recall) / (precision + recall)) + "%")

