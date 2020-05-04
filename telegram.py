import time
import telepot
from telepot.loop import MessageLoop
from PyQt5 import QtCore


class SenderTelegram(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        TOKEN = '900451039:AAH9ieek4ZfldhHbe9OWM9ubcFjfnqlCH90'
        self.bot = telepot.Bot(TOKEN)

        MessageLoop(self.bot, self.handle).run_as_thread()
        # print('Listening ...')

        # Keep the program running.
        # while 1:
        #     time.sleep(10)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if chat_id == 37221510:
            if msg['text'] == 'temp':
                self.bot.sendMessage(chat_id, 'Sending temperature graph...')
                image = open('graphs/temp.png', 'rb')
                self.bot.sendPhoto(chat_id, image)
            if msg['text'] == 'humi':
                self.bot.sendMessage(chat_id, 'Sending humidity graph...')
                image = open('graphs/humi.png', 'rb')
                self.bot.sendPhoto(chat_id, image)
            if msg['text'] == 'pres':
                self.bot.sendMessage(chat_id, 'Sending pressure graph...')
                image = open('graphs/pres.png', 'rb')
                self.bot.sendPhoto(chat_id, image)


