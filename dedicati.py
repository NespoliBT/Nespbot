# -*- coding: utf-8 -*-

#librerie utili
import telepot
import sqlite3
import time

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
			dedicati = sqlite3.connect('Databases/dedicati.db')
			cursorDedicati = dedicati.cursor()

			#crea il db della chat se non esiste gia
			cursorDedicati.execute(f"""
				CREATE TABLE IF NOT EXISTS G{gID} (
					ID NUMERIC(50) PRIMARY KEY,
					Trigger VARCHAR(50) NOT NULL,
					mID NUMERIC(20) NOT NULL
				)
			""")
			dedicati.commit()
			dedicati.close()

			mex("""
				Come vuoi azionare il comando personalizzato?
			""", gID)

			return 0

		elif i == 1:				#seconda fase [viene registrato il trigger]
			command = command.lower()
			dedicati = sqlite3.connect('Databases/dedicati.db')

			with open("resources/temp","w") as temp:
				temp.write(command)
				temp.close()

			mex("""
			Come vuoi che il bot risponda?
			(Puoi mandare una frase o un contenuto multimediale)
			""", gID)
			return 1

		elif i == 2:				#terza fase   [viene registrata la risposta]
			mID = msg["message_id"]
			dedicati = sqlite3.connect('Databases/dedicati.db')
			dateTime = time.time()

			try:
				with open("resources/temp","r") as temp:
					trigger = temp.read()
					temp.close()

				with dedicati:
					dedicati.execute(f"""
					INSERT INTO G{gID} (ID, Trigger, mID)
					VALUES(?,?,?)
					""",(dateTime, trigger, mID))

				dedicati.close()

				mex("""
				Comando registrato con successo!
				""", gID)
			except Exception as e:
				print(e)
				mex("""
				Errore durante la registrazione del comando.
				L'errore verrà riportato.
				""", gID)

				mex(f"""
				Errore di registrazione comando nella chat {gID}!!
				{e}
				""", 203240148)

			return 3


		else:
			print("PROBLEMONE")		#???

	#funzione utile a trovare dal comando la risposta personalizzata e a inviarla
	def Default(self, command, gID):
		dedicati = sqlite3.connect('Databases/dedicati.db')
		cursorDedicati = dedicati.cursor()
		try:
			cursorDedicati.execute(f"SELECT mID FROM G{gID} WHERE Trigger=?",(command,))
			mID = cursorDedicati.fetchall()[0][0]
			print(mID)
			frw(gID, gID, mID)

		except Exception as e:
			print(e)

		dedicati.close()					#il database dei comandi personalizzati viene chiuso

	#funzione utile a eliminare un comando personalizzato
	#	il comando viene identificato con un numero v
	def Del(self, command, i, gID):

		dedicati = sqlite3.connect('Databases/dedicati.db')
		cursorDedicati = dedicati.cursor()
		cursorDedicati.execute(f"SELECT Trigger FROM G{gID}")
		lDedicati = cursorDedicati.fetchall()
		dedicati.close()

		#prima fase [vengono visualizzati i comandi]
		if i == 0:
			v = 1															#v viene inizializzata a 0
			try:
				mex(f"Che comando vuoi eliminare?(Es. {lDedicati[0][0]})", gID)

				for i in lDedicati:
					mex(str(v)+" - "+lDedicati[v-1][0], gID)
					v += 1
				return 0
			except:
				mex("Nessun comando da eliminare!", gID)
				return 1

		#seconda fase [viene eliminato il messaggio]
		if i == 1:
			dedicati = sqlite3.connect('Databases/dedicati.db')
			try:
				with dedicati:
					dedicati.execute(f"DELETE FROM G{gID} WHERE Trigger=?",(command,))
				if(command in str(lDedicati)):
					mex("Comando eliminato con successo!", gID)
				else:
					mex("Errore nella eliminazione del comando!", gID)
			except:
				mex("Errore nella eliminazione del comando!", gID)

			dedicati.close()
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
