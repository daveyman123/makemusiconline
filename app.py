from werkzeug import secure_filename
from flask import Flask, url_for, redirect, render_template, jsonify, make_response, request, session
import json
import string
import sys
from io import StringIO  # Python3sdf
import OSC
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable
import cgi

import re

import os
import os
# from flask_socketio import SocketIO, emit


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "music.db"))

app = Flask(__name__)
#socketio = SocketIO(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
app.secret_key='y337kGcy&zP3B'

def is_blank(stringinput):

    if stringinput == "" or " " in stringinput:

        return True

    else:

        return False



def valid_legnth(stringinput):

    if len(stringinput) > 2 and len(stringinput) < 20:

        return True

    else:

        return False 



def valid_characters(stringinput):

    lan = r"[^A-Za-z0-9]"

    if re.search(lan,stringinput):

        return False

    else:

        return True



def valid_email(stringinput):

    if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", stringinput) != None:

        return True

    else:

        return False 

class SongClass(db.Model):
    key = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(120))
    song = db.Column(db.String(200))

    def __repr__(self):
        return self.song

class User(db.Model):
	key = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(120), nullable=True)
	password = db.Column(db.String(120))
	username = db.Column(db.String(120))
	
	def __init__(self, email, password, username):
		self.email=email
		self.password=password
		self.username=username
	



def sendCmd(cmd,par = None):
    oscmsg = OSC.OSCMessage()
    oscmsg.append('MY_PYTHON_GUI')
    oscmsg.setAddress(cmd)
    if par:
        oscmsg.append(par)
    c.send(oscmsg)
c = OSC.OSCClient()
c.connect(('127.0.0.1', 4557))   # connect to SuperCollider
@app.before_request
def require_login():
    allowed_routes = ['login', 'register1', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully to /home/pi/test/ folder'


	  
@app.route('/login', methods=['POST', 'GET'])

def login():
	if request.method == 'POST':
		
	    password = request.form['password']
            username = request.form['username']
            user = User.query.filter_by(username=username).first()
	    if user and user.password == password:
                session['username'] = username
                return redirect(url_for('my_form'))
	    else:
			# TODO - explain why login failed
		return '<h1>Error</h1>'
	
	
		
	return render_template('login.html')		
@app.route('/register')
def register1():
    username_error =""

    password_error =""

    verify_error =""

    email_error =""

    username =""

    email=""			
    return render_template('register.html', username = username,email = email,

 username_error=username_error, password_error = password_error,

  verify_error = verify_error, email_error = email_error)			
	
@app.route('/register', methods=['POST', 'GET'])
def register():
	
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    verify = cgi.escape(request.form['verify'])
    email = cgi.escape(request.form['email'])

    username_error = ""
    password_error = ""
    verify_error = ""
    email_error = ""





    if (is_blank(username)) == True:

        username_error = "That's not a valid username"



    if (is_blank(password)) == True:

        password_error = "That's not a valid password"



    if (valid_legnth(username)) == False:

        username_error = "That's not a valid username"



    if (valid_legnth(password)) == False:

        password_error = "That's not a valid password"



    if (valid_characters(username)) == False:

        username_error = "That's not a valid username"



    if (valid_characters(password)) == False:

        password_error = "That's not a valid password"



    if password != verify:

        verify_error = "Passwords don't match"





    if email != "":

        if (valid_legnth(email)) == False:

            email_error = "That's not a valid Email"



        if " " in email:

            email_error = "That's not a valid Email"



        if (valid_email(email)) == False:

            email_error = "That's not a valid Email"



    if not username_error and not password_error and not verify_error and not email_error:
            existing_user = User.query.filter_by(username=username).first()
	    if not existing_user:
			new_user = User(email, password, username)
			db.session.add(new_user)
			db.session.commit()
                        session['username'] = username
                        return redirect(url_for('my_form',username=username))
	    else:
			# TODO - user better response messaging
			return "<h1>duplicate user</h1>"
        

		


    return render_template('register.html', username = username, password = "",

 verify ="", email = email, username_error=username_error,

 password_error = password_error, verify_error = verify_error,

email_error = email_error)




@app.route('/')


def my_form():
    song_query = SongClass.query.all()
    if song_query:
        song = str(song_query[-2])
        username1 = song_query[-1].username
        username2 = song_query[-2].username
    else:
	song = " "
    
    username = session['username']
  
    #username2={'username': username2, "song": song}
    return render_template('index.html', username = username, song=song, user=username1, user2 = username2)
 

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
# @socketio.on('value_changed', namespace='/test')
# def value_changed(message):
    # print(message)
 

# @socketio.on('my event', namespace='/test')
# def test_message(message):
    # emit('my response', {'data': message['data']})

# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
    # emit('my response', {'data': message['data']}, broadcast=True)

# @socketio.on('connect', namespace='/test')
# def test_connect():
    # emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
    # print('Client disconnected')
@app.route('/stop', methods=['POST'])
def stop(): 
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 4557))   # connect to SuperCollider
    sendCmd("/stop-all-jobs")
    return redirect(url_for('my_form'))
@app.route('/parse_data', methods=['POST'])
def my_form_post():
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 4557))   # connect to SuperCollider
    sendCmd("/stop-all-jobs")
    song = request.get_json()
    song = song["value"]
    song = SongClass(song=song, username=session['username'])
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
        username = str(song_query[-1].username)
        print username
    else:
        song=" "
        username= "nobody i guess"
    
    print song
    username2={'username': username, "song": song}
    sendCmd("/run-code", song)
 #   if state == "off":
	#    sendCmd("/stop-all-jobs")
    
    return jsonify({ 'var1': username, 'var2': song })
	
	

if __name__ == "__main__":
   # socketio.run(app, host='0.0.0.0',debug=True, port = 8080)
      app.run(host='0.0.0.0',debug=True, port = 8080)
