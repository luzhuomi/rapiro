import subprocess
import os

DEVNULL = open(os.devnull, 'wb')

def speak(t):
	p = subprocess.Popen(["sudo","festival", "-b", "(SayText \"" + t + "\")"], stdin=subprocess.PIPE, stdout=DEVNULL, stderr=DEVNULL)
	return p.wait()

#speak("hi")
