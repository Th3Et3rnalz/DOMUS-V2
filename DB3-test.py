#!/usr/bin/python

import sqlite3
from passlib.hash import pbkdf2_sha256


conn = sqlite3.connect('DB.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE table if not exists LOGIN(unix real, username TEXT, password TEXT, hash TEXT)''')
print "Opened database successfully"

def ReadNMR():
    cursor = conn.execute('SELECT max(unix) FROM LOGIN')
    max_id = cursor.fetchone()[0]
    if isinstance(max_id, float):
        return max_id + 1
    else:
        return 1

nmr = ReadNMR()

while True:
    goal = raw_input("Read or Write")
    if(goal == "R"):
        cursor = conn.execute("SELECT unix, username, password, hash from LOGIN")
        for row in cursor:
            print "ID       = ", row[0]
            print "USER     = ", row[1]
            print "PASSWORD = ", row[2]
            print "HASH     = ", row[3], "\n"
    elif(goal == "W"):
        user = raw_input("Username")
        psw = raw_input("Password")
        hash = pbkdf2_sha256.encrypt(psw)
        sql = "INSERT into LOGIN VALUES ("+ str(nmr) + ",'" + user + "', '"+ psw + "','"+ hash +"')"
        c.execute(sql)
        nmr = nmr + 1
        print(nmr)
        conn.commit()
    elif(goal == "S"):
        query = raw_input("What do you want to search?")
        cursor = c.execute('SELECT * FROM LOGIN WHERE username=?', (query,))
        for row in cursor:
            print "PASSWORD =",row[2]
    else:
        print(ReadNMR())
    

print "Operation done successfully";
conn.close()
