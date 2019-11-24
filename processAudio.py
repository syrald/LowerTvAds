import librosa

import pandas as pd
import numpy as np

class Frames:
	def __init__(self, filePath, mfcc = True, db = True):
		# File variables
		audio, self.framerate = librosa.load(filePath, sr = 44100, res_type = "kaiser_fast")

		# To iterate the file
		self.iterator = 0
		self.padding = self.framerate * 10

		# Activate or not features
		self.activMFCC = mfcc
		self.activDB = db
		if self.activDB:
			self.db = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100]

		# Add zeros before and after the file
		# Also fill the last element to be the same length as the others
		borders = np.zeros(self.padding, dtype = np.float32)
		fill = np.zeros(self.framerate - (len(audio) % self.framerate), dtype = np.float32)
		self.audio = np.concatenate([borders, audio, fill, borders])

		self.length = int(len(self.audio) / self.framerate)

	def __del__(self):
		del self.audio

# Browse functionscs
	def browse(self, TV):
		out = []
		while self.hasNext():
			self.update(TV)
			out.append(self.output(TV.file_id))

		return out

	def hasNext(self):
		return (self.iterator + 11) != self.length

	def update(self, TV):
		self.iterator += 1

		# Mfcc
		if self.activMFCC:
			mfcc = librosa.feature.mfcc(y = self.audio[self.iterator * self.framerate:(self.iterator + 10) * self.framerate], sr = self.framerate, n_mfcc = 80)
			self.mfcc = np.round(np.mean(mfcc.T, axis = 0), 4)

		if self.activDB:
			db = librosa.core.amplitude_to_db(self.audio[(self.iterator + 9) * self.framerate:(self.iterator + 10) * self.framerate])
			self.db.pop(0)
			self.db.append(np.round(np.mean(db), 4))

		# pub
		for _, row in TV.iterrows():
			if row.timestamp <= self.iterator:
				self.pub = row.IsAPub

	def output(self, file_id):
		temp = [self.pub, file_id.iloc[0], self.iterator]
		if self.activMFCC:
			temp = np.concatenate([temp, self.mfcc])
		if self.activDB:
			temp = np.concatenate([temp, self.db])

		return temp

# CSV read/load part
def browseFile(fileName, i, activMFCC = True, activDB = True):
	global frames

	print("file: ", i)
	frames = Frames(fileName, activMFCC, activDB)
	ret = frames.browse(ads[ads.file_id == i])
	del frames
	return ret

def createCsv(filePath, activMFCC = True, activDB = True):
	global csv
	global ads

	ads_df = pd.read_csv("data/TV_ad_flag.csv")
	tv_df = pd.read_csv("data/TV_Files.csv")
	temp = []

	# Transform the variable pub into the variable IsAPub: Percentage of pub in the audio
	lastId = 0
	for _, row in ads_df.iterrows():
		if lastId != row.file_id:
			if lastId != 0 and temp[-1]["IsAPub"] == 1:
				lastFileLength = tv_df[tv_df.file_id == lastId].length.item()
				f = lambda i: round(1 - (0.1 * i), 1)
				for i in range(11):
					tempRow = {"file_id": lastId, "timestamp": lastFileLength + i, "IsAPub": f(i)}
					temp += [tempRow]

			lastId = row.file_id
		if row.timestamp == 0 and row.pub == 0:
			tempRow = {"file_id": row.file_id, "timestamp": row.timestamp, "IsAPub": 0}
			temp += [tempRow]
			continue
		elif row.pub == 0:
			f = lambda i: round(0.9 - (0.1 * i), 1)
		else:
			f = lambda i: round((0.1 + 0.1 * i), 1)

		for i in range(10):
			tempRow = {"file_id": row.file_id,"timestamp": row.timestamp + i, "IsAPub": f(i)}
			temp += [tempRow]

	lastFileLength = tv_df[tv_df.file_id == lastId].length.item()
	f = lambda i: round(1 - (0.1 * i), 1)
	for i in range(11):
		tempRow = {"file_id": lastId, "timestamp": lastFileLength + i, "IsAPub": f(i)}
		temp += [tempRow]

	ads = pd.DataFrame(temp, columns = ["file_id", "timestamp", "IsAPub"])
	csv = []

	# Read the files
	for _, row in tv_df.iterrows():
		if row.file_id > 8:
			csv = csv + browseFile(filePath + row.file_name, row.file_id, activMFCC, activDB)

	cols = ["pub", "file_id", "ts"]
	if activMFCC:
		cols = np.concatenate([cols, ["mfcc_" + str(i) for i in range(0, 80)]])
	if activDB:
		cols = np.concatenate([cols, ["db_" + str(i) for i in range(0, 10)]])

	csv = pd.DataFrame(csv, columns = cols)
	print("Done !")
