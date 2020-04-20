import bme280
import smbus2
import cv2
from time import sleep
from PyQt5 import QtCore
import time


class ThreadBME280(QtCore.QThread):

    s_temp_chart = QtCore.pyqtSignal(list, list)
    s_pres_chart = QtCore.pyqtSignal(list, list)
    s_humi_chart = QtCore.pyqtSignal(list, list)

    def __init__(self, window, cursor, connection, reload_seconds, parent=None):

        QtCore.QThread.__init__(self)
        self.window = window
        self.cursor = cursor
        self.connection = connection
        self.reload_seconds = reload_seconds

    def __del__(self):
        self.wait()

    def run(self):
        self.sample_data_bme280()

    def sample_data_bme280(self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)

        bme280.load_calibration_params(bus, address)

        while True:
            bme280_data = bme280.sample(bus, address)
            humidity = bme280_data.humidity
            pressure = bme280_data.pressure
            ambient_temperature = bme280_data.temperature

            print("H: {} P: {} T: {}".format(humidity, pressure, ambient_temperature))

            self.window.lcd_h.display("{:.1f}".format(humidity))
            self.window.lcd_p.display(pressure)
            self.window.lcd_t.display("{:.1f}".format(ambient_temperature))

            date_now = time.strftime('%Y-%m-%d %H:%M:%S')
            # self.cursor.execute("INSERT INTO BME_280 VALUES (%s, %s, %s, %s)", (ambient_temperature, pressure, humidity, date_now))
            # self.connection.commit()

            self.s_temp_chart.emit([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 2, 8, 4, 9, 5, 4, 3])
            self.s_pres_chart.emit([1, 2, 3], [1, 2, 3])
            self.s_humi_chart.emit([1, 2, 3], [1, 2, 3])

            sleep(self.reload_seconds)