from dataclasses import dataclass
from datetime import datetime
import math

# answer_example = {'base': 'stations',
#           'clouds': {'all': 100},
#           'cod': 200,
#           'coord': {'lat': 59.9844, 'lon': 30.2406},
#           'dt': 1726044515,
#           'id': 489226,
#           'main': {'feels_like': 17.17,
#                    'grnd_level': 1008,
#                    'humidity': 81,
#                    'pressure': 1010,
#                    'sea_level': 1010,
#                    'temp': 17.27,
#                    'temp_max': 17.27,
#                    'temp_min': 17.1},
#           'name': 'Staraya Derevnya',
#           'sys': {'country': 'RU',
#                   'id': 197864,
#                   'sunrise': 1726024694,
#                   'sunset': 1726072397,
#                   'type': 2},
#           'timezone': 10800,
#           'visibility': 10000,
#           'weather': [{'description': 'overcast clouds',
#                        'icon': '04d',
#                        'id': 804,
#                        'main': 'Clouds'}],
#           'wind': {'deg': 156, 'gust': 8.32, 'speed': 3.37}}

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


@dataclass
class Openweather:
    response: dict

    @staticmethod
    def conv_deg_to_wind(deg):
        val = int((deg / 22.5) + .5)
        arr = ["Север", "Северо-Северо-Восток", "Северо-Восток", "Востоко-Северо-Восток", "Восток",
               "Востоко-Юго-Восток",
               "Юго-Восток", "Юго-Юго-Восток", "Юг", "Юго-Юго-Запад", "Юго-Запад", "Запад-Юго-Запад", "Запад",
               "Запад-Север-Запад", "Северо-Запад", "Северо-Северо-Запад"]
        return arr[(val % 16)]

    def __post_init__(self):
        self.city = self.response["name"]
        self.curr_temp = self.response["main"]["temp"]
        self.feel_temp = self.response['main']['feels_like']
        self.humidity = self.response["main"]["humidity"]
        self.pressure = self.response["main"]["pressure"]
        self.wind = self.response["wind"]["speed"]
        self.wind_dir = self.conv_deg_to_wind(self.response['wind']['deg'])
        self.weather_description = self.response["weather"][0]["main"]

        # time of sunrise and sunset
        self.sunrise_timestamp = datetime.fromtimestamp(self.response["sys"]["sunrise"]).strftime("%H:%M")
        self.sunset_timestamp = datetime.fromtimestamp(self.response["sys"]["sunset"]).strftime("%H:%M")

        self.length_of_the_day = datetime.fromtimestamp(self.response["sys"]["sunset"]) - datetime.fromtimestamp(
            self.response["sys"]["sunrise"])

    def __str__(self):
        return (f"{datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
                f"Погода в городе: {self.city}\n"
                f"Температура: {self.curr_temp}°C \n"
                f"Ощущается как {self.feel_temp}°C \n"
                f"{code_to_smile[self.weather_description]}\n"
                f"Влажность: {self.humidity}%\n"
                f"Давление: {math.ceil(self.pressure / 1.333)} мм.рт.ст\n"
                f"Ветер: {self.wind} м/с, {self.wind_dir} \n"
                f"Восход солнца: {self.sunrise_timestamp}\n"
                f"Закат солнца: {self.sunset_timestamp}\n"
                f"Продолжительность дня: {self.length_of_the_day}\n"
                f"Хорошего дня, пупчанчики 💖!")
