import librosa

import numpy as np

class Frames:
	def __init__(self, filePath, MFCC = True, DB = True):
		# File variables
		audio, self.framerate = librosa.load(filePath, sr = 44100, res_type = "kaiser_fast")

		# To iterate the file
		self.iterator = 0
		self.padding = self.framerate * 10

		# Activate or not features
		self.activMFCC = MFCC
		self.activDB = DB
		if self.activDB:
			self.DB = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100]

		# Add zeros before and after the file
		# Also fill the last element to be the same length as the others
		borders = np.zeros(self.padding, dtype = np.float32)
		fill = np.zeros(self.framerate - (len(audio) % self.framerate), dtype = np.float32)
		self.audio = np.concatenate([borders, audio, fill, borders])

		self.length = int(len(self.audio) / self.framerate)

	def __del__(self):
		del self.audio

	# Browse functions
	def transform(self, TV):
		out = []
		while (self.iterator + 11) != self.length:
			out.append(self.update(TV))
			out.append(self.output(TV.file_id))

		return out

	def update(self, TV):
		self.iterator += 1

		# Mfcc
		if self.activMFCC:
			MFCC = librosa.feature.mfcc(y = self.audio[self.iterator * self.framerate:(self.iterator + 10) * self.framerate], sr = self.framerate, n_mfcc = 80)
			self.MFCC = np.round(np.mean(MFCC.T, axis = 0), 4)

		if self.activDB:
			DB = librosa.core.amplitude_to_db(self.audio[(self.iterator + 9) * self.framerate:(self.iterator + 10) * self.framerate])
			self.DB.pop(0)
			self.DB.append(np.round(np.mean(DB), 4))

		# pub
		for _, row in TV.iterrows():
			if row.timestamp <= self.iterator:
				self.pub = row.IsAPub

	def output(self, file_id):
		temp = [self.pub, file_id.iloc[0], self.iterator]
		if self.activMFCC:
			temp = np.concatenate([temp, self.MFCC])
		if self.activDB:
			temp = np.concatenate([temp, self.DB])

		return temp