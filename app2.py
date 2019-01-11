from flask import Flask, render_template, session, request, flash, url_for#imports class Flask
from util import db_build as build
app = Flask(__name__)#Creates an instance of Flask

@app.route('/')#Defines index
def home():
    build.main()
    if 'username' in session:
        return render_template("home.html")
    else:
        return render_template("login.html")
@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    if 'username' in session:
        username = session['username']
        return render_template("home.html", Name = username)
    else:
        username = request.form.get["username"]
        password = search.password(username)
        if password == request.form.get['password']:
            session['username'] = Username
            redirect(url_for(authenticate))
        else:
            flash('Wrong Username or Password!')
            return redirect(url_for('home'))

@app.route("/reg",methods=['GET','POST'])
def reg():
        newUser = request.form.get['user']
        newPass = request.form.get['pass']
        update.adduser(newUser, newPass)
        return redirect(url_for('home'))
if __name__ == '__main__':
    app.debug = True
    app.run()
