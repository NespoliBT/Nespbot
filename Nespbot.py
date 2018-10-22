# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import telegram
import time
import telepot
from telepot.loop import MessageLoop
import subprocess
import random
import coso

def handle(msg):
    chat_id = msg['chat']['id']
    commandH = msg['text']
    command = commandH.lower()

    try:
        username = msg['from']['username']
        print username+': '+commandH+'        ['+str(chat_id)+']'

    except:
        print 'No Username: '+commandH+'      ['+str(chat_id)+']'

    if command == "ciao":
        bot.sendMessage(chat_id, "ciao!!")

#Token del bot.
bot = telepot.Bot(coso.Token)

#Istruzione richiamante 'handle' per i messaggi e 'queryes' per le query
MessageLoop(bot, handle).run_as_thread()

#Non lo so, c'è sempre stato e funziona, non lo voglio toccare.
while 1:
    time.sleep(1)
