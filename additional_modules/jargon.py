import os

def process(string):
	return '"' + string + '"'

def speak(string):
	os.system("bash /home/mason/ComputerVision/additional_modules/speech.sh " + process(string))

