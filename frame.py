import web, sqlite3
from web import form
import RPi.GPIO as GPIO

# ---GPIO SETUP---
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# ---SQLITE3 DATABASE SETUP---
conn = sqlite3.connect("DB.db", check_same_thread=False)
print "Opened database successfully"

# ---VARIABLE(S)---
elements = []

def cleanup(value):
        answer = value.replace("'", "")
        answer = answer.replace("u", "")
        return answer

def writeNewState(username, state):
	userNm = cleanup(username)
	stateNm = cleanup(state)

	Value = "NOT A LED"
	if stateNm.replace("led","").isdigit() == 1: #name as 'led38' igve us the pin number so we can read the value
                pinNm = stateNm.replace("led", "") #I do this after the if statement because some words have 'led' in them (i.e. deskled)
                GPIO.setup(int(pinNm), GPIO.OUT)
                Value = GPIO.input(int(pinNm))
	sql = "UPDATE " + userNm + " SET value = '" + str(Value) + "' WHERE name = '"+ stateNm +"'"
	print "Updating the values in the sqlite3 database."
	conn.execute(sql)
	conn.commit()
	return "Status updated in the database"

def toggleLed(ledn):
	GPIO.setup(ledn, GPIO.OUT)
        if (GPIO.input(ledn) == 1):
		GPIO.output(ledn, GPIO.LOW)
        elif (GPIO.input(ledn) == GPIO.LOW):
                GPIO.output(ledn, GPIO.HIGH)
        else:
                print "WTF"
        return GPIO.input(ledn)

def checkUser(username, password):
	cursor = conn.execute('SELECT * FROM LOGIN WHERE username=?', (username,))
	for row in cursor:
                if row[2] == password:
			global user
			user = username
			sql = "SELECT unix, name, type, value, location from "  + user
			cursor = conn.execute(sql)
			elements = []
			global  elLen
			elLen = 0
			for row in cursor:
				elLen += 1
				""" Remove the captions for troubleshooting
				print "ID       = ", row[0]
				print "NAME     = ", row[1]
				print "TYPE     = ", row[2]
				print "VALUE    = ", row[3]
				print "LOCATION = ", row[4], "\n """
				elements.append(row[1] + ".")
				elements.append(row[2] + ".")
				elements.append(row[3] + ".")
				elements.append(row[4] + ", ")
		else:
			print "No such user....."
				
	global newEl
	newEl = "".join(elements)
	newEl = newEl.replace("'", "")
	
	return "Success baby!!"

urls = (
    '/', 'index',
    '/btn(.*)', 'btnclick'
    )
    
myform = form.Form( 
    form.Textbox("Username",
        form.notnull), 
    form.Password("Password", 
        form.notnull)
    )

render = web.template.render('/home/pi/Templates/')
app = web.application(urls, globals())

class index:
    def GET(self):
        print "We have a user!"
        form = myform()
        return render.frameLogin(form)

    def POST(self): 
        form = myform() 
	if not form.validates():
	   return render.frameLogin(form)
	else:
		checkUser(form.d.Username, form.d.Password)
        return render.frame(newEl, elLen)    

class btnclick:
    def GET(self, name):
        status = "FILLER"
        if web.input().name.replace("led", "").isdigit() == 1:
                status = toggleLed(int(web.input().name.replace("led","")))
	returned = writeNewState(web.input().username, web.input().name)
        return web.input().name, status



if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
