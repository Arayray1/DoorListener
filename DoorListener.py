from flask import Flask, request, render_template, Response, json
app = Flask(__name__)
import  gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
from werkzeug.serving import run_with_reloader
monkey.patch_all
#Before any data is received it reports that it is uninitialized
current_status = "uninitialized"

#The template for the website
@app.route('/')
def index():
    return render_template('index.html')

#Repeat this over and over
def event():
    local_status = "not here"
    global current_status
    while True:
        if local_status != current_status:
            # yield 'data: ' + json.dumps(current_status) + '\n\n'
            yield 'data: ' + current_status + '\n\n'
            local_status = current_status
        gevent.sleep(0.2)

#Recieves data from BBB and if no data, returns error 400
#If it recieves data, returns "got some status" and tells what it is
@app.route('/status',methods=['POST'])
def handlestatus():
    status = request.form.get('status', None)
    if not status:
        return ('Missing status value', 400)
    print "Got some status: " + status
    global current_status
    current_status = status
    return ('',200)

# Sends data to browser and if it connects prints "A browser is connected"
#Runs the event code, so sends data to website
@app.route('/stream/',methods=['GET','POST'])
def stream():
    print 'A browser is conncected!'
    return Response(event(), mimetype="text/event-stream")

#The WSGIServer is a slave to the system, as it must "serve forever"
@run_with_reloader
def run_server():
     WSGIServer(('',80), app).serve_forever()
#If it is the main application then it runs the code
if __name__ == "__main__":
    run_server()
