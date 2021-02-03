from PyQt5 import QtCore
from time import sleep
import time
from datetime import datetime
import cv2
from os.path import join, basename
import os
import requests
# from tqdm import tqdm


class ThreadCamera(QtCore.QThread):

    def __init__(self, window, config):
        QtCore.QThread.__init__(self)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        self.fph = config['CAMERA']['FPH']
        self.face_detection = config['CAMERA']['FACE DETECTION']
        self.motion_detection = config['CAMERA']['MOTION DETECTION']

        self.output_path = 'acquisitions'
        self.output_path_faces = join(self.output_path, 'faces')

        self.how_many_seconds = int(3600 / self.fph)

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if not os.path.exists('data'):
            os.makedirs('data')

        if self.face_detection:
            if not os.path.exists(self.output_path_faces):
                os.makedirs(self.output_path_faces)

        if self.face_detection:
            xml_url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
            if not os.path.isfile(join(os.getcwd(), 'data', basename(xml_url))):
                print("Downloading Face Detector module...")
                download = requests.get(xml_url)
                with open(join(os.getcwd(), 'data', basename(xml_url)), 'wb') as f:
                    f.write(download.content)

            self.face_detector = cv2.CascadeClassifier(join(os.getcwd(), 'data', basename(xml_url)))

    def __del__(self):
        self.wait()

    def run(self):
        self.get_frame()

    def get_frame(self):

        while True:
            t = time.time()

            ret, frame = self.cap.read()

            if ret:
                timestamp = datetime.now().strftime('%d%m_%H%M%S')

                # cv2.imwrite(join(self.output_path, timestamp + '.jpg'), frame)

                if self.face_detection:

                    faces = self.face_detector.detectMultiScale(frame, 1.1, 4)
                    for (x, y, w, h) in faces:
                        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        face = frame[y:y + h, x:x + w]
                        cv2.imwrite(join(self.output_path_faces, timestamp + '.jpg'), face)

                cv2.imwrite(join(self.output_path, timestamp + '.jpg'), frame)

                if self.motion_detection:
                    pass

            time_to_wait = self.how_many_seconds - (time.time()-t)
            if time_to_wait > 0:
                sleep(time_to_wait)


if __name__ == "__main__":
    import yaml

    # settings
    print("Loading config file: {}".format('settings'))
    with open('settings', 'rt') as fd:
        config = yaml.load(fd, Loader=yaml.SafeLoader)

    th = ThreadCamera(None, config)

    th.get_frame()

