# -*- coding: utf-8 -*-

#librerie utili
import telepot
from telepot.loop import MessageLoop
import time

#librerie personali
from discover import *			#fetching informazioni e archiviazione
from tools import *				#utlità del bot
import chiave 					#token del bot
from dedicati import *			#comandi personalizzati

#Variabili grobali di cui non posso fare a meno :(
statoCom = ""
statoDel = ""



def handle(msg):
	global statoCom, statoDel
	#ottiene tutte le informazioni utili dal messaggio
	info = discover(msg).get()

	pID = info[0]				#id dell'utente
	gID = info[1]				#id del gruppo
	command = info[2]			#comando inviato dall'utente
	capitalCommand = info[3]	#comando comprensivo di maiuscole inviato dall'utente
	username = info[4]			#username dell'utente
	private = info[5]			#identifica se la chat è privata(True) o pubblica(False)
	strprivate = info[6]		#stringa contenente il tipo di chat(Private, Public)+

	#visualizza informazioni principali dei messaggi per debugging
	print("from: "+username+"   ["+pID+"]\n   command: "+command+"   ["+strprivate+"]")



	#comandi che necessitano di più messaggi
	if statoCom == 0:							#seconda fase comandi personalizzati
		statoCom = dedicati().Add(capitalCommand, 1, gID, msg)

	elif statoCom == 1:							#terza fase dei comandi personalizzati
		statoCom = dedicati().Add(capitalCommand, 2, gID, msg)

	if statoDel == 0:							#seconda fase della rimozione di un comando personalizzato
		statoDel = dedicati().Del(command, 1, gID)



	#il comando start è il primo messaggio con cui si inizializza un bot
	elif command == "/start" or command == "/start@nespbot":
		mex("""
			Ciao, questo bot è attualmente in sviluppo.
			Link utili:
			https://GitHub.com/NespoliBT/Nespbot
			http://blog.NespoliBT.com

			Comandi utili:
			/help

		""", pID)

	#il comando help permette di mostrare dal contenuto di un file i comandi utilizzabili
	elif command == "/help" or command == "/help@nespbot":
		with open("resources/help.txt","r") as help:
			h = help.read()
			help.close()
		mex(h, pID)

	#il comando /add permette di aggiungere comandi personalizzati
	elif command == "/add" or command == "/add@nespbot":		#prima fase comandi personalizzati
		statoCom = dedicati().Add(capitalCommand, 0, gID, msg)

	#il comando /del permette di rimuovere comandi personalizzati
	elif command == "/del" or command == "/del@nespbot":		#prima fase della rimozione di un comando personalizzato
		statoDel = dedicati().Del(command, 0, gID)

	#il comando /shw permette di visualizzare i comandi personalizzati
	elif command == "/shw" or command == "/shw@nespbot":
		dedicati().Shw(gID)

	#ogni messaggio viene controllato per dei messaggi personalizzati
	else:
		dedicati().Default(command, gID)

#inizializzazione del bot
bot = telepot.Bot(chiave.Token)

#ogni messaggio viene inoltrato a "handle" per consumarlo
MessageLoop(bot, handle).run_as_thread()

while 1:
	time.sleep(1)
