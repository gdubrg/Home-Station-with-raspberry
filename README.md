# Home Monitoring Station with Raspberry

## Project
This is a **Home Monitoring Station** based on the *Raspberry Pi* 
board designed to collect and display the following values:
* **Temperature** (C°)
* **Humidity** (%)
* **Pressure** (hPa)
* **Air Quality** (NO2, PM 2.5 and 10)
* **Current Weather** (min, max and current temperature and humidity)
* **Weather Forecast** (4 days)

### Graphical User Interface
The user interface is designed to be displayed in a 5'' touch screen monitor connected to the 
*Raspberry* board. An example of the interface is the following:

<p align="center">
  <img src="/images/vers4_1.PNG" width="85%" />
</p>

As shown, the GUI is divided into 3 different columns:
1. **Environment Data**: in the first column on the left, the current temperature, humidity and pressure 
are reported. These data are collected by a real sensor (the *BME280* or equivalent) directly connected to the board. 
Min and max values are also reported, a button 'graphs' allows to check the temporal summary of collected data:

<p align="center">
  <img src="/images/temp.PNG" width="32%" />
  <img src="/images/humi.PNG" width="32%" /> 
  <img src="/images/press.PNG" width="32%" />
</p>

2. **Air Quality**: values about the NO2 (*Nitrogen dioxide*), PM (*Particulate Matter*) 2.5 and 10 are reported. 
Data are collected through the Arpae (*Agenzia regionale prevenzione, ambiente ed energia dell'Emilia-Romagna*) website, 
and then are valid only for the aforementioned italian region. The colored rectangle on the side of each value indicates
the level of quality (green: *ok*, yellow: *acceptable*, orange: *medium*, red: *bad*, purple: *harmful*)
3. **Weather and Forecast**: the current weather (in terms of temperature, its min and max values and 
humidity) and weather forecast about the next 4 days are reported. These data are collected through 
the *OpenWeather API* (free version).
Since this service is global, weather and forecast can be used worldwide.

On the top of the GUI, the current date and the current time are reported.

This GUI is designed and optimized for a 5'' 800x480 touch screen (further details are reported in the 
(Hardware Requirements)[###-hardware-requirements] section).

### Remote Visualization
Thanks to the [Telegram](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=it&gl=US) app, you can get
the graphs about the current temperature, humidity and pressure, just sending a message to the bot with the following 
texts: 'temp', 'humi' or 'pres'.

<p align="center">
  <img src="/images/telebot.PNG" />
</p>

## How To
If you plan to launch this script on your *Raspberry* board, check the following documentation both 
for the software and hardware requirements.

### Hardware Requirements
The project is tested with the following components:
* **Raspberry Pi 4** (4 GB RAM version). However, the computational load is very low (about 3% of 
CPU usage and less than 300MB of RAM), then I suppose you can run the script even with an older version
of the board.
* **Adafruit 5''** (800x480) touch screen, PWM-able backlight. [Here](https://www.adafruit.com/product/2260)
the link to the product. Note that you can use any screen also with different resolutions, maybe you can 
experience some graphical errors.
* **BME280 sensor**: the [sensor](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/)
 used to collect environmental data.
 
### Software Requirements
Run the program with **Python 3**. 
Please, install all the packages required listed in the `requirements.txt` file.
Remember to activate the **I2C** interface of the Raspberry board.

### Web-related Requirements
Air quality and weather data are collected through web-based API.
Then, you have to obtain the secret token from [OpenWeatherMap API](https://openweathermap.org/) (create a free
account). To remote control the app, you need to activate a Telegram bot.

### Launch the script 
Once cloned this repository, open a terminal in the project folder and type: `python3 main.py`.
If you have python installed in a virtual environment, launch the script accordingly.

You can use the file `launcher.sh` to automatically launch the script every time you turn on the *Raspberry Pi* board.
There are several ways to do that.
I have used this solution:
1. Navigate into the `~/.config/autostart` directory, then create a new `*.desktop` file with the 
following lines:
```
[Desktop Entry]
Type=Application
Terminal=true
Name=home_station
Exec=<absolute_path_to_your_script>/launcher.sh
```
Note that I have added a sleep function (10 seconds) to wait the WiFi card turns on.

### Settings
From the `settings` file you can change the following items:
* **MODULES**: decide which module is activated or not.
    * BME280: collection of temperature, humidity and pressure data from the BME280 sensor.
    * OPENWEATHER: get current weather and weather forecast data from the *OpenWeatherMap* API.
    * ARPAE: get air quality data from Arpae API.
    * TELEGRAM: telegram bot for the remote visualization of the temperature, humidity and pressure graphs.

* **RELOAD SECONDS**: it is possible to set how many times (in seconds) sampling data.
    * TEMPERATURE: seconds to get data from the BME280 sensor.
    * WEATHER: seconds to get data from *OpenWeatherMap API*. The free account provides new data every 3 hours (10800 seconds, 
    that is the default value).
    * ARPAE: seconds to get data from *Arpae API*. Here, data are updated every 1 hour (3600 seconds, that is the default 
    value).
    * GRAPHS: seconds to create new graphs to be displayed. This value may be equal or greater than the TEMPERATURE reload 
    seconds.
* **ARPAE**: here you can change the value for the Arpae API.
     STATION ID: id of the air quality station that you want to use. [Here](https://dati.arpae.it/dataset/qualita-dell-aria-rete-di-monitoraggio/resource/21a9464d-c91a-4f17-b5c7-f3ee7560ff7e)
     you can find the list of available monitoring stations. Note that each station provides different data.
* **WEATHER**: settings about the data samples from [OpenWeatherMap API](https://openweathermap.org/)
    * CITY: place of the weather data.
    * TOKEN: this is the secret token for your account. You have to sign in the [website](https://openweathermap.org/) to get this token.
* **TELEGRAM**:
    * TOKEN: this is the secret token of your Telegram bot
    * CHAT ID: the id of your chat, in this way you can select users that are able to get data from the home station.
* **DATA COLLECTION**: settings about the buffer to store the collected values.
    * HOW MANY DAYS: put how many days you would like to store data from the BME280 sensor.
    

## Technical Details
If you do not live in Italy, and specifically in Emilia Romagna, the Arpae service is useless.
Despite this, this project can be an interesting starting point to develop your **own** Home Monitoring Station.
Then, technical details are provided.

### Code Structure
The entry point of the code is the file `main-py`.
The GUI is developed using the *Qt Libraries*.

### Execution
Several threads are started and run in parallel to collect data from the sensor, the websites and so on.
Despite this, the CPU usage is low (only 3%) on the quad-core *Cortex-A72 (ARM v8) 64-bit SoC @1.5GHz* of the Raspberry Pi 4.
Also the RAM usage is low, since less than 300MB are required. 

### Issues
* Telegram bot: I have noticed that the Telegram bot is not completely reliable, since the method `MessageLoop` sometimes gives 
timeout errors that cannot be handled by the `try-except` python operations.
Then, if you want an high reliability of the system, please deactivate this module.
* Database: you can easily note that no databases are included in the project. The use of threads and databases on Raspberry is not
so reliable (many random errors with database cursors), then I implemented the project without the use of database. 
After all, this is just a monitoring station and not a complete weather station to collect data during a long time interval. 
