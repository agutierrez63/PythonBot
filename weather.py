"""
Author:  Adrian Gutierrez
Project: K.A.R.A.
Kinetic Artificial Realistic Assistant
Updated: 24 Feb 2019
"""

"""
Python prgogram to find current
weather details of any city
using openweathermap api
"""
import requests, json
import functions as func
from time import sleep

api_key = ""
base_url = ""
forecast_url = ""

def currentWeather(command):
    func.talkToMe("Ok, for what city?")
    response = func.myCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + response
    res = requests.get(complete_url + "&units=imperial")
    x = res.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main" key in variable y
        y = x["main"]

        # store the value corresponding to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding to the "humidity" key of y
        current_humidity = y["humidity"]

        # store the value of "weather" key in variable z
        z = x["weather"]

        # store the value corresponding to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        func.talkToMe("The temperature is currently " +
                      str(current_temperature) + " degrees")
        func.talkToMe("Humidity is currently at " +
                      str(current_humidity) + "%")
        func.talkToMe("Weather condition: " +
                      str(weather_description))
    else:
        func.talkToMe("I'm sorry, I couldn\'t find the city you asked for.")

def forecastWeather(command):
    func.talkToMe("Ok, for what city?")
    response = func.myCommand()
    complete_url = forecast_url + "appid=" + api_key + "&q=" + response
    res = requests.get(complete_url + "&units=imperial")
    x = res.json()

    location_data = {
        'city': x['city']['name'],
        'conutry': x['city']['country']
    }

    current_date = ''

    func.talkToMe('Ok, here is your 5-day weather forecast for ' + response)
    for item in x['list']:
        time = item['dt_txt']
        next_date, hour = time.split(' ')
        if current_date != next_date:
            current_date = next_date
            year, month, day = current_date.split('-')
            date = { 'y': year, 'm': month, 'd':day }
            print('\n{m}/{d}/{y}'.format(**date))

        hour = int(hour[:2])

        if hour < 12:
            if hour == 0:
                hour = 12
            meridiem = 'AM'
        else:
            if hour > 12:
                hour -= 12
            meridiem = 'PM'
    
        print('\n%i:00 %s' % (hour, meridiem))

        temperature = item['main']['temp']

        description = item['weather'][0]['description']

        print('Weather condition: %s' % description)
        print('Farenheit: ' + str(temperature))
        sleep(1)
