
# requires cherrypy3
# installing directly via apt-get install python-cherrypy3 should be easiest
# installing via easy_install
# which requires apt-get install python-dev ffi-dev
#

import threading
import urllib 
from bottle import ServerAdapter, route, run, server_names, template, static_file # easy_install bottle cherrypy pyopenssl 
# which requires apt-get install python-dev ffi-dev

from socket import gethostname
import wolframapi

from text2speech import speak

counter = 0
rlock = threading.Lock()


@route('/voice')
def index():
	return template('voice.tpl') 


@route('/voice/<q>')
def index(q):
	print "query=%s" % (q)
	answer = ''
	words = q.split()
	if 'Jarvis' in words:
		q2 = ' '.join(filter(lambda x:x!='Jarvis', words))
		answer = wolframapi.process(q2)
		answer = answer.replace('Stephen Wolfram', 'Kenny Lu').replace('Wolfram Alpha','Jarvis')
		print answer
		speak(answer)
	return answer # template('voice.tpl')


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
