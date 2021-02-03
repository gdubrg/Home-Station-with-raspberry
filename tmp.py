# import requests
# import calendar
#
# api_key = '6de6d5f7dc205d00ce676ee7a2f2274a'
# api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
#
# running = True
#
# print('Welcome to Jaimes Subroto\'s 5 day weather forecast application using OpenWeatherMap\'s API!')
#
# # "https://api.openweathermap.org/data/2.5/forecast?q=modena&appid=6de6d5f7dc205d00ce676ee7a2f2274a"
#
#
# json_data = requests.get("https://api.openweathermap.org/data/2.5/forecast?id=3181927&appid=6de6d5f7dc205d00ce676ee7a2f2274a").json()

# Program loop
# while running:

    # Asks the user for the city or zip code to be queried
    # while True:

        # Input validation
        # try:
        #     print('\nThis application supports search by city(0) or search by zip code(1).')
        #     search = int(input('Please input 0 or 1: '))
        # except ValueError:
        #     print("Sorry, I didn't understand that.")
        # else:
        #
        #     # Passed the validation test
        #     if search == 0:
        #         city = input('Please input the city name: ')
        #         if city.lower() == 'sf':
        #             city = 'San Francisco, US'
        #
        #         # Appends the city to the api call
        #         api_call += '&q=' + city
        #         break
        #
        #     elif search == 1:
        #         zip_code = input('Please input the zip code: ')
        #
        #         # Appends the zip code to the api call
        #         api_call += '&zip=' + zip_code
        #         break
        #
        #     else:
        #         # Prints the invalid number (not 0 or 1)
        #         print('{} is not a valid option.'.format(search))

    # Stores the Json response
    # json_data = requests.get(api_call).json()

    # location_data = {
    #     'city': json_data['city']['name'],
    #     'country': json_data['city']['country']
    # }

    # print('\n{city}, {country}'.format(**location_data))

    # The current date we are iterating through
current_date = ''

# json_data['list'][0]['weather'][0]['description']

    # Iterates through the array of dictionaries named list in json_data
# for item in json_data['list']:
#
#     # Time of the weather data received, partitioned into 3 hour blocks
#     time = item['dt_txt']
#
#     # Split the time into date and hour [2018-04-15 06:00:00]
#     next_date, hour = time.split(' ')
#
#     # Stores the current date and prints it once
#     if current_date != next_date:
#         current_date = next_date
#         year, month, day = current_date.split('-')
#         date = {'y': year, 'm': month, 'd': day}
#         print('\n{m}/{d}/{y}'.format(**date))
#
#     # Grabs the first 2 integers from our HH:MM:SS string to get the hours
#     hour = int(hour[:2])
#
#     # Sets the AM (ante meridiem) or PM (post meridiem) period
#     if hour < 12:
#         if hour == 0:
#             hour = 12
#         meridiem = 'AM'
#     else:
#         if hour > 12:
#             hour -= 12
#         meridiem = 'PM'
#
#     # Prints the hours [HH:MM AM/PM]
#     print('\n%i:00 %s' % (hour, meridiem))
#
#     # Temperature is measured in Kelvin
#     temperature = item['main']['temp']
#
#     # Weather condition
#     description = item['weather'][0]['description'],
#
#     # Prints the description as well as the temperature in Celcius and Farenheit
#     print('Weather condition: %s' % description)
#     print('Celcius: {:.2f}'.format(temperature - 273.15))
#     print('Farenheit: %.2f' % (temperature * 9 / 5 - 459.67))

    # Prints a calendar of the current month
    # calendar = calendar.month(int(year), int(month))
    # print('\n' + calendar)

    # Asks the user if he/she wants to exit
    # while True:
    #     running = input('Anything else we can help you with? ')
    #     if running.lower() == 'yes' or running.lower() == 'y':
    #         print('Great!')
    #         break
    #     elif running.lower() == 'no' or running.lower() == 'n' or running == 'exit':
    #         print('Thank you for using Jaimes Subroto\'s 5 day weather forecast application.')
    #         print('Have a great day!')
    #         running = False
    #         break
    #     else:
    #         print('Sorry, I didn\'t get that.')

def get_motion_detection(old_frame, frame):
    motion = 0
    min_area_motion = 50

    frame_tmp = cv2.GaussianBlur(frame, (21, 21), 0)
    frame_old_tmp = cv2.GaussianBlur(old_frame, (21, 21), 0)

    diff_frame = cv2.absdiff(frame_old_tmp, frame_tmp)
    thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contour of moving object
    (_, cnts) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < min_area_motion:
            continue
        else:
            motion = 1
            # break
            (x, y, w, h) = cv2.boundingRect(contour)
            # making green rectangle arround the moving object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    old_frame = frame.copy()
    return frame

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
ret, first_frame = cap.read()
first_frame = cv2.resize(first_frame, (320, 240))
first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if frame is not None:
        # Our operations on the frame come here
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (320, 240))

        get_motion_detection(first_frame, frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        print("Frame nullo")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()