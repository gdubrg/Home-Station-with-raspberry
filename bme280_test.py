import bme280
import smbus2
import cv2
from time import sleep
import numpy as np


def sample_data_bme280(window):
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    bme280.load_calibration_params(bus, address)

    while True:
        bme280_data = bme280.sample(bus, address)
        humidity = bme280_data.humidity
        pressure = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        print("H: {} P: {} T: {}".format(humidity, pressure, ambient_temperature))
        window.lcd_h.display(humidity)
        sleep(1)