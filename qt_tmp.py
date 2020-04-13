from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import uic, QtCore
import sys
from bme280_test import sample_data_bme280

# Ui_MainWindow, QtBaseClass = uic.loadUiType("untitled.ui")


class ThreadAnalysis(QtCore.QThread):

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def __del__(self):
        self.wait()

    def run(self):
        sample_data_bme280(self.window)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)

        # threads
        self.sampling_thread = ThreadAnalysis(self)

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