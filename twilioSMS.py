"""
Author:  Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 28 Feb 2019
"""
import json
import re
import requests
import functions as func
from twilio.rest import Client

# Your Account SID and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

def sendText(command):
	func.talkToMe('Ok, who is the recipient?')
	phoneNumber = input('Number: ')
	type(phoneNumber)
	func.talkToMe('OK, what do you want to say?')
	txt = input('Message: ')
	type(txt)
	message = client.messages \
                .create(
                     body=txt + ' From Kara, Adrian\'s Assistant',
                     from_='+16617658949',
                     to=phoneNumber
                 )
	# print(message.sid)
	func.talkToMe('Ok, I\'ll send a text right now')