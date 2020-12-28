import time
import telepot
from telepot.loop import MessageLoop
from PyQt5 import QtCore


class SenderTelegram(QtCore.QThread):

    def __init__(self, config):
        QtCore.QThread.__init__(self)
        TOKEN = config['TELEGRAM']['TOKEN']
        self.bot = telepot.Bot(TOKEN)

        try:
            MessageLoop(self.bot, self.handle).run_as_thread()
        except Exception as e:
            print("Error in plotting values: ", e)

        print('Listening on Telegram...')

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if chat_id == 37221510:
            if msg['text'] == 'temp' or msg['text'] == 'Temp':
                self.bot.sendMessage(chat_id, 'Sending temperature graph...')
                image = open('graphs/temp.png', 'rb')
                self.bot.sendPhoto(chat_id, image)
            if msg['text'] == 'humi' or msg['text'] == 'Humi':
                self.bot.sendMessage(chat_id, 'Sending humidity graph...')
                image = open('graphs/humi.png', 'rb')
                self.bot.sendPhoto(chat_id, image)
            if msg['text'] == 'pres' or msg['text'] == 'Pres':
                self.bot.sendMessage(chat_id, 'Sending pressure graph...')
                image = open('graphs/pres.png', 'rb')
                self.bot.sendPhoto(chat_id, image)


