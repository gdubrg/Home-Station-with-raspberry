from PyQt5 import QtCore, QtGui
from time import sleep
import requests


class ThreadWeatherForecast(QtCore.QThread):

    signal_weather = QtCore.pyqtSignal()
    signal_forecast = QtCore.pyqtSignal()

    def __init__(self, window, config):
        QtCore.QThread.__init__(self)
        self.window = window

        self.city = config['WEATHER']['CITY']
        self.reload_seconds = config['RELOAD SECONDS']['WEATHER']
        self.token = config['WEATHER']['TOKEN']

        self.weather_data = None

        self.temp_min = None
        self.temp_max = None
        self.humidity = None
        self.temp_cur = None
        self.pixmap_cur_weather = QtGui.QPixmap()

        self.date_1 = None
        self.date_2 = None
        self.date_3 = None
        self.date_4 = None
        self.pixmap_day_1 = QtGui.QPixmap()
        self.pixmap_day_2 = QtGui.QPixmap()
        self.pixmap_day_3 = QtGui.QPixmap()
        self.pixmap_day_4 = QtGui.QPixmap()

    def __del__(self):
        self.wait()

    def run(self):
        self.get_current_weather()

    def get_current_weather(self):
        while True:
            self.do_request()
            if self.weather_data is not None:
                self.get_today_weather()
                self.get_forecast()
            sleep(self.reload_seconds)

    def do_request(self):
        url = "https://api.openweathermap.org/data/2.5/forecast?"
        city = "q=" + self.city
        token = self.token
        try:
            self.weather_data = requests.get(url + city + "&" + token).json()
        except requests.exceptions.RequestException as e:
            print("ERROR: connection to Open Weather API not working. ", e)

    def get_today_weather(self):

        self.temp_min = self.weather_data['list'][0]['main']['temp_min'] - 273.15
        self.temp_max = self.weather_data['list'][0]['main']['temp_max'] - 273.15
        self.humidity = self.weather_data['list'][0]['main']['humidity']
        self.temp_cur = self.weather_data['list'][0]['main']['temp'] - 273.15

        weather_icon = self.weather_data['list'][0]['weather'][0]['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(weather_icon))
        self.pixmap_cur_weather.loadFromData(icon._content)

        self.signal_weather.emit()

    def get_forecast(self):

        # find first day
        date, hour = self.weather_data['list'][0]['dt_txt'].split(' ')
        hour = int(hour[:2])
        first_day_offset = int((24 - hour) / 3)

        # forecast for 4 days at 12.00
        weather_1 = self.weather_data['list'][first_day_offset + 4]['weather'][0]
        weather_2 = self.weather_data['list'][first_day_offset + 4 + 8]['weather'][0]
        weather_3 = self.weather_data['list'][first_day_offset + 4 + 16]['weather'][0]
        weather_4 = self.weather_data['list'][first_day_offset + 4 + 24]['weather'][0]

        self.date_1, _ = self.weather_data['list'][first_day_offset + 4]['dt_txt'].split(' ')
        self.date_2, _ = self.weather_data['list'][first_day_offset + 4 + 8]['dt_txt'].split(' ')
        self.date_3, _ = self.weather_data['list'][first_day_offset + 4 + 16]['dt_txt'].split(' ')
        self.date_4, _ = self.weather_data['list'][first_day_offset + 4 + 24]['dt_txt'].split(' ')

        tmp = self.date_1.split('-')
        self.date_1 = tmp[2] + ' ' + tmp[1] + ' ' + tmp[0]

        tmp = self.date_2.split('-')
        self.date_2 = tmp[2] + ' ' + tmp[1] + ' ' + tmp[0]

        tmp = self.date_3.split('-')
        self.date_3 = tmp[2] + ' ' + tmp[1] + ' ' + tmp[0]

        tmp = self.date_4.split('-')
        self.date_4 = tmp[2] + ' ' + tmp[1] + ' ' + tmp[0]

        icon_name = weather_1['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))

        self.pixmap_day_1.loadFromData(icon._content)

        icon_name = weather_2['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))

        self.pixmap_day_2.loadFromData(icon._content)

        icon_name = weather_3['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        self.pixmap_day_3.loadFromData(icon._content)


        icon_name = weather_4['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        self.pixmap_day_4.loadFromData(icon._content)

        self.signal_forecast.emit()


