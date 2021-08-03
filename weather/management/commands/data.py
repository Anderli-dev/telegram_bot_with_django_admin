import requests
import json

URL = 'http://api.openweathermap.org/data/2.5/weather?id=707052&lang=fr&appid=f2d4edaf13c9825eeacfbe0385cc30ae'


def get_temp():
    response = requests.get(URL)
    data = json.loads(response.text)
    num = round(data['main']['temp']-273.15, 1)

    return num
