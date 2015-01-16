from bottle import route, run, template
import threading
import rapiro
import wolframapi
import urllib 

r = rapiro.Rapiro()
counter = 0
rlock = threading.Lock()


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/reset/')
def reset():
    global rlock
    global r
    with rlock:
        r.reset()
    return template('{{counter}}', counter=counter)

@route('/cmd/<command>')
def cmd(command):
	global rlock
	global r
	with rlock:
		query = urllib.unquote(command).decode('utf8').replace('+', ' ')
		print "query=%s" % (query)
		if query=="hello":
			r.look_for_face()
		elif query=="stop":
			r.reset()
		elif query=="dance":
			r.action(10)
		else:
			answer = wolframapi.process(query)
			answer = answer.replace('Stephen Wolfram', 'Kenny Lu').replace('Wolfram Alpha','Rapiro Lu')
			print answer
			r.speak(answer)
	return template('{ "command" : {{command}},  "status": "ok" }', command=command)

run(host='0.0.0.0', port=8080)
