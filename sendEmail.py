"""
Author:  Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 3 April 2019
"""

import smtplib
import socket
import functions as func
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql_connect as connect

me = ""
username = str('')
password = str('')

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "<From the desk of Adrian Gutierrez>"
msg['From'] = me

mycursor = connect.mydb.cursor()

def sendEmail(command):
	func.talkToMe('Who is the recipient?')
	response = func.myCommand()
	query = 'SELECT e_email FROM e_contacts WHERE e_firstName = %s', (response)
	# user_email = mycursor.execute(query)
	mycursor.execute(query)
	to = mycursor.fetchone()
	msg['To'] = to
	func.talkToMe('What would you like me to say?')
	content = input('Message: ')
	type(content)

	"""
	# type email address
	to = input('Email-address: ')
	type(to)
	"""
	# Create the body of the message (a plain-text and an HTML version).
	html = """\
	<html>
	  <head></head>
	  <body>
	  	<b>K.A.R.A. (Assistant)</b><br>
	  	<i>A.I. Assistant</i><br>
	  	<div>Tel: +1(661)765-8949</div>
	  	<div>Email: <a target="_blank" href=""></a></div>
	  </body>
	</html>
	"""
	
	message = content + html

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(content, 'plain')
	part2 = MIMEText(message, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(username, password)
		server.sendmail(me, to, msg.as_string())
		server.close()
		func.talkToMe('Ok, the email has been sent.')
	except Exception as e: 
		func.talkToMe("Hmm, it looks like something when wrong.")
		print(e)
