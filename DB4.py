#!/usr/bin/python

import sqlite3

user = raw_input("USER? ")

conn = sqlite3.connect("DB.db", check_same_thread=False)
c = conn.cursor()
sql = "CREATE table if not exists "+ user + "(unix REAL, name TEXT, type TEXT, value TEXT, location TEXT)"
c.execute(sql)
print "Opened database successfully"

def ReadNMR():
    cursor = conn.execute('SELECT max(unix) FROM '+ user)
    max_id = cursor.fetchone()[0]
    if isinstance(max_id, float):
        return max_id + 1
    else:
        return 1

nmr = ReadNMR()

while True:
    goal = raw_input("Read or Write: ")
    if(goal == "R"):    
        sql = "SELECT unix, name, type, value, location from " + user
        cursor = conn.execute(sql)
        for row in cursor:
            print "ID       = ", row[0]
            print "NAME     = ", row[1]
            print "TYPE     = ", row[2]
            print "VALUE    = ", row[3]
            print "LOCATION = ", row[4], "\n"
    elif(goal == "W"):
        nm = raw_input("name:    ")
        tp = raw_input("type:    ")
        vl = raw_input("value:   ")
        lc = raw_input("location:")
        sql = "INSERT into " + user + " VALUES ("+ str(nmr) + ",'" + nm + "', '"+ tp + "','"+ vl +"', '"+ lc + "')"
        c.execute(sql)
        nmr = nmr + 1
        print(nmr)
        conn.commit()
    elif(goal == "S"):
        query = raw_input("What do you want to search?")
        cursor = c.execute('SELECT * FROM ' + user + ' WHERE type=?', (query,))
        for row in cursor:
            print "VALUE    = ",row[3]
            print "LOCATION = ",row[4], "\n"
    else:
        print(ReadNMR())
    

print "Operation done successfully";
conn.close()
