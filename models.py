from keras.models import Sequential
from keras.layers import Dense
from sklearn.linear_model import LogisticRegression

def model1(X, Y, nbCols):
	model = Sequential()
	model.add(Dense(20, input_dim = nbCols, activation = 'relu'))
	model.add(Dense(12, activation = 'relu'))
	model.add(Dense(6, activation = 'relu'))
	model.add(Dense(1, activation = 'sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(X, Y, epochs = 150, batch_size = 10)
	return model

def model2(X, Y, nbCols):
	model = Sequential()
	model.add(Dense(32, input_dim = nbCols, activation = 'relu'))
	model.add(Dense(20, activation = 'relu'))
	model.add(Dense(12, activation = 'relu'))
	model.add(Dense(6, activation = 'relu'))
	model.add(Dense(1, activation = 'sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(X, Y, epochs = 150, batch_size = 10)
	return model

def model3(X, Y, nbCols):
	model = Sequential()
	model.add(Dense(32, input_dim = nbCols, activation = 'relu'))
	model.add(Dense(20, activation = 'relu'))
	model.add(Dense(12, activation = 'relu'))
	model.add(Dense(12, activation = 'relu'))
	model.add(Dense(6, activation = 'relu'))
	model.add(Dense(1, activation = 'sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(X, Y, epochs = 150, batch_size = 10)
	return model

def model4(X, Y, nbCols):
	return LogisticRegression(random_state = 42).fit(X, Y.apply(lambda x: x >= 0.5))