from .ProcessRaw import ProcessRaw

def processData(MFCC = True, DB = True):
	processRaw = ProcessRaw("data/raw/TV_ad_flag.csv", "data/raw/TV_Files.csv")
	csv = processRaw.transform(MFCC, DB)

	del processRaw
	return csv

print("""-------------------------------
processData(optional MFCC, optional DB):
	Given a list of audio file, generate a dataframe.
	Those audio file contains copyrighted data. Send an email to vianney.bacoup@gmail.com if you want them

	MFCC and DB are options you can activate or deactivate.
-------------------------------""")