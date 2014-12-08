import urllib2
import sys


api_key ="AIzaSyDuQQ2qw13-ZBc5cReLhskZz73bZc0hps4"
url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=" + api_key
audio = open(sys.argv[1],'rb').read()
headers={'Content-Type': 'audio/x-flac; rate=44100', 'User-Agent':'Mozilla/5.0'}

request = urllib2.Request(url, data=audio, headers=headers)
response = urllib2.urlopen(request)
print response.read()
