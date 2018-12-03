# -*- coding: utf-8 -*-

#librerie utili
import telepot

#librerie personali
from tools import *
import chiave
import os

#inizializzazione del bot
bot = telepot.Bot(chiave.Token)

#classe utile a salvare messaggi personalizzati per essere utilizzati con un richiamo
class dedicati:
	def __init__(self):
		pass

	#funzione utile ad aggiungere comandi personalizzati a una chat
	#tiene conto della fase con i
	def Add(self, command, i, gID,  msg):

		if i == 0:					#prima fase   [init]
		
			#crea il file della chat
			if not os.path.isfile("resources/dedicati/"+str(gID)):
				open("resources/dedicati/"+str(gID),"a").close()
			mex("""
				Come vuoi azionare il comando personalizzato?
				Es. "Ciao", "Buongiorno", "ahah" ecc..
			""", gID)
			return 0
			 
		elif i == 1:				#seconda fase [viene registrato il trigger]
			command = command.lower()
			
			with open("resources/dedicati/"+str(gID),"a") as dedicati:
				dedicati.write(command+" | ")
				dedicati.close()
				
			mex("""
			Come vuoi che il bot risponda?
			(Puoi mandare una frase o un contenuto multimediale)
			""", gID)
			return 1
			
		elif i == 2:				#terza fase   [viene registrata la risposta]

			mID = msg["message_id"]
			with open("resources/dedicati/"+str(gID),"a") as dedicati:
				dedicati.write(str(mID)+"\n")
				dedicati.close()
			mex("""
			Comando registrato con successo!
			""", gID)
			return 3

				
		else:
			print("PROBLEMONE")		#???
			
	#funzione utile a trovare dal comando la risposta personalizzata e a inviarla
	def Default(self, command, gID):
		#il file dei comandi personalizzati della chat viene aperta
		with open("resources/dedicati/"+str(gID), "r") as dedicati:
			for line in dedicati:
				l = line.split(" | ")
				dedicato = l[0]					#viene identificato il comando a cui bisogna rispondere
				try:							#except utile quando il comando personalizzato è in fase di registrazione
					mID = int(l[1])				#viene identificata la risposta al comando sotto forma di numero

					if dedicato in command:
						frw(gID, gID, mID)		#il messaggio viene inoltrato alla chat di dovere
						break
				except:
					pass
					
			dedicati.close()					#il file dei comandi personalizzati viene chiuso

	#funzione utile a eliminare un comando personalizzato
	#	il comando viene identificato con un numero v
	def Del(self, command, i, gID):
		#prima fase [vengono visualizzati i comandi]
		if i == 0:
			v = 0															#v viene inizializzata a 0
			mex("Che comando vuoi eliminare?(Es. 1)", gID)
			with open("resources/dedicati/"+str(gID), "r") as dedicati:
				for line in dedicati:
					v += 1													#v aumenta a ogni iterazione per mostrare i messaggi con un identificatore che parte da 1
					l = line.split(" | ")
					trigger = l[0]											#viene identificato il trigger del messaggio
					mex(str(v)+" - "+trigger+"\n", gID)						#i comandi personalizzati vengono inviati nel formato: <n> - <trigger>
			return 0														#la funzione ritorna 0 per dire al processo madre di iniziare la seconda fase

		#seconda fase [viene eliminato il messaggio]
		if i == 1:
			v = 0															#v viene inizializzata a 0
			with open("resources/dedicati/"+str(gID), "r+") as dedicati:
				dedic = dedicati.readlines()								#il file dei comandi personalizzati della chat viene aperto e vengono lette le righe
				dedicati.close()											#il file dei comandi personalizzati della chat viene chiuso
				
			with open("resources/dedicati/"+str(gID), "w") as dedicati:		#il file dei comandi personalizzati della chat viene riaperto
				for line in dedic:
					v += 1													#v aumenta a ogni iterazione per identificare il comando che bisogna eliminare
					if not v == int(command):								#finche il numero della linea non è uguale a v la linea viene riscritta
						dedicati.write(line)

					else:
						mex("Comando eliminato con successo!", gID)			#quando il comando viene trovato non viene riscritto e il messaggio di conferma viene inviato
				dedicati.close()
		
	#funzione utile a visualizzare i comandi personalizzati					
	def Shw(self, gID):
		v = 0																#v viene inizializzata a 0
		mex("Comandi personalizzati:", gID)
		with open("resources/dedicati/"+str(gID), "r") as dedicati:			#il file dei comandi personalizzati della chat viene aperto
			for line in dedicati:
				v += 1														#v aumenta a ogni iterazione per mostrare i messaggi con un indentificatore che parte da 1
				l = line.split(" | ")
				trigger = l[0]												#viene identificato il trigger del messaggio
				mex(str(v)+" - "+trigger+"\n", gID)							# i comandi personalizzati vengono inviati nel formato: <n> - <trigger>
