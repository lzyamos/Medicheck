import mysql.connector
database = mysql.connector.connect(
    host = 'localhost',
    user = 'amos',
    passwd = 'Amosw@2002'
    
)

cursorObject = database.cursor()
cursorObject.execute("CREATE DATABASE Medicheck")

print("Running database")