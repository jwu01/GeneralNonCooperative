from flask import Flask, render_template, session, request, flash, url_for, redirect#imports class Flask
from util import db_build as build
from util import db_update as update
from util import db_retrieve as search
import os

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')



@app.route('/')#Defines index
def home():
    build.main()
    return render_template("login.html")
@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form["username"]
    password = search.password(username)
    if password == request.form['password']:
        session['username'] = Username
        return redirect(url_for(home))
    else:
        flash('Wrong Username or Password!')
        return render_template('login.html')

@app.route("/reg",methods=['GET','POST'])
def reg():
        newUser = request.form['user']
        newPass = request.form['pass']
        update.addUser(newUser, newPass)
        session['username'] = newUser
        return render_template('login.html')
if __name__ == '__main__':
    app.debug = True
    app.run()
