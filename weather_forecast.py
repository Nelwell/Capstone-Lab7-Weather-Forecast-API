import os
import requests
from datetime import datetime
import logging

wx_key = os.environ.get('open_weather_key')  # environment variable
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
query = {'q': 'minneapolis,us', 'units': 'imperial', 'appid': wx_key}  # dictionary to store params
url = 'http://api.openweathermap.org/data/2.5/forecast'  # base url


def main():
    location = get_location()
    weather_data, error = get_wx_data(location, wx_key)
    if error:
        print('Sorry, could not get weather for that location or locations doesn\'t exist')
    else:
        display_wx_forecast(weather_data, location)


def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of the city: ').upper().strip()

    while len(country) != 2 or not country.isalpha():
        country = input('Enter a 2-letter country code: ').upper().strip()

    location = f'{city},{country}'
    return location


def get_wx_data(location, wx_key):
    try:
        query = {'q': location, 'units': 'imperial', 'appid': wx_key}
        response = requests.get(url, params=query)
        response.raise_for_status()  # Raise exception for 400 or 500 errors
        data = response.json()  # this may error too, if response is not JSON
        return data, None
    except Exception as e:
        logging.exception(f'Error decoding response into JSON')
        return None, e


def display_wx_forecast(weather_data, location):
    fcst_data_list = weather_data['list']

    print(f'\n*** HERE\'S YOUR {location} 3-HOURLY, 5-DAY FORECAST ***')
    for element in fcst_data_list:
        temp = element['main']['temp']
        wind_spd = element['wind']['speed']
        timestamp = element['dt']
        # UTC time, we don't know where the user is at.
        # Local time on their computer will make no sense for areas outside their time zone.
        valid_datetime = datetime.utcfromtimestamp(timestamp)
        print(f'\nAt {valid_datetime}UTC:\n'
              f'\tTemperature: {temp}°F')
        wx_desc_list = element['weather']
        for wx in wx_desc_list:
            wx_desc = wx['description']
            print(f'\tWeather: {wx_desc}')
        print(f'\tWind Speed: {wind_spd}mph')


if __name__ == '__main__':
    main()
