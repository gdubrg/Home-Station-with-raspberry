from datetime import datetime
from PyQt5 import QtCore
from time import sleep
import time


class ThreadDateTime(QtCore.QThread):

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
            t = time.time()
            date = datetime.now().strftime('%A %d %B %Y')
            hour = datetime.today().strftime('%H:%M:%S')
            self.window.data.setText(date)
            self.window.ora.setText(hour)
            sleep(1 - (time.time()-t))


if __name__ == "__main__":
    pass