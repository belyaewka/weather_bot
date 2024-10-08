from dataclasses import dataclass
from dateutil import parser
import datetime
import logging
from bs4 import BeautifulSoup
import re


@dataclass
class RpFive:
    soup: BeautifulSoup

    @staticmethod
    def get_short_forecast(soup: BeautifulSoup) -> list:
        """parse and get short forecast"""
        try:
            res2 = soup.find_all(attrs={"id": "forecastShort-content"})
            s = res2[0].find('b').text.split('°C°F')
            return (s[0].strip() + s[2].strip() + s[4].strip()).split('Завтра')
        except:
            logging.error('Cannot parse short forecast')
            return ['error', 'error']

    @staticmethod
    def get_clouds(soup: BeautifulSoup) -> tuple:
        """parse and get information about clouds"""
        try:
            cloudy = soup.find('div', class_='cc_0')
            clouds = re.findall(string=str(cloudy), pattern=r'\([А-Яа-я]+.*\%')[0].strip('(')
            cloud_state = re.findall(string=str(cloudy), pattern=r'\;[А-Яа-я]+')[0].strip(';')
        except:
            cloud_state = 'error'
            clouds = 'error'
            logging.error('Cannot parse clouds')
        return cloud_state, clouds

    @staticmethod
    def get_wind(soup: BeautifulSoup) -> str:
        """parse and get wind data from Soup"""
        try:
            w = soup.find('div', class_='wv_0')
            s = str(w).split("\'")
            wind = s[3]
        except:
            wind = 'error'
            logging.error('Cannot parse wind')
        return wind

    @staticmethod
    def get_pressure(soup: BeautifulSoup) -> str:
        """parse and get pressure data from Soup"""
        try:
            p = soup.find('div', class_='p_0')
            pressure = p.text
        except:
            pressure = 'error'
            logging.error('Cannot parse pressure')
        return pressure

    @staticmethod
    def get_wind_direction(soup: BeautifulSoup) -> str:
        """parse and get wind direction data from Soup"""
        try:
            wd = soup.find('td', class_='grayLittled underlineRow')
            wind_direction = wd.text
        except:
            wind_direction = 'error'
            logging.error('Cannot parse wind direction')
        return wind_direction

    @staticmethod
    def get_humidity(soup: BeautifulSoup) -> str:
        """parse and get humidity data from Soup"""
        found = soup.find('tr', class_='brief')
        try:
            humidity = found.find('td', class_='d underlineRow').text
        except:
            try:
                humidity = found.find('td', class_='d underlineRow red').text
            except:
                try:
                    humidity = found.find('td', class_='n underlineRow red').text
                except:
                    humidity = 'error'
                    logging.error('Cannot parse humidity')

        return humidity

    @staticmethod
    def sunrise(soup: BeautifulSoup) -> str:
        """parse and get sunrise time from Soup"""
        try:
            find = soup.find('td', class_='d underlineRow grey')
            res = find.text
        except:
            res = 'error'
            logging.error('Cannot parse sunrise')

        return res

    @staticmethod
    def sunset(soup: BeautifulSoup) -> str:
        """parse and get sunset time from Soup"""
        try:
            find = soup.find('td', class_='d2 underlineRow litegrey')
            res = find.text

        except:
            res = 'error'
            logging.error('Cannot parse sunset')

        return res

    @staticmethod
    def day_length(sunrise_time: str, sunset_time: str) -> datetime.timedelta | str:
        """calculate day length from sunrise and sunset time"""
        try:
            d1 = parser.parse(sunrise_time)
            d2 = parser.parse(sunset_time)
            diff = d2 - d1
        except:
            diff = 'error'
            logging.error('Cannot get day length')
        return diff

    @staticmethod
    def choose_sign(string):
        """plus is not acceptable for telegram message, this function change + to appropriate emoji """
        return string.replace('+', '\U00002795') if "+" in string else string

    def __post_init__(self):
        # short forecast
        self.today = self.choose_sign(self.get_short_forecast(self.soup)[0])
        self.tomorrow = self.choose_sign(self.get_short_forecast(self.soup)[1])

        # clouds
        self.cloud_state = self.get_clouds(self.soup)[0]
        self.clouds = self.get_clouds(self.soup)[1]

        # wind
        self.wind = self.get_wind(self.soup)

        # pressure
        self.pressure = self.get_pressure(self.soup)

        # wind direction
        self.wind_direction = self.get_wind_direction(self.soup)

        # humidity
        self.humidity = self.get_humidity(self.soup)

        # sunrise
        self.sunrise = self.sunrise(self.soup)

        # sunset
        self.sunset = self.sunset(self.soup)

        # day_length
        self.day_len = self.day_length(self.sunrise, self.sunset)

    def __str__(self):
        return (f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
                f"Погода в городе Санкт-Петербург\n"
                f"{self.today}\n"
                f"Облачность: {self.cloud_state}, {self.clouds} \n"
                f"Влажность: {self.humidity} %\n"
                f"Давление: {self.pressure} мм.рт.ст\n"
                f"{self.wind}, {self.wind_direction} \n"
                f"Восход солнца: {self.sunrise}\n"
                f"Закат солнца: {self.sunset}\n"
                f"Продолжительность дня: {self.day_len}\n"
                f"Завтра{self.tomorrow}\n\n"
                f"Хорошего дня!")
