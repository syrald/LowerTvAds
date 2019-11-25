from processAudio import *
from processFiles import *
from buildModel import *
from models import *

def menu():
	global model
	loop = True
	while (loop):
		print("Menu")
		print("1 - Import the model")
		print("2 - Quit")
		choice = input(" >> ")
		if choice == "1":
			model = readModel()
		elif choice == "2":
			loop = False
		else:
			print("Wrong command")

if __name__ == "__main__":
	print("The purpose of this program is to automatically lower the TV when an ad is played.")
	print("https://github.com/syrald/LowerTvAds")

	print("Done:")
	print("- A model is built from more than 10h of french TV")
	print("")
	print("Todo:")
	print(" - Get the audio in real time")
	print(" - Predict the result from the model without any time issues")
	print(" - Learning how to lower the sound from a computer like a remote")
	print("")
	menu()
