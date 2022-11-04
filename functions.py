"""
Author: Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 8 August 2019
"""
import json
import msvcrt
import pyaudio
import pyttsx3
import os
import re
import requests
import sys
import speech_recognition as sr
import soundscraper as scraper
import time
import wikipedia
import webbrowser
import wolframalpha
from gtts import gTTS
from pathlib import Path
from pydub import AudioSegment

engine = pyttsx3.init()
t0 = time.time()

# listens for commands
def myCommand():
	r = sr.Recognizer()

	# will use computer mic as default (change to kinect)
	with sr.Microphone(0) as source:
		print('listening...')
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)

	try:
		command = r.recognize_google(audio).lower()
		print('You said: ' + command + '\n')

	# loop back to continue to listen for command
	except sr.UnknownValueError:
		print('Your last command couldn\'t be heard')
		command = myCommand()

	return command

# voice of assistant
def talkToMe(audio):
	print(audio)
	for line in audio.splitlines():
		try:
			engine.setProperty('voice','')
			engine.say(audio)
			engine.runAndWait()
		except KeyboardInterrupt:
			print('\nKeyboard Interrupt')
			print('Exit')
			exitSystem()

# will play songs avaialable in the media folder
def media(command):
	if 'sing' in command:
		talkToMe('I won\'t sing, but I\'ll play a song for you')
		talkToMe('What would you like me to play?')
		file = myCommand()
		talkToMe('OK, now playing ' + file)
		os.startfile('C:/Users/PC/Music/iTunes/iTunes Media/Music/' + file + '.mp3')
	else:
		talkToMe('OK, what do you want me to play for you?')
		file = myCommand()
		talkToMe('OK, now playing ' + file)
		os.startfile('C:/Users/PC/Music/iTunes/iTunes Media/Music/' + file + '.mp3')

# jokes are told using icanhazdadjokes api
def joke(command):
	res = requests.get(
		'https://icanhazdadjoke.com/',
		headers={"Accept":"application/json"}
	)
	if res.status_code == requests.codes.ok:
		talkToMe(str(res.json()['joke']))
	else:
		talkToMe('oops! I ran out of jokes')

# words are defined using the oxford dictionaries' api
def define(command):
	talkToMe('OK, what word would you like me to define?')
	response = myCommand()

	app_id = '060f858f'
	app_key = '73e075276aeca107979ddd627795d17a'
	language = 'en'
	word_id = response
	url = 'https://od-api.oxforddictionaries.com/api/v2'  + language + '/'  + word_id.lower()

	talkToMe("OK, here is what i found for the word " + response)
	r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
	json_data = json.loads(r.text)
	for i in json_data["results"]:
		for j in i["lexicalEntries"]:
			for k in j["entries"]:
				for v in k["senses"]:
					print(v["definitions"])

# response to common questions
def questions(command):
	if 'how are you' in command:
		talkToMe('I\'m fine, thanks for asking.')

	elif 'who are you' in command:
		talkToMe('My name is Kara. I am an assistant created by Adrian to assist him in his daily life.')

	elif 'what are you' in command:
		talkToMe('I am a kinteic artificial realistic assistant.')

	elif 'your name' in command:
		talkToMe('My name is Kara. Nice to meet you.')

# opn/launch specific applications on my device
def launch(command):
	if 'google' in command:
		talkToMe('OK, on it...')
		reg_ex = re.search('open google(.*)', command)
		url = 'https://www.google.com/'
		webbrowser.open(url)
		talkToMe('Done!')

	elif 'youtube' in command:
		talkToMe('OK, on it...')
		reg_ex = re.search('open youtube(.*)', command)
		url = 'https://www.youtube.com/'
		webbrowser.open(url)
		talkToMe('Done!')

	elif 'soundcloud' in command:
		talkToMe('OK, I\'m on it...')
		scraper.soundScraper(command)

# read input file and print
def printMenu(filename):
	f = open(filename, 'r')
	file_contents = f.read()
	print(file_contents)
	f.close()

# set up or check reminders 
def reminder():
	if command in ['create', 'setup']:
		talkToMe("OK, just tell me what you want to be reminded about.")
		message = myCommand()
		talkToMe("OK, when do you want me to remind you?")
		time = mycommand()
	elif command in ['my list', 'list', 'my reminders', 'reminders']:
		talkToMe('OK, here is a list of reminders')
		filename = ''
		f = open(filename, 'r')
		file_contents = f.read()
		talkToMe('OK, here is what I found')
		print(file_contents)
		f.close()


# if command is not defined, do series of searches
def search(command):
	talkToMe('I don\'t know what you mean.')
	talkToMe('Perhaps I can search it for you?')
	print('yes or no')
	response = myCommand()
	if 'yes' in response:
		try:
			app_id = 'https://www.google.com/'
			client = wolframalpha.Client(app_id)
			res = client.query(command)
			answer = next(res.results).text
			talkToMe('OK, here\'s is what I found.')
			print(answer)

		except:
			talkToMe('OK, here is what I found.')
			print(wikipedia.summary(command))

		else:
			url = ''
			talkToMe('OK, here\'s what I found.')
			webbrowser.open(url + command, new=0)

	elif 'no' in command:
		talkToMe('OK, cancelling search.')

	else:
		talkToMe('OK, nevermind')

# update packages
"""
def updateSystem():
	talkToMe('Ok, updating system now...')
	updateCmd = 'pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U'
	os.system(updateCmd)
"""

# close the program
def exitSystem():
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)
