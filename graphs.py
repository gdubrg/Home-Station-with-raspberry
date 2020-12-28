from PyQt5 import QtCore, QtGui
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


class ThreadGraphs(QtCore.QThread):

    signal_minmax = QtCore.pyqtSignal()

    def __init__(self, window, config, l):
        QtCore.QThread.__init__(self)

        self.reload_seconds = config['RELOAD SECONDS']['GRAPHS']
        self.reload_seconds_sampling = config['RELOAD SECONDS']['TEMPERATURE']

        self.l = l

        self.temp_min = 1000
        self.temp_max = 0
        self.humi_min = 10000
        self.humi_max = 0
        self.pixmap_pres = None

    def __del__(self):
        self.wait()

    def run(self):
        self.create_graphs()

    def create_graphs(self):

        while True:

            try:

                if len(self.l[0]) > 5:
                    step = int(len(self.l[0])/5)
                else:
                    step = 1

                p = self.l[3][::step]
                p = [label.replace(' ', '\n') for label in p]

                # temperature
                plt.plot(self.l[0])
                plt.box(False)
                plt.grid()

                plt.xticks(np.arange(0, len(self.l[0]), step), p)
                plt.yticks(np.arange(10, 30, 1))

                plt.savefig("graphs/temp.png", bbox_inches='tight')

                plt.cla()
                plt.clf()
                plt.close()

                ###
                # humidity

                plt.plot(self.l[1])
                plt.box(False)
                plt.grid()

                # p = self.l[3][::step]
                # p = [label.replace(' ', '\n') for label in p]
                plt.xticks(np.arange(0, len(self.l[1]), step), p)

                plt.savefig("graphs/humi.png", bbox_inches='tight')
                plt.cla()
                plt.clf()
                plt.close()

                ###
                # pressure

                plt.plot(self.l[2])
                plt.box(False)
                plt.grid()

                plt.xticks(np.arange(0, len(self.l[2]), step), p)

                plt.savefig("graphs/pres.png", bbox_inches='tight')
                plt.cla()
                plt.clf()
                plt.close()

            except Exception as e:
                print("Error in plotting values: ", e)

            sleep(self.reload_seconds)


if __name__ == "__main__":
    pass