import bme280
import smbus2
from time import sleep
from PyQt5 import QtCore
import time
from datetime import timedelta
from datetime import datetime


class ThreadBME280(QtCore.QThread):

    signal_bme280 = QtCore.pyqtSignal()

    def __init__(self, window, cursor, connection, reload_seconds):

        QtCore.QThread.__init__(self)
        # self.window = window
        self.cursor = cursor
        self.connection = connection
        self.reload_seconds = reload_seconds

        self.ambient_temperature = None
        self.humidity = None
        self.pressure = None

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
            self.humidity = bme280_data.humidity
            self.pressure = bme280_data.pressure
            self.ambient_temperature = bme280_data.temperature

            # print("H: {} P: {} T: {}".format(humidity, pressure, ambient_temperature))

            # self.window.lcd_h.display("{:.1f}".format(self.humidity))
            # self.window.lcd_p.display(self.pressure)
            # self.window.lcd_t.display("{:.1f}".format(self.ambient_temperature))

            # date_now = time.strftime('%Y-%m-%d-%H-%M-%S')
            # for i in range(3):
            date_now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')

            try:
                self.cursor.execute("INSERT INTO BME_280 VALUES (%s, %s, %s, %s)", (self.ambient_temperature, self.pressure, self.humidity, date_now))
                self.connection.commit()
            except Exception as e:
                print("ERROR: problem in inserting values in database", e)

            self.signal_bme280.emit()

            sleep(self.reload_seconds)
