#desktop assistant!
from gtts import gTTS				#Google Text to Speech
import speech_recognition as sr 	#Recognize user's speech
import os							#Interact with Operating system
import re
import webbrowser					#Interact with default web browser
import smtplib						#Used to send e-mail.
import requests
#from weather import Weather 		#For current and forecast weather.

def talk(audio):
	print(audio)
	for line in audio.splitlines():
		os.system("say" + audio)

	#mpg123 could be installed, or use system's inbuilt say command.
	#old code:
	'''tts = gTTS(text=audio, lang='en'
	tts.save(log.mp3')
	os.system('mpg123 log.mp3')
	'''

#Listens for commands
def userCommand():
	r = sr.Recognizer()				#Recognize speech

	#Will use default mic for commmands
	with sr.Microphone() as source:
		print('I am ready for your next command')
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration = 1)
		audio = r.listen(source)

	try:
		command = r.recognize_google(audio).lower()
		print('You said: ' + command + '\n')

	#loop back if audio is not recognizeable
	except sr.UnknownValueError:
		print('Oh no, your last command couldn\'t be heard.')
		jasper(usercommand())

	return command

#Statements for executing commands
def jasper(command):
	#re-used variables
	firefox_path = '/usr/bin/firefox'

	#Chatting
	if 'hello jasper' in command:
		talk('Hello Levi.  What are we working on today?')

	elif 'joke' in command:
		res = requests.get('https://icanhazdadjoke.com/', headers = {"Accept":"application/json"})
		if res.status_code == requests.codes.ok:
			talk(str(res.json()['joke']))
		else:
			talk('Uh oh, I\'ve run out of jokes!')
	#Webbrowser
	elif "open reddit python" in command:
		url = 'https://www.reddit.com/r/python'
		webbrowser.get(firefox_path).open(url)

	elif  'search' in command:
		talk('What would you like to look up?')
		search = userCommand()
		webbrowser.get(firefox_path).open(search)

	#Messaging
	elif 'email' in command:
		talk('Who is the recipent')
		recipient = userCommand()

		if 'Gabby' in recipient:
			talk('What should I say')
			content = userCommand()

			#init gmail SMTP
			mail = smtplib.SMTP('smtp.gmail.com', 587)

			#identify to server
			mail.ehlo()

			#encrypt session
			mail.starttls()

			#login
			mail.login('senderemail@whatever.com', 'password')

			#Send mail
			mail.sendmail('PERSON NAME', 'recieveremail@whatever.com', content)

			#close the connection
			mail.close()

			talk('Email Sent')
			
	'''elif 'weather' in command:
	talk('Do you want current weather or the forcast?')
	weather = userCommand()
	if weather == 'current':
		reg_ex = re.search('current weather in(.*)', command)
		if reg_ex:
			city = reg_ex.group(1)
			weather = Weather()
			location = weather.lookup_by_location(city)
			condition = location.condition()
			talk('The current weather in %s is %s.  The temperature is %.1f degree' % (city, condition.text(), (int(condition.text()) -32)/1.8))
	elif weather == 'forcast':
		reg_ex = re.search('weather forecast in(.*)', command)
		if reg_ex:
			city = reg_ex.group(1)
			weather = Weather()
			location = weather.lookup_by_location(city)
			forecasts = location.forecast()
			for i in range (0, 3):
				talk('On %s will it %s.  The maximum temperature will be %.1f degree.'
					'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))'''

	talk('I am ready for your command.')

#loop to continue executing multiple commands.
while True:
	jasper(userCommand())