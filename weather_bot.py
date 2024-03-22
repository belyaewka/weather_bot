import requests
from datetime import datetime
import math
import os
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = '6869510590:AAES08owvRm0JABKJEybzU3Q-VTH9ej7QmA'
TOKEN = '9e778ebba87c3de82c6d7b1ea26a890d'

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

LAT = 59.9844
LON = 30.2406
# lat = 59.9911
# lon = 30.1597

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# id бота 6869510590
# id чата 811509730


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет {message.from_user.full_name}! Нажми кнопку и я пришлю сводку погоды {bot.id}")


@dp.message_handler()
async def get_weather(message: types.Message):
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat='
        f'{LAT}&lon={LON}&date={datetime.now().strftime("%Y-%m-%d")}'
        f'&appid=9e778ebba87c3de82c6d7b1ea26a890d&units=metric')
    data = response.json()

    city = data["name"]
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    weather_description = data["weather"][0]["main"]

    # рассвет и закат
    sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])

    # продолжительность дня
    length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(
        data["sys"]["sunrise"])

    await message.reply(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    f"Погода в городе: {city}\nТемпература: {cur_temp}°C \n"
                        f"{code_to_smile[weather_description]}\n"
    f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
    f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
    f"Хорошего дня!")
    # print(f'Город: {city}')
    # print(data['coord'])
    # print(f'{code_to_smile[weather_description]}')
    # print(f'Температура: {cur_temp} С')
    # print(f'Влажность: {humidity} %')
    # print(f'Давление: {pressure} hPa')
    # print(f'Ветер: {wind} м/с')
    # print(f'Рассвет: {sunrise_timestamp}')
    # print(f'Закат: {sunset_timestamp}')
    # print(f'Продолжительность дня: {length_of_the_day}')


if __name__ == "__main__":
    # С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
    executor.start_polling(dp)
