from werkzeug import secure_filename
from flask import Flask, render_template, jsonify, make_response, request
import json
import string
import sys
from io import StringIO  # Python3sdf
import OSC
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable

import os
from flask_socketio import SocketIO, emit


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "music.db"))

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class SongClass(db.Model):
    key = db.Column(db.Integer, autoincrement=True, primary_key=True)

    song = db.Column(db.String(200))

    def __repr__(self):
        return self.song



def sendCmd(cmd,par = None):
    oscmsg = OSC.OSCMessage()
    oscmsg.append('MY_PYTHON_GUI')
    oscmsg.setAddress(cmd)
    if par:
        oscmsg.append(par)
    c.send(oscmsg)
c = OSC.OSCClient()
c.connect(('127.0.0.1', 4557))   # connect to SuperCollider
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully to /home/pi/test/ folder'

	  


@app.route('/')


def my_form():
    song_query = SongClass.query.all()
    if song_query[-1]:
        song = str(song_query[-1])
    else:
	song = " "
    if song_query[-2]:
        song2 = str(song_query[-2])
    else:
	song2 = " "
    return render_template('index.html', song=song, song2=song2)
 #   return render_template('index.html')
 

@socketio.on('value_changed', namespace='/test')
def value_changed(message):
    print(message)
 

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
 
 
@app.route('/parse_data', methods=['POST'])
def my_form_post():
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 4557))   # connect to SuperCollider
    sendCmd("/stop-all-jobs")
    song = request.get_json()
    song = song["value"]
    song = SongClass(song=song)
    db.session.add(song)
    db.session.commit()
#    my_obj = MyObject(song)
#	another_obj = MyObject.query.first()
#	print another_obj
#    song = another_obj["value"]
	#song = song.replace("\n","")
    #song = json.dumps(song)
    song_query = SongClass.query.all()
    if song_query:
        song = str(song_query[-1])
    else:
        song=" "
    if song_query[-2]:
        song2 = str(song_query[-2])
    else:
        song2 = " "
    print song
    sendCmd("/run-code", song)
 #   if state == "off":
	#    sendCmd("/stop-all-jobs")
    return render_template('index.html', song=song, song2=song2)
	
	

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0',debug=True, port = 8001)
