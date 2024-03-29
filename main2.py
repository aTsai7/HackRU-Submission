from flask import Flask, request, render_template
from twilio import twiml
from get_schedule import *
from mongodb_access import *
from string_manipulation import *
from remind import *
#imports classes

app = Flask(__name__)

s = sched.scheduler(time.time, time.sleep)

@app.route("/sms", methods = ['GET', 'POST'])
def checklist():
	number = request.form['From']
	message_body = request.form['Body']

	if (message_body == "schedule"):
		#RESPONSE TO PHONE; getSchedule() splits up string
		message = get_schedule(get_events(number))

		resp = twiml.Response()
		resp.message(message)
		return str(resp)	#returns message to user
	elif(message_body == "clear"):
		remove_events(number)
	else:
		#PUT USERS INFO IN A MONGODB DATABASE
		if (get_events(number) == "ERROR"):
			#if user isn't present in database add user
			add_user(number, string_manipulation(message_body))
		else:
			#if user is present add event
			add_event(number, string_manipulation(message_body))

		populate(number, string_manipulation(message_body))
	return ('x')



if __name__ == "__main__":
	app.run()
