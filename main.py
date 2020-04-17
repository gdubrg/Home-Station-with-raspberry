from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import uic, QtCore
import sys
from bme280_sensor import sample_data_bme280
import mysql.connector as mariadb
import time


# Ui_MainWindow, QtBaseClass = uic.loadUiType("untitled.ui")


class ThreadAnalysis(QtCore.QThread):

    def __init__(self, window, cursor, connection):
        QtCore.QThread.__init__(self)
        self.window = window
        self.cursor = cursor
        self.connection = connection

    def __del__(self):
        self.wait()

    def run(self):
        sample_data_bme280(self.window, self.cursor, self.connection)


class MainWindow(QMainWindow):
    def __init__ (self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)

        # database
        self.mariadb_connection = mariadb.connect(user='pi', password='dardinello', database='home_station')
        self.cursor = self.mariadb_connection.cursor()

        # self.cursor.execute("SELECT * FROM BME_280")
        # records = self.cursor.fetchall()
        # for r in records:
        #     print(r)

        # threads
        self.sampling_thread = ThreadAnalysis(self, self.cursor, self.mariadb_connection)

        # buttons
        self.button_start.clicked.connect(self.start_sampling)

    def start_sampling(self):
        self.sampling_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    # main_window.showFullScreen()
    # main_window.showMaximized()
    main_window.show()

    sys.exit(app.exec_())