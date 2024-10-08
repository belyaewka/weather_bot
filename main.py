from rp_five import RpFive
from open_weather import Openweather
import requests
from config import BOT_TOKEN, chat_id, LAT, LON, API_TOKEN
import logging
from bs4 import BeautifulSoup
from datetime import datetime


# root logger configuration
logging.basicConfig(filename='/home/weather/weather.log',
                    format='%(asctime)s '
                           'LOGGER=%(name)s '
                           'MODULE=%(module)s.py '
                           'FUNC=%(funcName)s '
                           ' %(levelname)s '
                           ' %(message)s ',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level='INFO',
                    encoding='utf8')

# creating a logger
logger = logging.getLogger('weather_bot')


if __name__ == '__main__':

    # set initial values for variables
    soup = None  # should change to Beautifulsoup object, if all is all right
    op = None  # should change to Openweather object, if all is OK
    message = 'Ошибка получения данных'  # it will change if data receiving is OK, otherwise the message will not change

    # request rp5.ru and making Beautifulsoup object from response.text
    try:
        response_rp5 = requests.get(
            'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-'
            '%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5_(%D1%81%D0%B5%D0%B2-%D0%B7%D0'
            '%B0%D0%BF%D0%B0%D0%B4)')

        if response_rp5.status_code == 200:
            logger.info(f'Request to rp5.ru was successful, code={response_rp5.status_code}')
            text = response_rp5.text
            soup = BeautifulSoup(text, 'html.parser')
            logger.info('Beautifulsoup object from rp5.ru was created')

    except Exception as e:
        logger.error(f'There was an error during request to rp5.ru {e}')

    # request OpenWeatherMap.org and making Openweather object
    try:
        response_open = requests.post(
            f'https://api.openweathermap.org/data/2.5/weather?lat='
            f'{LAT}&lon={LON}&date={datetime.now().strftime("%Y-%m-%d")}'
            f'&appid={API_TOKEN}&units=metric', timeout=10)

        if response_open.status_code == 200:
            logger.info(f'Request to OpenWeatherMap.org was successful, code={response_open.status_code}')
            data = response_open.json()
            op = Openweather(data)  # making Openweather object with data from OpenWeatherMap API
    except Exception as e:
        op = None
        logger.error(f'There was an error during request to OpenWeatherMap: {e}')

    # prepare the message depending on data collection result (first rp5.ru data, if fail - OpenWeather)
    if soup:  # if rp5 request succesful and Beautifulsoup object exists
        try:
            rp5 = RpFive(soup)
            message = str(rp5)
        except Exception as e:
            logger.error(f'RpFive object creating error {e}')
            if op:
                message = str(op)
            else:
                logger.error('Total data receiving error')  # could not receive data from both sources

    # send message to telegram chat with {chat_id}
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.post(url)
        logger.info(f'Message to chat_id {chat_id} was succesfully sent')
    except Exception as e:
        print('Total ERROR')
        logger.error(f'Message to telegram chat {chat_id} was NOT sent. ERROR : {e}')
