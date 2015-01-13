from bottle import route, run, template
import threading
import rapiro

r = rapiro.Rapiro()
counter = 0
rlock = threading.Lock()


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/reset/')
def reset():
    global rlock
    global counter
    global r
    with rlock:
        counter = counter + 1
        r.look_for_face()
    return template('{{counter}}', counter=counter)


run(host='0.0.0.0', port=8080)
