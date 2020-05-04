from datetime import datetime
from PyQt5 import QtCore
from time import sleep
import time


class ThreadDateTime(QtCore.QThread):

    signal_time = QtCore.pyqtSignal()

    def __init__(self, window, reload_seconds):
        QtCore.QThread.__init__(self)
        # self.window = window
        self.reload_seconds = reload_seconds

        self.date = None
        self.hour = None

    def __del__(self):
        self.wait()

    def run(self):
        self.get_date_and_time()

    def get_date_and_time(self):
        while True:
            t = time.time()
            self.date = datetime.now().strftime('%A %d %B %Y')
            self.hour = datetime.today().strftime('%H:%M:%S')

            # self.window.data.setText(date)
            # self.window.ora.setText(hour)

            self.signal_time.emit()
            sleep(1 - (time.time()-t))


if __name__ == "__main__":
    pass
