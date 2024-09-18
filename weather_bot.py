import requests
from datetime import datetime
import math

from config import TOKEN, API_TOKEN, chat_id

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

# Старая Деревня
LAT = 59.9844
LON = 30.2406

# convert degrees to wind direction
def conv_deg_to_wind(deg):
    val = int((deg / 22.5) + .5)
    arr = ["Север", "Северо-Северо-Восток", "Северо-Восток", "Востоко-Северо-Восток", "Восток", "Востоко-Юго-Восток",
           "Юго-Восток", "Юго-Юго-Восток", "Юг", "Юго-Юго-Запад", "Юго-Запад", "Запад-Юго-Запад", "Запад",
           "Запад-Север-Запад", "Северо-Запад", "Северо-Северо-Запад"]
    return arr[(val % 16)]


# make a request to API
response = requests.get(
    f'https://api.openweathermap.org/data/2.5/weather?lat='
    f'{LAT}&lon={LON}&date={datetime.now().strftime("%Y-%m-%d")}'
    f'&appid=9e778ebba87c3de82c6d7b1ea26a890d&units=metric')

# get request
data = response.json()

# get parameters
city = data["name"]
cur_temp = data["main"]["temp"]
feel_temp = data['main']['feels_like']
humidity = data["main"]["humidity"]
pressure = data["main"]["pressure"]
wind = data["wind"]["speed"]
wind_dir = conv_deg_to_wind(data['wind']['deg'])
weather_description = data["weather"][0]["main"]

# time of sunrise and sunset
sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

# length of the day
length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(data["sys"]["sunrise"])

message = (f"{datetime.now().strftime('%d-%m-%Y %H:%M')}\nПогода в городе: {city}\nТемпература: {cur_temp}°C \n"
           f"Ощущается как {feel_temp}°C \n"
           f"{code_to_smile[weather_description]}\nВлажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
           f"Ветер: {wind} м/с, {wind_dir} \n"
           f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
           f"Хорошего дня, пупчанчики 💖!")


url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

# send message
if __name__ == '__main__':
    requests.get(url)
