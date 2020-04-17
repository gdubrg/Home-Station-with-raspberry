import bme280
import smbus2
import cv2
from time import sleep
import numpy as np
import time


def sample_data_bme280(window, cursor, connection):
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
        window.lcd_p.display(pressure)
        window.lcd_t.display(ambient_temperature)

        date_now = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO BME_280 VALUES (%s, %s, %s, %s)", (ambient_temperature, pressure, humidity, date_now))
        connection.commit()

        sleep(2)