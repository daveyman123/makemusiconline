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



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "music.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class SongClass(db.Model):
    key = db.Column(db.Integer, autoincrement=True, primary_key=True)

    song = db.Column(db.String(80))

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

@app.route('/')
def my_form():
    song = SongClass.query.all()
    song = song[-1]
    #print song

    return render_template('index.html', song=song)

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
    song = SongClass.query.all()
    
    song = str(song[-1])
    print song
    sendCmd("/run-code", song)
 #   if state == "off":
	#    sendCmd("/stop-all-jobs")
    return render_template('index.html', song=song)
	
	

if __name__ == "__main__":
   app.run(host='0.0.0.0', threaded=True, port=8080, debug=True)