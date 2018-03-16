#!/usr/bin/python3

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, send, emit
import Aggregator
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is supposed to be a secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

aggregator = None


def background_thread():
    while True:
        content = aggregator.get_content()
        socketio.emit('newdata', content, namespace='/api')
        socketio.sleep(1)


@app.route('/')
def hello_world():
    return render_template('index.html')


@socketio.on('slider', namespace='/api')
def slider(data):
    print('slider value updated: %s' % data.get('value'))


# @socketio.on('connect', namespace='/api')
# def connect(namespace=None, query_string=None, headers=None):
#     print('client connect', query_string)


@socketio.on('pping', namespace='/api')
def pping(_):
    socketio.emit('ppong', namespace='/api')


if __name__ == '__main__':
    aggregator = Aggregator.Aggregator()
    command = sys.argv[1] if len(sys.argv) > 1 else "python3 ./test.py"
    aggregator.register_component(command)
    aggregator.start_gathering()
    socketio.start_background_task(target=background_thread)
    socketio.run(app, host='0.0.0.0', port=8080)
