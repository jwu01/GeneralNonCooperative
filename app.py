from flask import Flask, render_template, session, request, flash, url_for, redirect#imports class Flask
import urllib
import json
from util import db_functions as func
import os
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')

@app.route('/')
def home():
    if "username" in session:
        return render_template("homePage.html")
    return render_template("loginPage.html")

@app.route('/auth', methods = ['POST', 'GET'])
def authorize():
    username = request.form['username']
    if (checkLogin(username, request.form['password'])):
        print('Successful Login')
        session["username"] = username
        return render_template("homePage.html")
    print('Failed login')
    flash('Invalid Username/Password Combo!')
    return redirect(url_for("home"))

@app.route('/problems', methods= ['POST', 'GET'])
def problemsPage():
    if "username" in session:
        return render_template("problemsPage.html", easyProblems = getEasyProblems(session["username"]), mediumProblems = getMediumProblems(session["username"]), hardProblems = getHardProblems(session["username"]))
    return redirect(url_for("home"))

@app.route('/problem', methods=['POST', 'GET'])
def problemPage():
    if "username" in session:
        return render_template('problemPage.html', data = getProblemJSON(request.args.get('title')))
    return redirect(url_for("home"))

@app.route('/success', methods=['POST', 'GET'])
def successRouter():
    if "username" in session:
        problemDone(session["username"], request.args.get('title'))
    return redirect(url_for("home"))

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    passwordConfirm = request.form['passwordConfirm']
    print('User is trying to register: (' + username + ", " + password + ")")
    if (checkIfUserInDB(username)):
        print('Username already taken!')
        flash('Username already taken!')
    elif (password != passwordConfirm):
        print('Passwords do not match!')
        flash('Passwords do not match!')
    else:
        print('Successfully registered user!')
        flash('Successfully registered user!')
        url = 'https://ipapi.co/json/'
        req = urllib.request.urlopen(url)
        data = json.loads(req.read())
        country = data["country"]
        registerUser(username, password, country)
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    if "username" in session:
        print("sucessful logout")
        session.pop("username")
    return redirect(url_for("home"))

@app.route("/register", methods=['GET'])
def registerGET():
    return redirect(url_for("home"))

@app.route("/leaderboard", methods=['POST', 'GET'])
def leaderboard ():
    if "username" in session:
        leaderboard = getLeaderboard()
        return render_template('leaderboardPage.html', users=leaderboard, length=len(leaderboard), username=session["username"])
    return redirect(url_for("home"))


# FAKE METHODS
def checkIfUserInDB (username):
    return func.findInfo('users',  username,'username', fetchOne = True)

def registerUser (username, password, country):
    func.insert('users', [username,  sha256_crypt.encrypt(password), 0, '', country, 0])

def checkLogin (username, password):
    user = checkIfUserInDB(username)
    if user:
        return sha256_crypt.verify(password, user[2])
    return False

def problemDone (username, problemTitle):
    # Check if user has done problem before and if not, give them points and mark the item as done
    userSolvesQuestion(username, problemTitle)

def getEasyProblems(username):
    # True / False shows if the user did the problem or not
    return [
        ["Fibonacci", func.hasSolved(username, "Fibonacci")],
        ["Longest Word", True],
        ["easyFunction2", True],
        ["easyFunction3", False]
    ]

def getMediumProblems(username):
    # True / False shows if the user did the problem or not
    return [
        ["mediumFunction0", True],
        ["mediumFunction1", True],
        ["mediumFunction2", True],
        ["mediumFunction3", False]
    ]

def getHardProblems(username):
    # True / False shows if the user did the problem or not
    return [
        ["hardFunction0", False],
        ["hardFunction1", False],
        ["hardFunction2", False],
        ["hardFunction3", False]
    ]

def getLeaderboard ():
    return func.getAllUsers()

def getProblemJSON(problemTitle):
    return '{"name": "' + problemTitle + '", "description":"Write a function to return the n-th element in the Fibonacci sequence","testCases":{"0":"0","1":"1","2": "1", "3": "2", "4": "3", "6": "8", "7":"13"}, "hiddenTestCases":{"8":"21", "9":"34", "10":"55", "11":"89"}}'

if __name__ == '__main__':
    app.debug = True
    app.run()
