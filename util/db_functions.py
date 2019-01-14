import sqlite3   #enable control of an sqlite database

DB_FILE="./data/gen.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

#info is a list of fieldValues in order without primary key
def insert(tableName, info):
    '''inserts data into certain table, taking info as a list of parameters'''
    # collect Column Data Names in strings
    c.execute('PRAGMA TABLE_INFO({})'.format(tableName))
    colNames = ''
    i = 0
    for cols in c.fetchall():
        if i == 0:
            i += 1 # primary key will update itself
        else:
            colNames += "'" + cols[1] + "'"+ ','
    colNames = colNames[:-1]
    values = ''
    for val in info:
        values += "'" + str(val) + "'" + ","
    values = values[:-1]
    print("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    c.execute("INSERT INTO {0}({1}) VALUES ({2})".format(tableName,
                                                          colNames ,
                                                          values  ))
    db.commit()

def findInfo(tableName,filterValue,colToFilt,fetchOne = False, search= False):
    '''returns entire record with specific value at specific column from specified db table'''
    if search:
        filterValue = '%' + filterValue + '%'
        eq = 'LIKE'
    else:
        eq = '='

    command = "SELECT * FROM  '{0}'  WHERE {1} {3} '{2}'".format(tableName,colToFilt,filterValue, eq)
    c.execute(command)

    listInfo = []
    if fetchOne:
        info = c.fetchone()
    else:
        info = c.fetchall()
    if info:
        for col in info:
            listInfo.append(col)
    return listInfo

def modify(tableName, colToMod, newVal, filterCol, filterValue):
    print(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterCol, filterValue))
    c.execute(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterCol, filterValue))
    db.commit()

def delete(tableName, filterCol, filterValue):
    print(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterCol, filterValue))
    c.execute(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterCol, filterValue))
    db.commit()

def getAllUsers():
    command = "SELECT * FROM 'users' ORDER BY points"
    c.execute(command)
    return c.fetchall()

def addQuestion(problemName, problem):
    insert('events', [eventName, date, city])
    eventRow = findInfo('events', eventName, 'EventName',fetchOne = True)

'''checks if user solved question; returns true if yes'''
def hasSolved(username,problem):
    user = findInfo('users', username, 'Username', fetchOne = True)
    questionS = user[4]
    problem = findInfo('questions', problem, 'problemName',fetchOne = True)
    if questionS:
        if str(problem[0]) in questionS.split(','):
            return True
        else:
            return False
    else:
        return False

'''gives user points if question is solved'''
def userSolvesQuestion(username,problemName):
    user = findInfo('users', username, 'Username', fetchOne = True)
    questionS = user[4]
    problem = findInfo('questions', problem, 'problemName',fetchOne = True)
    if not hasSolved(username,problemName):
        questionS += str(problem[0]) + ','
        modify('questions', 'questionSolved', questionS,  'username', username)
        point += problem[5]
        modify('users', 'points', points,  'username', username)

def getAllProblems(difficulty):
     return findInfo('questions', difficulty, 'difficulty')
