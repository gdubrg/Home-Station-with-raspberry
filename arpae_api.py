from PyQt5 import QtCore
from time import sleep
import requests


class ThreadArpae(QtCore.QThread):

    def __init__(self, window, reload_seconds):
        QtCore.QThread.__init__(self)
        self.window = window
        self.reload_seconds = reload_seconds

    def __del__(self):
        self.wait()

    def run(self):
        self.get_date_and_time()

    def get_date_and_time(self):
        while True:
            pm10 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                      'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                      'WHERE station_id=4000022 '
                                      'AND variable_id=5'
                                      'ORDER BY reftime DESC LIMIT 1').json()

            pm10_value = pm10['result']['records'][0]['value']

            pm25 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                'WHERE station_id=4000022 '
                                'AND variable_id=111'
                                'ORDER BY reftime DESC LIMIT 1').json()

            pm25_value = pm25['result']['records'][0]['value']

            no2 = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql='
                                'SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                                'WHERE station_id=4000022 '
                                'AND variable_id=8'
                                'ORDER BY reftime DESC LIMIT 1').json()

            pm1_value = no2['result']['records'][0]['value']

            self.window.lcd_pm1.display(pm1_value)
            self.window.lcd_pm25.display(pm25_value)
            self.window.lcd_pm10.display(pm10_value)

            sleep(self.reload_seconds)


if __name__ == "__main__":
    pass