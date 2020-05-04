from PyQt5 import QtCore, QtGui
from time import sleep
import requests


class ThreadArpae(QtCore.QThread):

    signal_arpae = QtCore.pyqtSignal()

    def __init__(self, window, reload_seconds):
        QtCore.QThread.__init__(self)
        # self.window = window
        self.reload_seconds = reload_seconds

        self.pm10_value = None
        self.pm25_value = None
        self.no2_value = None

    def __del__(self):
        self.wait()

    def run(self):
        self.air_quality()

    def air_quality(self):
        while True:

            pm10, pm25, no2 = None, None, None
            pm10_value, pm25_value, no2_value = 0, 0, 0

            try:
                pm10 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                          'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                          'WHERE station_id=4000022 '
                                          'AND variable_id=5'
                                          'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if pm10 is not None:
                self.pm10_value = pm10['result']['records'][0]['value']

            try:
                pm25 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                    'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                    'WHERE station_id=4000022 '
                                    'AND variable_id=111'
                                    'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if pm25 is not None:
                self.pm25_value = pm25['result']['records'][0]['value']

            try:
                no2 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                    'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                    'WHERE station_id=4000022 '
                                    'AND variable_id=8'
                                    'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if no2 is not None:
                self.no2_value = no2['result']['records'][0]['value']

            # wait for results
            sleep(3)

            # if no2_value < 100:
            #     self.window.label_color_1.setStyleSheet("QLabel { background-color: green }")
            # if 101 < no2_value < 199:
            #     self.window.label_color_1.setStyleSheet("QLabel { background-color: yellow }")
            # if 200 < no2_value < 299:
            #     self.window.label_color_1.setStyleSheet("QLabel { background-color: orange }")
            # if 300 < no2_value < 399:
            #     self.window.label_color_1.setStyleSheet("QLabel { background-color: red }")
            # if no2_value > 400:
            #     self.window.label_color_1.setStyleSheet("QLabel { background-color: purple }")
            #
            # self.window.lcd_pm1.display(no2_value)
            #
            # if pm25_value < 20:
            #     self.window.label_color_2.setStyleSheet("QLabel { background-color: green }")
            # if 20 < pm25_value < 39:
            #     self.window.label_color_2.setStyleSheet("QLabel { background-color: yellow }")
            # if 40 < pm25_value < 59:
            #     self.window.label_color_2.setStyleSheet("QLabel { background-color: orange }")
            # if 60 < pm25_value < 79:
            #     self.window.label_color_2.setStyleSheet("QLabel { background-color: red }")
            # if pm25_value > 80:
            #     self.window.label_color_2.setStyleSheet("QLabel { background-color: purple }")
            #
            # self.window.lcd_pm25.display(pm25_value)
            #
            # if pm10_value < 25:
            #     self.window.label_color_3.setStyleSheet("QLabel { background-color: green }")
            # if 26 < pm10_value < 50:
            #     self.window.label_color_3.setStyleSheet("QLabel { background-color: yellow }")
            # if 51 < pm10_value < 75:
            #     self.window.label_color_3.setStyleSheet("QLabel { background-color: orange }")
            # if 76 < pm10_value < 100:
            #     self.window.label_color_3.setStyleSheet("QLabel { background-color: red }")
            # if pm10_value > 100:
            #     self.window.label_color_3.setStyleSheet("QLabel { background-color: purple }")
            #
            # self.window.lcd_pm10.display(pm10_value)

            self.signal_arpae.emit()

            sleep(self.reload_seconds)


if __name__ == "__main__":
    pass