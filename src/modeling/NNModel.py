from keras.models import model_from_json
from sklearn import metrics

class NNModel:
	def __init__(self, model = None):
		self.model = model

	def fit(self, X_train, Y_train, epochs = 150, batch_size = 10):
		if self.model != None:
			self.model.fit(X_train, Y_train, epochs = epochs, batch_size = batch_size)

	def predict(self, X_test):
		if self.model == None:
			return

		return self.model.predict(X_test)

	def printScore(self, y_test, y_pred):
		score = metrics.confusion_matrix(y_test.round(), y_pred.round())
		print("accuracy: " + str((score[0][0] + score[1][1]) / len(y_test)) + "%")
		precision = score[1][1] / (score[0][1] + score[1][1])
		print("precision: " + str(precision) + "%")
		recall = score[1][1] / (score[1][1] + score[1][0])
		print("recall: " + str(recall) + "%")
		print("f1-score: " + str(2 * (precision * recall) / (precision + recall)) + "%")

	def save(self, fileName):
		if self.model == None:
			return

		model_json = self.model.to_json()

		with open("model/" + fileName + ".json", "w") as json_file:
			json_file.write(model_json);

		self.model.save_weights("model/" + fileName + "model.h5")

	def read(self, fileName):
		json_file = open("model/" + fileName + ".json", "r")
		model_json = json_file.read()
		json_file.close()

		self.model = model_from_json(model_json)
		self.model.load_weights("model/" + fileName + ".h5")