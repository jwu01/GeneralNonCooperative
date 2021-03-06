from flask import Flask, render_template, session, request, flash, url_for, redirect#imports class Flask
import urllib
import json
from util import db_functions as func
import os
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')

#--------------------------------Home Page-------------------------------------------
@app.route('/')
def home():
    '''
    If user is in session, return home page and allow user to start coding.
    If user not in session, redirect to login/register Page
    '''
    if "username" in session:
        return render_template("homePage.html")
    return render_template("loginPage.html")

#----------------------------------Login/logout/register--------------------------------------
@app.route('/auth', methods = ['POST', 'GET'])
def authorize():
    '''
    Authenticate username/password combination
    '''
    username = request.form['username']
    if (checkLogin(username, request.form['password'])):
        print('Successful Login')
        session["username"] = username
        if (username == "admin"):
            return redirect(url_for("adminPage"))
        return render_template("homePage.html")
    print('Failed login')
    flash('Invalid Username/Password Combo!')
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    '''
    Logs user out by popping their name from session
    '''
    if "username" in session:
        print("sucessful logout")
        session.pop("username")
    return redirect(url_for("home"))

# @app.route("/register", methods=['GET'])
# def registerGET():
#     return redirect(url_for("home"))

@app.route("/register", methods=['POST'])
def register():
    '''
    Registers new username/password combination and checks to see if Username
    is unique
    '''
    
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

#-------------------------------Admin Page--------------------------------------

@app.route('/admin', methods=['POST', 'GET'])
def adminPage():
    '''
    Admins have access to creating their own problems
    '''
    if "username" in session:
        if (session['username'] == 'admin'):
            return render_template("adminPage.html")
    return redirect(url_for("home"))

@app.route('/postProblem', methods = ['POST', 'GET'])
def post():
    if "username" in session and session["username"] == "admin":
        title = request.form["title"].strip()
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        visibleTestCases = "{"
        hiddenTestCases = "{"
        for i in range(0,3):
            vin = request.form["visibleInput"+ str(i)]
            vout = request.form["visibleOutput"+ str(i)]
            hin = request.form["hiddenInput"+ str(i)]
            hout = request.form["hiddenOutput"+ str(i)]
            visibleTestCases += '"{}":"{}",'.format(vin,vout)
            hiddenTestCases += '"{}":"{}",'.format(hin,hout)
        visibleTestCases = visibleTestCases[:-1] + "}"
        hiddenTestCases = hiddenTestCases[:-1] + "}"
        func.storeProblem(title,difficulty,description,visibleTestCases,hiddenTestCases)
        return redirect(url_for("adminPage"))
    return redirect(url_for("home"))


#-------------------------------View and Solve Problems----------------------------------------------

@app.route('/problems', methods= ['POST', 'GET'])
def problemsPage():
    '''
    Display available functions and whether or not they have been solve
    '''
    if "username" in session:
        return render_template("problemsPage.html", easyProblems = getEasyProblems(session["username"]), mediumProblems = getMediumProblems(session["username"]), hardProblems = getHardProblems(session["username"]))
    return redirect(url_for("home"))


@app.route('/problem', methods=['POST', 'GET'])
def problemPage():
    '''
    Allows user to code their solution to a problem and run it by several test test cases
    '''
    if "username" in session:
        print(getProblemJSON(request.args.get('title')))
        return render_template('problemPage.html', data = getProblemJSON(request.args.get('title')))
    return redirect(url_for("home"))

#-------------------------------Celebration--------------------------

@app.route('/success', methods=['POST', 'GET'])
def successRouter():
    '''
    If problem passes all visible and hidden test cases,
    confetti drops
    '''
    if "username" in session:
        problemDone(session["username"], request.args.get('title'))
        redirect(url_for("problemPage"))
    return redirect(url_for("home"))


#---------------------------View Leaderboard-----------------------------------------

@app.route("/leaderboard", methods=['POST', 'GET'])
def leaderboard ():
    '''
    Display users with their respective point values and countries
    '''
    if "username" in session:
        leaderboard = getLeaderboard()
        return render_template('leaderboardPage.html', users=leaderboard, length=len(leaderboard), username=session["username"])
    return redirect(url_for("home"))


#----------------------------Database Functions-------------------------------------
def postProblemDB(title, difficulty, description, visibleTestCases, hiddenTestCases):
    # difficulty is a string of'easy', 'medium' or 'hard'
    # visibleTestCases and hiddenTestCases are both dictionaries where key is input and value is output
    print('problem posted')
def getLeaderboard ():
    '''
    Retrieves users for leaderboard
    '''
    return func.getAllUsers()

def checkIfUserInDB (username):
    '''
    Check if username is unique
    '''
    return func.findInfo('users',  username,'username', fetchOne = True)

def registerUser (username, password, country):
    '''
    Register username/password combo, encrypt password, check country
    '''
    func.insert('users', [username,  sha256_crypt.encrypt(password), 0, '', country, 0])

def checkLogin (username, password):
    '''
    Authenticate
    '''
    user = checkIfUserInDB(username)
    if user:
        return sha256_crypt.verify(password, user[2])
    return False

def problemDone (username, problemTitle):
    '''
    Check if user has done problem before and if not, give them points and mark the item as done
    '''
    func.userSolvesQuestion(username, problemTitle)

def getEasyProblems(username):
    '''
    Retrieve problems with easy difficulty
    '''
    problems = []
    for problem in func.getAllProblems('easy'):
        problems.append([problem[1], func.hasSolved(username, problem[1])])
    return problems

def getMediumProblems(username):
    '''
    Retrieve problems with medium difficulty
    '''
    problems = []
    for problem in func.getAllProblems('medium'):
        problems.append([problem[1], func.hasSolved(username, problem[1])])
    return problems

def getHardProblems(username):
    '''
    Retrieve problems with hard difficulty
    '''
    problems = []
    for problem in func.getAllProblems('hard'):
        problems.append([problem[1], func.hasSolved(username, problem[1])])
    return problems


def getProblemJSON(problemTitle):
    '''
    Retrieve problem information stored in json dictionary
    '''
    print(problemTitle)
    problem = func.findInfo('questions', problemTitle, 'problemName', fetchOne = True)
    print(problem)
    return '{"name": "' + problemTitle + '", "description": "{}", "testCases" : {}, "hiddenTestCases" : {}'.format(problem[2], problem[3], problem[4]) + '}'

@app.route('/base')
def base():
    return render_template("base.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
