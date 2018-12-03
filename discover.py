# -*- coding: utf-8 -*-

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
		#il file "nomi.txt" nella directory "resources" viene aperto con capacità di lettura e scrittura
		#ogni linea di questo file è scritta in questo modo: @<username> | <nome> | <cognome> : <pID> 
		with open("resources/nomi.txt","r+") as nomi:
		
			brk=False					#identificatore di break: True-> una corrispondenza è stata trovata. False -> nessuna corrispondenza trovata.
			for line in nomi:
				l=line.split(" : ")		#ogni linea viene divisa in due (l[0] -> info dell'utente, l[1] -> pID dell'utente)
				if pID != int(l[1]):
					toRegister = pID	#il pID da registrare viene aggiornato a ogni iterazione
				else:
					brk=True			#se il pID è gia nella lista l'identificatore viene aggiornato a True
					break				#il ciclo si ferma
						
			if not brk:					#se il ciclo non ha trovato nessuna corrispondenza i dati dell'utente vengono registrati
				nomi.write("@"+username+" | "+nome+" | "+cognome+" : "+str(pID)+"\n")
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
		#with open("resources/gruppi.txt","a+r") as gruppi:

		
	#quanto viene richiamata la funzione get di questa classe essa restituisce i dati ricavati dal messaggio
	def get(self):
		return self.pID, self.gID, self.command, self.capitalCommand, self.username, self.private, self.strprivate

#dato il pID dell'utente questa classe ricava le seguenti informazioni:
#	username, nome, cognome
class pIDiscover:

	def __init__(self, pID):
		#viene aperto il file "nomi.txt" nella directory "resources"
		#ogni linea di questo file è scritta in questo modo: @<username> | <nome> | <cognome> : <pID> 
		with open("resources/nomi.txt","r") as nomi:
			for line in nomi:
				UnknownpID=line.split(" : ")[1]				#viene identificato come UnknownpID il pID di ogni riga  
				if int(UnknownpID) == int(pID):				#quando viene trovata una corrispondenza tra UnknownpID e il pID da trovare i dati di questi vengono salvati
					info=line.split(" : ")[0].split(" | ")
					self.username=info[0]					#username dell'utente
					self.nome=info[1]						#nome dell'utente
					self.cognome=info[2]					#cognome dell'utente
					break									#fine del ciclo -> una corrispondenza è stata trovata
			nomi.close()
	#quanto viene richiamata la funzioen get di questa classe essa restituisce i dati trovati fino ad ora
	def get(self):
		return self.username, self.nome, self.cognome
				
	