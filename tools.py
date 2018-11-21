# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import chiave
import telepot

bot = telepot.Bot(chiave.Token)

#classe utile a inviare messaggi testuali dato testo e pID
class mex:
	def __init__(self, text, pID):
		bot.sendMessage(pID, text)