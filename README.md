# Home Monitoring Station with Raspberry

## Project
This is a Home Station based on the Raspberry board able to check the following values:
* Temperature (C°)
* Humidity (%)
* Pression (hPa)
* Air Quality (NO2, PM 2.5 and 10)
* Current Weather
* Weather Forecast

### Graphical User Interface
A easy-to-read Graphical User Interface has been developed using the Qt Libraries. 
This GUI is displayed in a touch screen monitor connected to the Raspberry board and it is the following:

<p align="center">
  <img src="/images/vers4_1.PNG" />
</p>

The GUI is divided into 3 different columns:
1. **Environment Data**: in the first column on the left, the current temperature, humidity and pressure 
are reported. These data are collected by the BME280 sensor. Min and max values are also reported, 
a button 'graphs' allows to check the temporal summary of collected data.

<p float="center">
  <img src="/images/temp.PNG" width="33%" />
  <img src="/images/humi.PNG" width="33%" /> 
  <img src="/images/press.PNG" width="33%" />
</p>

2. **Air Quality**: values about the NO2 (*Nitrogen dioxide*), PM2.5 and PM 10 are reported. Data are collected
through the Arpae (*Agenzia regionale prevenzione, ambiente ed energia dell'Emilia-Romagna*) website.
3. **Weather and Forecast**: the current weather (in terms of temperature and its min and max values) and weather 
forecast about the next 4 days are reported. These data are collected through the service of *OpenWeather API* (free version).

On the top of the GUI, the current date and the current time are reported.
This GUI is designed and optimized for a 800x480 touch screen (5'').

### Settings
From the `settings` file you can change the following items:
* Modules
* Reload seconds
* 

## How To
If you plan to launch this script on your Raspberry board, check the following documentation for the software and hardware
components.

### Software Requirements
Please, install all the requirements listed in the `requirements.txt` file.
* Python 3
* Numpy
*

## Hardware Requirements
The project is tested with the following components:
* Raspberry Pi 4 (4 GB RAM version)
* Adafruit 5'' (800x480) touch screen, PWM-able backlight
* BME280 sensor

## Web-related Requirements

### Launch the script 
Once cloned this repository, open a terminal in the project folder and type: `python3 main.py`.
If you have python installed in a virtual environment, launch the script accordingly.


## Technical Details
If you do not live in Italy, and specifically in Emilia Romagna, the Arpae service is useless.
Despite this, this project can be an interesting starting point to develop your own Home Monitoring Station.
Then, technical details are provided.

### Code Structure

### Execution
