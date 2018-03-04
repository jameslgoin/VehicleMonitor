from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, send, emit
import Aggregator
import eventlet
import signal

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is supposed to be a secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)


thread = None
content = {}
aggregator = None


def background_thread():
    while True:
        content = aggregator.get_content()
        print(content)
        socketio.emit('newdata', content, namespace='/api')
        socketio.sleep(0.5)


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
    if thread is None:
        aggregator = Aggregator.Aggregator()
        aggregator.register_component("python3 /Users/hht/Documents/VehicleMonitor/test.py")
        aggregator.start_gathering()
        print('thread init')
        thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    socketio.run(app, host='0.0.0.0', port=8080)
