from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import sys
from bme280_sensor import ThreadBME280
from date_time import ThreadDateTime
from weather_api import ThreadWeatherForecast
from arpae_api import ThreadArpae
import mysql.connector as mariadb


class MainWindow(QMainWindow):

    def __init__ (self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        uic.loadUi("main.ui", self)

        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height())

        self.setGeometry(geometry)

        # settings ToDO: create file settings
        reload_seconds = 60

        # database
        self.mariadb_connection = mariadb.connect(user='homestation', password='hs', database='home_station')
        self.cursor = self.mariadb_connection.cursor()

        # self.cursor.execute("SELECT * FROM BME_280")
        # records = self.cursor.fetchall()
        # for r in records:
        #     print(r)

        self.initialize_gui()

        # threads
        self.sampling_thread = ThreadBME280(self, self.cursor, self.mariadb_connection, reload_seconds)
        self.datetime_thread = ThreadDateTime(self, reload_seconds)
        self.weather_thread = ThreadWeatherForecast(self, city='Modena', reload_seconds=10800)  # 10800: 3 hours in seconds
        self.arpae_thread = ThreadArpae(self, reload_seconds=3600)

        # signals
        self.sampling_thread.s_temp_chart.connect(lambda x, y: self.update_charts(x, y))
        # self.sampling_thread.s_pres_chart.connect(lambda x, y: self.update_charts(x, y))
        # self.sampling_thread.s_humi_chart.connect(lambda x, y: self.update_charts(x, y))

        # starters
        self.sampling_thread.start()
        self.datetime_thread.start()
        self.weather_thread.start()
        self.arpae_thread.start()

        # buttons
        # self.button_start.clicked.connect(self.start_sampling)

        # ToDo decidere come startare i thread
        # start threads

    def initialize_gui(self):

        # charts temperature, pressure and humidity
        self.temp_chart.setBackground('w')
        self.temp_chart.hideAxis('bottom')
        self.temp_chart.hideAxis('left')

        self.pres_chart.setBackground('w')
        self.pres_chart.hideAxis('bottom')
        self.pres_chart.hideAxis('left')

        self.humi_chart.setBackground('w')
        self.humi_chart.hideAxis('bottom')
        self.humi_chart.hideAxis('left')

    def start_sampling(self):
        self.sampling_thread.start()

    def update_charts(self, x, y):
        # self.temp_chart.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [30, 32, 34, 32, 33, 31, 29, 32, 35, 45])
        self.temp_chart.plot(x, y)
        self.pres_chart.plot(x, y)
        self.humi_chart.plot(x, y)
        # print(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    # main_window.showFullScreen()
    # main_window.showMaximized()
    main_window.show()

    sys.exit(app.exec_())