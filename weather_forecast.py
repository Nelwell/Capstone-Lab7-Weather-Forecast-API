import os
import requests
from datetime import datetime
from pprint import pprint

key = os.environ.get('open_weather_key')  # environment variable
query = {'q': 'minneapolis,us', 'units': 'imperial', 'appid': key}  # dictionary to store params

url = 'http://api.openweathermap.org/data/2.5/forecast'  # base url

data = requests.get(url, params=query).json()  # gets data in JSON format
pprint(data)

fcst_data_interval_list = data['list']

for fcst in fcst_data_interval_list:
    temp = fcst['main']['temp']
    timestamp = fcst['dt']
    valid_datetime = datetime.fromtimestamp(timestamp)
    print(f'At {valid_datetime} the temperature will be {temp} °F')
