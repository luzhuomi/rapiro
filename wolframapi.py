import wolframalpha
import sys
import ConfigParser # easy_install configparser

# Get a free API key here http://products.wolframalpha.com/api/
# This is a fake ID, go and get your own, instructions on my blog.

config = ConfigParser.ConfigParser()
config.read('/boot/rapiro.conf')
app_id = config.get('WOLFRAMALPHA','app_id')

client = wolframalpha.Client(app_id)

def process(query):
	res = client.query(query)

	if len(res.pods) > 0:
    		texts = ""
    		pod = res.pods[1]
    		if pod.text:
        		texts = pod.text
    		else:
        		texts = "I have no answer for that"
    		# to skip ascii character in case of error
    		texts = texts.encode('ascii', 'ignore').replace('|', ' ')
    		return texts
	else:
    		return "Sorry, I am not sure."

