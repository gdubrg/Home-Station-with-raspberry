from PyQt5 import QtCore, QtGui
from time import sleep
import requests


class ThreadArpae(QtCore.QThread):

    signal_arpae = QtCore.pyqtSignal()

    def __init__(self, window, config):
        QtCore.QThread.__init__(self)

        self.reload_seconds = config['RELOAD SECONDS']['ARPAE']
        self.station_id = str(config['ARPAE']['STATION ID'])

        self.url_arpae = "https://dati.arpae.it/api/action/datastore_search_sql"

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
                pm10 = requests.get(self.url_arpae + '?sql='
                                          'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                          'WHERE station_id=' + self.station_id + ' '
                                          'AND variable_id=5'
                                          'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if pm10 is not None:
                self.pm10_value = pm10['result']['records'][0]['value']

            try:
                pm25 = requests.get(self.url_arpae + '?sql='
                                    'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                    'WHERE station_id=' + self.station_id + ' '
                                    'AND variable_id=111'
                                    'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if pm25 is not None:
                self.pm25_value = pm25['result']['records'][0]['value']

            try:
                no2 = requests.get(self.url_arpae + '?sql='
                                    'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                    'WHERE station_id=' + self.station_id + ' '
                                    'AND variable_id=8'
                                    'ORDER BY reftime DESC LIMIT 1').json()
            except requests.exceptions.RequestException as e:
                print("ERROR: connection to ARPAE API not working. ", e)

            if no2 is not None:
                self.no2_value = no2['result']['records'][0]['value']

            # wait for results
            sleep(3)

            self.signal_arpae.emit()

            sleep(self.reload_seconds)


if __name__ == "__main__":
    pass