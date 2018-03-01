from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
from flask_socketio import send, emit
from threading import Thread, Event, Lock
from time import sleep
import random
import Aggregator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is supposed to be a secret!'
socketio = SocketIO(app)
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)


thread = None
thread_lock = Lock()
content = {}
aggregator = None


def background_thread():
    while True:
        socketio.emit('newdata', aggregator.get_content(), namespace='/api')
        socketio.sleep(1)


@app.route('/')
def hello_world():
    return render_template('index.html')


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
    global aggregator
    with thread_lock:
        if thread is None:
            aggregator = Aggregator.Aggregator()
            aggregator.register_component("python /Users/hht/Documents/VehicleMonitor/test.py")
            aggregator.start_gathering()
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
