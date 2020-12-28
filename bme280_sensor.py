import bme280
import smbus2
from time import sleep
from PyQt5 import QtCore, QtGui
from datetime import datetime
import numpy as np


class ThreadBME280(QtCore.QThread):

    signal_bme280 = QtCore.pyqtSignal()
    signal_minmax = QtCore.pyqtSignal()

    def __init__(self, window, config, l):

        QtCore.QThread.__init__(self)

        self.reload_seconds = config['RELOAD SECONDS']['TEMPERATURE']
        self.how_many_days = config['DATA COLLECTION']['HOW MANY DAYS']
        self.l = l

        self.ambient_temperature = None
        self.humidity = None
        self.pressure = None

        self.temp_min = 1000
        self.temp_max = 0
        self.humi_min = 10000
        self.humi_max = 0

    def __del__(self):
        self.wait()

    def run(self):
        self.sample_data_bme280()

    def sample_data_bme280(self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)

        try:
            bme280.load_calibration_params(bus, address)
        except Exception as e:
            print("Error on BME280 sensor. Is it connected?")
            return

        while True:

            try:
                bme280_data = bme280.sample(bus, address)
                self.humidity = bme280_data.humidity
                self.pressure = bme280_data.pressure
                self.ambient_temperature = bme280_data.temperature
                timestamp = datetime.now().strftime('%d/%m %H:%M')

                self.l[0].append(self.ambient_temperature)
                self.l[1].append(self.humidity)
                self.l[2].append(self.pressure)
                self.l[3].append(timestamp)

                if len(self.l[0]) > 0:
                    array_temp = np.array(self.l[0])
                    if np.min(array_temp) < self.temp_min:
                        self.temp_min = np.min(array_temp)
                    if np.max(array_temp) > self.temp_max:
                        self.temp_max = np.max(array_temp)

                if len(self.l[1]) > 0:
                    array_humi = np.array(self.l[1])
                    if np.min(array_humi) < self.humi_min:
                        self.humi_min = np.min(array_humi)
                    if np.max(array_humi) > self.humi_max:
                        self.humi_max = np.max(array_humi)

                if len(self.l[2]) > 0:
                    array_pres = np.array(self.l[2])
                    index_min_press = np.argmin(array_pres)
                    index_max_press = np.argmax(array_pres)
                else:
                    index_min_press = 0
                    index_max_press = 0

                if index_max_press > index_min_press:
                    self.pixmap_pres = QtGui.QPixmap('./icons/arrow_up.png')
                    # self.window.arrow_press.setScaledContents(True)
                    # self.window.arrow_press.setPixmap(pixmap)
                else:
                    self.pixmap_pres = QtGui.QPixmap('./icons/arrow_down.png')
                    # self.window.arrow_press.setScaledContents(True)
                    # self.window.arrow_press.setPixmap(pixmap)

                how_many_days = self.how_many_days
                max_samples = ((60 * 60 * 24) / self.reload_seconds) * how_many_days

                how_many_days_press = 0.5
                max_samples_press = ((60 * 60 * 24) / self.reload_seconds) * how_many_days_press

                while len(self.l[0]) > max_samples:
                    self.l[0].pop(0)
                while len(self.l[1]) > max_samples:
                    self.l[1].pop(0)
                while len(self.l[2]) > max_samples_press:
                    self.l[2].pop(0)

                self.signal_minmax.emit()

                self.signal_bme280.emit()

                sleep(self.reload_seconds)

            except:
                print("Error on BME280 sensor")
