
# requires cherrypy3
# installing directly via apt-get install python-cherrypy3 should be easiest, note the apt-get way of getting cherrypy3 will yield a ssl problem
# installing via easy_install
# which requires apt-get install python-dev libffi-dev
# easy_install pyOpenSSL

import threading
import urllib 
from bottle import ServerAdapter, route, run, server_names, template, static_file # easy_install bottle cherrypy pyopenssl 
# which requires apt-get install python-dev ffi-dev

from socket import gethostname
import wolframapi

from text2speech import speak
import rapiro

r = rapiro.Rapiro()


counter = 0
rlock = threading.Lock()


@route('/prompt')
def prompt():
	return template('template/prompt.tpl')

@route('/voice')
def index():
	r.speak("Yes")
	return template('template/voice.tpl') 


@route('/voice/<q>')
def index(q):
	answer = "Ok"
	words = q.split()
	if (len(words) >0) and ('' == words[0]): 
		words = words[1:]
	if (len(words) >0): # and ('ryan' == words[0].lower()):
		q2 = q #' '.join(words[1:])
		query = urllib.unquote(q2).decode('utf8').replace('+', ' ')
		print "query=%s" % (query)
		if query.lower()=="look at me":
			r.speak(answer)
			r.look_for_face()
		if query.lower()=="take a picture":
			r.speak(answer)
			r.picture()			
		elif query=="move forward":
			r.speak(answer)
			r.forward()
		elif query=="move backword":
			r.speak(answer)
			r.backward()
		elif query=="turn to your left":
			r.speak(answer)
			r.turn_left()
		elif query=="turn to your right":
			r.speak(answer)
			r.turn_right()
		elif query=="stop" or query=="reset":
			r.speak(answer)
			r.reset()
		elif query=="hello" or query=="hi":
			r.speak(answer)
			r.action(6)
		elif query=="hug":
			r.speak(answer)
			r.action(7)
		elif query=="bye" or query=="bye bye" or query=="byebye":
			r.speak(answer)
			r.action(8)
		elif query=="hold this for me":
			r.speak(answer)
			r.action(9)
		elif query=="shutdown":
			r.shutdown()
		elif query=="turn off the light":
			import smarthome
			smarthome.turn_off()
		elif query=="turn on the light":
			import smarthome
			smarthome.turn_on()
		#elif query=="dance": # too dangerous
		#	r.action(10)
		else:
			answer = wolframapi.process(query)
			answer = answer.replace('Stephen Wolfram', 'Kenny Lu').replace('Wolfram Alpha','Rapiro Ryan')
			# print answer
			r.speak(answer)
	return answer

@route('/static/<path:path>')
def callback(path):
    return static_file(path, root='/home/pi/git/rapiro/static/')



class SSLWebServer(ServerAdapter):
    """
    CherryPy web server with SSL support.
    """

    def run(self, handler):
        """
        Runs a CherryPy Server using the SSL certificate.
        """
        from cherrypy import wsgiserver
        from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter

        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)

        server.ssl_adapter = pyOpenSSLAdapter(
            certificate="openssl/certificate.crt",
            private_key="openssl/privateKey.key"#,
            #certificate_chain="intermediate_cert.crt"
        )

        try:
            server.start()
        except Exception,e:
	    print "failed to start %s" % (str(e))
            server.stop()

server_names['sslwebserver'] = SSLWebServer

run(host='0.0.0.0', port=8080, server='sslwebserver')
