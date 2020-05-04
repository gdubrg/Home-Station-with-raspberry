from PyQt5 import QtCore, QtGui
from time import sleep
import requests


class ThreadWeatherForecast(QtCore.QThread):

    signal_weather = QtCore.pyqtSignal()
    signal_forecast = QtCore.pyqtSignal()

    def __init__(self, window, city, reload_seconds):
        QtCore.QThread.__init__(self)
        self.window = window
        self.city = city
        self.reload_seconds = reload_seconds

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
            # self.window.label_city.setText(self.city)
            self.do_request()
            if self.weather_data is not None:
                self.get_today_weather()
                self.get_forecast()
            sleep(self.reload_seconds)

    def do_request(self):
        url = "https://api.openweathermap.org/data/2.5/forecast?"
        city = "q=" + self.city
        token = "appid=6de6d5f7dc205d00ce676ee7a2f2274a"
        try:
            self.weather_data = requests.get(url + city + "&" + token).json()
        except requests.exceptions.RequestException as e:
            print("ERROR: connection to Open Weather API not working. ", e)

    def get_today_weather(self):

        self.temp_min = self.weather_data['list'][0]['main']['temp_min'] - 273.15
        self.temp_max = self.weather_data['list'][0]['main']['temp_max'] - 273.15
        self.humidity = self.weather_data['list'][0]['main']['humidity']
        self.temp_cur = self.weather_data['list'][0]['main']['temp'] - 273.15

        # self.window.lcd_w_min.display("{:.1f}".format(temp_min))
        # self.window.lcd_w_max.display("{:.1f}".format(temp_max))
        # self.window.lcd_w_hum.display("{:.1f}".format(humidity))
        # self.window.lcd_w_tem.display("{:.1f}".format(temp))

        weather_icon = self.weather_data['list'][0]['weather'][0]['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(weather_icon))
        # self.pixmap_cur_weather = QtGui.QPixmap()
        self.pixmap_cur_weather.loadFromData(icon._content)
        # self.window.label_cur_weather.setPixmap(pixmap)

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

        icon_name = weather_1['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        # pixmap = QtGui.QPixmap()

        self.pixmap_day_1.loadFromData(icon._content)

        # self.window.forecast_1.setPixmap(pixmap)
        # self.window.label_day_forecast_1.setText(date_1)

        icon_name = weather_2['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        # pixmap = QtGui.QPixmap()

        self.pixmap_day_2.loadFromData(icon._content)
        # self.window.forecast_2.setPixmap(pixmap)
        # self.window.label_day_forecast_2.setText(date_2)

        icon_name = weather_3['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        # pixmap = QtGui.QPixmap()
        self.pixmap_day_3.loadFromData(icon._content)
        # self.window.forecast_3.setPixmap(pixmap)
        # self.window.label_day_forecast_3.setText(date_3)

        icon_name = weather_4['icon']
        icon = requests.get('http://openweathermap.org/img/w/{}.png'.format(icon_name))
        # pixmap = QtGui.QPixmap()
        self.pixmap_day_4.loadFromData(icon._content)
        # self.window.forecast_4.setPixmap(pixmap)
        # self.window.label_day_forecast_4.setText(date_4)

        # self.window.forecast_1.show()
        # self.window.forecast_2.show()
        # self.window.forecast_3.show()
        # self.window.forecast_4.show()

        self.signal_forecast.emit()


