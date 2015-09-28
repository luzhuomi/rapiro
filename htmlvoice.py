
# requires cherrypy3
# installing directly via apt-get install python-cherrypy3 should be easiest
# installing via easy_install
# which requires apt-get install python-dev ffi-dev
#

import threading
import urllib 
from bottle import ServerAdapter, route, run, server_names, template # easy_install bottle cherrypy pyopenssl # which requires apt-get install python-dev ffi-dev
from socket import gethostname
import wolframapi


counter = 0
rlock = threading.Lock()


@route('/voice')
def index():
	return template('voice.tpl') 


@route('/voice/<q>')
def index(q):
	print "query=%s" % (q)
	answer = wolframapi.process(q)
	answer = answer.replace('Stephen Wolfram', 'Kenny Lu').replace('Wolfram Alpha','Rapiro Lu')
	print answer
	return answer # template('voice.tpl')


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
