import sqlite3 #enable control of an sqlite database

DB_FILE="../data/gen.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

def main():
    try:
        userHead = {"ID":"INTEGER PRIMARY KEY", "username":"TEXT", "password":"TEXT", "points" : "INTEGER", "questionsSolved" : "TEXT","country": "TEXT", "isAdmin" : "TINYINT(1)"}
        createTable("users", userHead)

        questionHead = {"ID" : "INTEGER PRIMARY KEY", "problemName" : "TEXT", "description": "TEXT", "test cases": "TEXT",  "value": "INTEGER"}
        createTable( "questions", questionHead)

        closeDB()

    except:
        print('not created')

def createTable(tableName, fieldNames):
	'''creates new table with list of parameters to be taken in'''
	commandArgs = "("
	colTypes = []
	for name in fieldNames:
		commandArgs += name + " " + fieldNames[name] + ","
		colTypes.append(fieldNames[name])
	commandArgs = commandArgs[:-1]
	commandArgs += ")"
	c.execute("CREATE TABLE " + tableName + " "+ commandArgs)

def closeDB():
	db.commit() #save changes
	db.close()  #close database

main()