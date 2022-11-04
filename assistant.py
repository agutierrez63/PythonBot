"""
Author:  Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 6 March 2019
"""

"""
TODO:
	- create a reminders function that will
	setup or display reminders
	- create a python file that hold a number arrays
	for cities, responses, etc.
	- weather function:
	if command in arrayList:
		# do something
	else 
		# ask for city name then do something
"""
import datetime
import random
import functions as func
import weather as w
import twilioSMS as sms
import sendEmail as mail
from faces import openEye

currentDT = datetime.datetime.now()
fileMenu = 'C:/Users/PC/Documents/Git/Project/Files/menu.txt'
introMenu = 'C:/Users/PC/Documents/Git/Project/Files/intro.txt'

# if statement for executing commands
def assistant(command):

	if command in ['hey', 'hello', 'hi', 'howdy', 'sup', 'hi kara', 'hello kara', 'hey kara', 'sup kara', 'howdy kara', 'yo', 'yo kara']:
		response = random.choice(['Hi', 'Hey! How are you?', 'Hello', 'Hey', 'Hello! How are you?', 'Hi! How are you?'])
		func.talkToMe(response)

	elif 'what\'s up' in command:
		func.talkToMe('Nothing much')

	elif command in ['how are you', 'i\'m good how are you', 'not bad how are you',
	'who are you', 'what are you', 'what is your name', 'what\'s your name']:
		func.questions(command)

	elif 'open' in command:
		func.launch(command)

	elif 'launch' in command:
		func.launch(command)

	elif 'joke' in command:
		func.joke(command)

	elif 'define' in command:
		func.define(command)

	elif 'song' in command:
		func.media(command)

	elif 'text' in command:
		sms.sendText(command)

	elif 'reminder' in command:
		func.setUpReminder(command)

	elif "camera" in command:
		openEye()

	elif 'time' in command:
		func.talkToMe(currentDT.strftime("%I:%M %p"))

	elif 'date' in command:
		func.talkToMe(currentDT.strftime("%A, %B, %d, %Y"))

	elif 'email' in command:
		mail.sendEmail(command)

	elif 'menu' in command:
		func.printMenu(fileMenu)

	elif 'weather' in command:
		w.currentWeather(command)

	elif 'forecast' in command:
		w.forecastWeather(command)

	elif command in ['thanks', 'thank you', 'thanks kara', 'thank you kara', 'you\'re the best', 'you\'re the best kara', 'thanks for the help']:
		response = random.choice(['No prob', 'No problem', 'Always happy to help', 'I\'m always happy to help', 'That\'s what I\'m here for'])
		func.talkToMe(response)

	elif command in ['goodbye', 'bye', 'shut down', 'exit']:
		response = random.choice(['Bye', 'Goodbye', 'Ok, shutting down...'])
		func.talkToMe(response)
		func.exitSystem()

	else:
		func.search(command)

func.printMenu(introMenu)
func.talkToMe('Hello, my name is Kara. How may I help you?')

# loop to continue executing multiple commands
while True:
	try:
		assistant(func.myCommand())
	except KeyboardInterrupt:
		print('\nKeyboard Interrupt')
		print('Exit')
		func.exitSystem();
