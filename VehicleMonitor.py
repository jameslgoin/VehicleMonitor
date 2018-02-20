from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
from flask_socketio import send, emit
from threading import Thread, Event, Lock
from time import sleep
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)


thread = None
thread_lock = Lock()

def background_thread():
    while True:
        socketio.emit('newdata', {'speed': random.randint(0,300)}, namespace='/api')
        socketio.sleep(0.2)


@app.route('/')
def hello_world():
    return send_file('static/index.html')

@socketio.on('slider', namespace='/api')
def text(data):
    print('slider value updated: %s' % data.get('value'))

@socketio.on('break', namespace='/api')
def text(data):
    print('break value updated: %s' % data.get('value'))

@socketio.on('connect', namespace='/api')
def connect():
    print('client connect')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
