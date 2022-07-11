import socketio
from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread
import subprocess
from flask import Flask, Response
import json 

listener = TuioListener()
setattr(listener, "sio", socketio.Server(async_mode='threading'))
app = Flask(__name__,
            static_url_path='/', 
            static_folder='./')
app.wsgi_app=socketio.WSGIApp(listener.sio, app.wsgi_app)

sid_ = 0;
@listener.sio.event
def connect(sid, environ):
	print('connect ', sid)
	sid_ = sid;
	listener.sio.emit('my_message','connected')

@listener.sio.event
def my_message(sid, data):
    print('message ', data)

@listener.sio.event
def disconnect(sid):
    print('disconnect ', sid)

@listener.sio.event
def _add_tuio_cursor(cursor):
    listener.sio.emit('my_message','added')
    listener.sio.emit('add_cursor',json.dumps({'id':cursor.session_id,'position':{'x':cursor.position[0],'y':cursor.position[1]}}))
    #print("Add : "+str(cursor.position))

@listener.sio.event
def _remove_tuio_cursor(cursor):
    listener.sio.emit('remove_cursor',json.dumps({'id':cursor.session_id,'position':{'x':cursor.position[0],'y':cursor.position[1]}}))
    #print("Remove : "+str(cursor.position))

@listener.sio.event
def _update_tuio_cursor(cursor):
    listener.sio.emit('update_cursor',json.dumps({'id':cursor.session_id,'position':{'x':cursor.position[0],'y':cursor.position[1]}}))
    #print("Update : "+str(cursor.position))

    
if __name__ == '__main__':
    client = TuioClient(("localhost",3333))
    t = Thread(target=client.start)
    listener.add_tuio_cursor = _add_tuio_cursor
    listener.update_tuio_cursor = _update_tuio_cursor
    listener.remove_tuio_cursor = _remove_tuio_cursor
    client.add_listener(listener)
    t.start()
    chrom = subprocess.Popen(['chromium', '--start-fullscreen', 'http://127.0.0.1:5000/index.html'])
    app.run(port=5000)
    chrom.terminate()
    print("Program Terminated")


