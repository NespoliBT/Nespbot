# -*- coding: utf-8 -*-
import chiave
import telepot

bot = telepot.Bot(chiave.Token)

#classe utile a inviare messaggi testuali dato testo e pID
class mex:
	def __init__(self, text, pID):
		bot.sendMessage(pID, text)

		
class frw:
	def __init__(self, gID, pID, mID):
		bot.forwardMessage(gID, pID,  mID)