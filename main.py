from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5 import uic
import sys
from bme280_sensor import ThreadBME280
from date_time import ThreadDateTime
from weather_api import ThreadWeatherForecast
from arpae_api import ThreadArpae
from graphs import ThreadGraphs
from telegram import SenderTelegram
import mysql.connector as mariadb


class SecondWindow(QDialog):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        uic.loadUi("/home/pi/Documents/home_station/second.ui", self)

        self.type = None

        self.exit_button.clicked.connect(self.close)

    def set_type(self, type):
        self.type = type
        if type == 'temp':
            pixmap = QtGui.QPixmap('graphs/temp.png')
        elif type == 'humi':
            pixmap = QtGui.QPixmap('graphs/humi.png')
        elif type == 'press':
            pixmap = QtGui.QPixmap('graphs/pres.png')

        self.img_graph_temp.setScaledContents(True)
        self.img_graph_temp.setPixmap(pixmap)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        uic.loadUi("main.ui", self)

        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height())

        self.setGeometry(geometry)

        # settings ToDO: create file settings
        reload_seconds = 2#60
        reload_seconds_graphs = 1#300

        # database
        self.mariadb_connection_1 = mariadb.connect(user='homestation', password='hs', database='home_station')
        # self.mariadb_connection_2 = mariadb.connect(user='homestation', password='hs', database='home_station')
        self.cursor_1 = self.mariadb_connection_1.cursor(buffered=True)
        self.cursor_2 = self.mariadb_connection_1.cursor(buffered=True)

        l = [[], [], []]

        # threads
        self.sampling_thread = ThreadBME280(self, self.cursor_1, self.mariadb_connection_1, reload_seconds, l)
        self.graph_thread = ThreadGraphs(self, self.cursor_2, self.mariadb_connection_1, reload_seconds, reload_seconds_graphs, l)
        self.datetime_thread = ThreadDateTime(self, reload_seconds)
        self.weather_thread = ThreadWeatherForecast(self, city='Bagnacavallo', reload_seconds=10800)  # 10800: 3 hours in seconds
        self.arpae_thread = ThreadArpae(self, reload_seconds=3600)
        self.sender = SenderTelegram()

        # signals
        self.sampling_thread.signal_bme280.connect(self.update_temp_humi_pres)
        self.datetime_thread.signal_time.connect(self.update_time)
        self.graph_thread.signal_minmax.connect(self.update_minmax)
        self.arpae_thread.signal_arpae.connect(self.update_arpae)
        self.weather_thread.signal_weather.connect(self.update_weather)
        self.weather_thread.signal_forecast.connect(self.update_forecast)


        # starters
        self.sampling_thread.start()
        self.graph_thread.start()
        self.datetime_thread.start()
        self.weather_thread.start()
        self.arpae_thread.start()

        # buttons
        # self.button_start.clicked.connect(self.start_sampling)
        self.graph_temp_button.clicked.connect(lambda: self.on_pushButton_clicked('temp'))
        self.graph_humi_button.clicked.connect(lambda: self.on_pushButton_clicked('humi'))
        self.graph_press_button.clicked.connect(lambda: self.on_pushButton_clicked('press'))

        self.dialog = SecondWindow(self)

        # ToDo decidere come startare i thread
        # start threads

    def on_pushButton_clicked(self, type):
        self.dialog.set_type(type)
        self.dialog.show()

    def update_temp_humi_pres(self):
        if self.sampling_thread.humidity is not None:
            self.lcd_h.display("{:.1f}".format(self.sampling_thread.humidity))
        if self.sampling_thread.pressure is not None:
            self.lcd_p.display(self.sampling_thread.pressure)
        if self.sampling_thread.ambient_temperature is not None:
            self.lcd_t.display("{:.1f}".format(self.sampling_thread.ambient_temperature))

    def update_time(self):
        if self.datetime_thread.date is not None:
            self.data.setText(self.datetime_thread.date)
        if self.datetime_thread.hour is not None:
            self.ora.setText(self.datetime_thread.hour)

    def update_arpae(self):
        if self.arpae_thread.no2_value is not None:
            if self.arpae_thread.no2_value < 100:
                self.label_color_1.setStyleSheet("QLabel { background-color: green }")
            elif 101 < self.arpae_thread.no2_value < 199:
                self.label_color_1.setStyleSheet("QLabel { background-color: yellow }")
            elif 200 < self.arpae_thread.no2_value < 299:
                self.label_color_1.setStyleSheet("QLabel { background-color: orange }")
            elif 300 < self.arpae_thread.no2_value < 399:
                self.label_color_1.setStyleSheet("QLabel { background-color: red }")
            elif self.arpae_thread.no2_value > 400:
                self.label_color_1.setStyleSheet("QLabel { background-color: purple }")
        self.lcd_pm1.display(self.arpae_thread.no2_value)

        if self.arpae_thread.pm25_value is not None:
            if self.arpae_thread.pm25_value < 20:
                self.label_color_2.setStyleSheet("QLabel { background-color: green }")
            elif 20 < self.arpae_thread.pm25_value < 39:
                self.label_color_2.setStyleSheet("QLabel { background-color: yellow }")
            elif 40 < self.arpae_thread.pm25_value < 59:
                self.label_color_2.setStyleSheet("QLabel { background-color: orange }")
            elif 60 < self.arpae_thread.pm25_value < 79:
                self.label_color_2.setStyleSheet("QLabel { background-color: red }")
            elif self.arpae_thread.pm25_value > 80:
                self.label_color_2.setStyleSheet("QLabel { background-color: purple }")
            self.lcd_pm25.display(self.arpae_thread.pm25_value)

        if self.arpae_thread.pm10_value is not None:
            if self.arpae_thread.pm10_value < 25:
                self.label_color_3.setStyleSheet("QLabel { background-color: green }")
            if 26 < self.arpae_thread.pm10_value < 50:
                self.label_color_3.setStyleSheet("QLabel { background-color: yellow }")
            if 51 < self.arpae_thread.pm10_value < 75:
                self.label_color_3.setStyleSheet("QLabel { background-color: orange }")
            if 76 < self.arpae_thread.pm10_value < 100:
                self.label_color_3.setStyleSheet("QLabel { background-color: red }")
            if self.arpae_thread.pm10_value > 100:
                self.label_color_3.setStyleSheet("QLabel { background-color: purple }")
            self.lcd_pm10.display(self.arpae_thread.pm10_value)

    def update_weather(self):

        if self.weather_thread.city is not None:
            self.label_city.setText(self.weather_thread.city)

        if self.weather_thread.temp_min is not None:
            self.lcd_w_min.display("{:.1f}".format(self.weather_thread.temp_min))

        if self.weather_thread.temp_max is not None:
            self.lcd_w_max.display("{:.1f}".format(self.weather_thread.temp_max))

        if self.weather_thread.humidity is not None:
            self.lcd_w_hum.display("{:.1f}".format(self.weather_thread.humidity))

        if self.weather_thread.temp_cur is not None:
            self.lcd_w_tem.display("{:.1f}".format(self.weather_thread.temp_cur))

        if self.weather_thread.pixmap_cur_weather is not None:
            self.label_cur_weather.setPixmap(self.weather_thread.pixmap_cur_weather)

    def update_forecast(self):

        if self.weather_thread.date_1 is not None and self.weather_thread.pixmap_day_1 is not None:
            self.forecast_1.setPixmap(self.weather_thread.pixmap_day_1)
            self.label_day_forecast_1.setText(self.weather_thread.date_1)

        if self.weather_thread.date_2 is not None and self.weather_thread.pixmap_day_2 is not None:
            self.forecast_2.setPixmap(self.weather_thread.pixmap_day_2)
            self.label_day_forecast_2.setText(self.weather_thread.date_2)

        if self.weather_thread.date_3 is not None and self.weather_thread.pixmap_day_3 is not None:
            self.forecast_3.setPixmap(self.weather_thread.pixmap_day_3)
            self.label_day_forecast_3.setText(self.weather_thread.date_3)

        if self.weather_thread.date_4 is not None and self.weather_thread.pixmap_day_4 is not None:
            self.forecast_4.setPixmap(self.weather_thread.pixmap_day_4)
            self.label_day_forecast_4.setText(self.weather_thread.date_4)

        self.forecast_1.show()
        self.forecast_2.show()
        self.forecast_3.show()
        self.forecast_4.show()

    def update_minmax(self):
        if self.graph_thread.temp_min is not None:
            self.lcd_min_temp.display(self.graph_thread.temp_min)

        if self.graph_thread.temp_max is not None:
            self.lcd_max_temp.display(self.graph_thread.temp_max)

        if self.graph_thread.humi_min is not None:
            self.lcd_min_humi.display(self.graph_thread.humi_min)

        if self.graph_thread.humi_max is not None:
            self.lcd_max_humi.display(self.graph_thread.humi_max)

        if self.graph_thread.pixmap_pres is not None:
            self.arrow_press.setScaledContents(True)
            self.arrow_press.setPixmap(self.graph_thread.pixmap_pres)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # os.chdir("/home/pi/Documents/home_station/")

    main_window = MainWindow()
    # main_window.showFullScreen()
    # main_window.showMaximized()
    main_window.show()

    sys.exit(app.exec_())