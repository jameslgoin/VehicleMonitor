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

#turn the flask app into a socketio app, set client ping server every 1 sec
socketio = SocketIO(app, ping_interval=1, ping_timeout=10)

aggregator = None


def update(interval=0.01, sanity_interval=30):
    """
    emit new content every interval seconds.
    Per sanity_interval second will send out a full content packet
    Per interval second will send out a partial update packet if there is change in the content
    :param interval: must be between 0 and 1 (will be capped at both end)
    :param sanity_interval: should be between 10 to 60 seconds
    """
    interval = min(max(0.0, interval), 1.0)
    previous_content = {}
    sanity_check_counter = 0
    while True:
        sanity_check_counter += 1
        content = aggregator.get_content()
        reduced_content = {k: v for k, v in content.items() if v != previous_content.get(k, None)}
        previous_content = content
        content = reduced_content
        if sanity_check_counter == int(sanity_interval / interval):
            content = previous_content
            sanity_check_counter = 0
        if len(content) != 0:
            socketio.emit('newdata', content, namespace='/api')
        socketio.sleep(interval)


@app.route('/')
def hello_world():
    return render_template('index.html')


@socketio.on('slider', namespace='/api')
def slider(data):
    print('slider value updated: %s' % data.get('value'))


@socketio.on('connect', namespace='/api')
def connect():
    socketio.emit('newdata', aggregator.get_content(), namespace='/api')


if __name__ == '__main__':
    aggregator = Aggregator.Aggregator()
    command = sys.argv[1] if len(sys.argv) > 1 else "python3 ./test.py"
    aggregator.register_component(command)
    aggregator.start_gathering()
    socketio.start_background_task(target=update)
    socketio.run(app, host='0.0.0.0', port=8080)
