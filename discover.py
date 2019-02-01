# -*- coding: utf-8 -*-
import sqlite3

#classe utile a ricavare le informazioni necessarie al consumo dei dati da "msg".
#questa classe ha anche il compito di registrare username, nome, cognome e pID del mittente per futuro uso
class discover:
	def __init__(self, msg):
		pID = msg["from"]["id"] 							#pID del mittente

		gID = msg["chat"]["id"]								#ID del gruppo

		try:
			capitalCommand = msg["text"]					#testo del messaggio
		except:
			try:
				capitalCommand = msg["caption"]				#testo del messaggio in caso sia un contenuto multimediale con descrizione
			except:
				capitalCommand = "Contenuto Multimediale"	#defualt in caso sia un contenuto multimediale senza descrizione
		command = capitalCommand.lower()					#testo del messaggio ma tutto minuscolo

		try:
			username = msg["from"]["username"]				#username dell'utente
		except:
			username = "N/D"								#default in caso l'utente non abbia un username

		try:
			nome = msg["from"]["first_name"]				#nome dell'utente
		except:
			nome = "noName"									#default in caso l'utente non abbia un nome

		try:
			cognome = msg["from"]["last_name"]				#cognome dell'utente
		except:
			cognome = "noSurname"							#default in caso l'utente non abbia un cognome

		if msg["chat"]["type"] == "private":
			private = True									#identificatore del tipo di chat -> privata(True)
			strprivate = "Private"							#identificatore del tipo di chat -> privata("Private")
		else:
			private = False									#identificatore del tipo di chat -> pubblica(False)
			strprivate = "Public"							#identificatore del tipo di chat -> pubblica("Public")



		#fase di registrazione di username, nome, cognome e pID
		nomi = sqlite3.connect('Databases/nomi.db')
		try:
			with nomi:
				nomi.execute("""
				INSERT INTO Users(ID, Name, Surname, Username)
				VALUES(?,?,?,?)
				""",(pID, nome, cognome, username))
		except sqlite3.IntegrityError:
			pass
		finally:
			nomi.close()


		#a ognuna di queste variabili globali alla classe viene assegrato uno dei dati dell'utente
		self.pID = str(pID)						#pID dell'utente sotto forma di stringa
		self.gID = str(gID)						#ID del gruppo sotto forma di stringa
		self.command = command					#comando tutto minuscolo
		self.capitalCommand = capitalCommand	#comando
		self.username = username				#username dell'utente
		self.private = private					#identificatore del tipo di chat
		self.strprivate = strprivate			#identificatore del tipo di chat in stringa

		#TODO salvare gruppi
		#gruppi = sqlite3.connect('gruppi.db')


	#quanto viene richiamata la funzione get di questa classe essa restituisce i dati ricavati dal messaggio
	def get(self):
		return self.pID, self.gID, self.command, self.capitalCommand, self.username, self.private, self.strprivate

#dato il pID dell'utente questa classe ricava le seguenti informazioni:
#	username, nome, cognome
class pIDiscover:

	def __init__(self, pID):
		nomi = sqlite3.connect('Databases/nomi.db')
		cursorNomi = nomi.cursor()

		cursorNomi.execute("SELECT Name, Surname, Username FROM Users WHERE ID=?", (pID,))
		self.info = cursorNomi.fetchall()[0]
		nomi.close()


	#quanto viene richiamata la funzioen get di questa classe essa restituisce i dati trovati fino ad ora
	def get(self):
		return self.info
