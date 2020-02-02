from .Frames import Frames

import numpy as np
import pandas as pd

class ProcessRaw:
	def __init__(self, TV_ad_flag, TV_files):
		self.ads_df = pd.read_csv(TV_ad_flag)
		self.tv_df = pd.read_csv(TV_files)

	def transform(self, activMFCC = True, activDB = True):
		# Transform the variable pub into the variable IsAPub: Percentage of pub in the audio
		temp = []
		lastId = 0
		for _, row in self.ads_df.iterrows():
			if lastId != row.file_id:
				if lastId != 0 and temp[-1]["IsAPub"] == 1:
					lastFileLength = self.tv_df[self.tv_df.file_id == lastId].length.item()
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

		lastFileLength = self.tv_df[self.tv_df.file_id == lastId].length.item()
		f = lambda i: round(1 - (0.1 * i), 1)
		for i in range(11):
			tempRow = {"file_id": lastId, "timestamp": lastFileLength + i, "IsAPub": f(i)}
			temp += [tempRow]

		ads = pd.DataFrame(temp, columns = ["file_id", "timestamp", "IsAPub"])
		csv = []

		# Read the files
		for _, row in self.tv_df.iterrows():
			if row.file_id > 8:
				print("file: ", i)
				frames = Frames("data/raw/" + row.file_name, activMFCC, activDB)
				csv = csv + frames.transform(ads[ads.file_id == i])
				del frames

		cols = ["pub", "file_id", "ts"]
		if activMFCC:
			cols = np.concatenate([cols, ["mfcc_" + str(i) for i in range(0, 80)]])
		if activDB:
			cols = np.concatenate([cols, ["db_" + str(i) for i in range(0, 10)]])

		self.csv = pd.DataFrame(csv, columns = cols)

		return self.csv