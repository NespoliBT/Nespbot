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
import os.path
import os
import token
from scose import snomi, sgruppi, aggcom, delcom, shwcom
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from post import post

i = 0
giocatori = []
tris=''
chat_idScon='203240148'
command=''
msgGlobal=''
version = 'v1.9'
bpost=0
titolo=""
s=0
id=""
exit = False

ttt = [[
		InlineKeyboardButton(text=' ', callback_data='11t'),
		InlineKeyboardButton(text=' ', callback_data='21t'),
		InlineKeyboardButton(text=' ', callback_data='31t')
	],[
		InlineKeyboardButton(text=' ', callback_data='12t'),
		InlineKeyboardButton(text=' ', callback_data='22t'),
		InlineKeyboardButton(text=' ', callback_data='32t')
	],[
		InlineKeyboardButton(text=' ', callback_data='13t'),
		InlineKeyboardButton(text=' ', callback_data='23t'),
		InlineKeyboardButton(text=' ', callback_data='33t')
	]]


#Dato un id trova il nome corrispondente
def trovanome(id):
	with open('nomi.txt','r') as nomi:
		for line in nomi:
			idt = line.split(' : ')
			nome = line.split(' | ')
			if int(idt[1]) == int(id):
					break
		nomi.close()
		return nome[0]

#gioca a tictactoe
def tictactoe(msg):
	global tris, ttt, i
	del giocatori[:]
	i = 0
	chat_id = msg['chat']['id']
	ttt = [[
			InlineKeyboardButton(text=' ', callback_data='11t'),
			InlineKeyboardButton(text=' ', callback_data='21t'),
			InlineKeyboardButton(text=' ', callback_data='31t')
		],[
			InlineKeyboardButton(text=' ', callback_data='12t'),
			InlineKeyboardButton(text=' ', callback_data='22t'),
			InlineKeyboardButton(text=' ', callback_data='32t')
		],[
			InlineKeyboardButton(text=' ', callback_data='13t'),
			InlineKeyboardButton(text=' ', callback_data='23t'),
			InlineKeyboardButton(text=' ', callback_data='33t')
		]]

	tictactoe = InlineKeyboardMarkup(inline_keyboard = ttt)
	tris = bot.sendMessage(chat_id, "Il classico gioco tris", reply_markup = tictactoe)


#Funzione utile ad avvertire una persona in privato.
#I parametri passati sono: Il messaggio e il testo del messaggio.
#Questa funzione controlla prima se l'utente è il non disturbare.
#Se non è in non disturbare esso verrà notificato con il nome del gruppo dove è stato chiamato e il messaggio con cui è stato chiamato.
def avverti(msg, commandH):
	nondisturbare = False
	with open('stato.txt','r') as f:
		for line in f:
			l = line.split('|')
			if l[0] == msg['chat']['id']:
				if l[1] == 'Off':
					nondisturbare = True
		f.close()
		if nondisturbare == False:
			nome = commandH.split(' ')
			with open('nomi.txt','r') as f:
				for line in f:
					l = line.split(' : ')
					g = line.split(' | ')
					if g[0] == nome[1]:
						destinatario = l[1]
		f.close()
	mex(nome[1]+' guarda che ti hanno chiamato sul gruppo:\n'+msg['chat']['title']+'\n\nMessaggio:\n'+commandH, destinatario, False)



#Funzione utile ad accendere il bot.
#I parametri passati sono: il messaggio.
#Questa funzione è divisa in tre parti:
#	Formattazione dello stato salvando in l[0] l'ID della chat e in l[1] il suo stato.
#	Se non si trova lo stato del bot si scrive.
#	Se si trova lo stato del bot si scrive.
def accenditi(msg):
	nome = msg['chat']['id']
	trovato = False
	bot.sendAudio(nome, 'CQADBAADIAQAAlJYQFJDrvmHspGYaQI')
	with open('stato.txt','r') as f:
		for line in f:
			l = line.split('|')
			if l[0] == str(nome):
				trovato = True
				break
		f.close()
		if trovato == False:
			with open('stato.txt','a') as nt:
				nt.write(str(nome)+'|On|\n')
		else:
			with open('stato.txt','r') as t:
				lines = t.readlines()
				t.close()

			with open('stato.txt','w') as t:
				for line in lines:
					l = line.split('|')
					if l[0] == str(nome):
						t.write(str(nome)+'|On|\n')
					else:
						t.write(line)
				t.close()


#Funzione utile ad spegnere il bot.
#I parametri passati sono: il messaggio.
#Questa funzione è divisa in tre parti:
#	Formattazione dello stato salvando in l[0] l'ID della chat e in l[1] il suo stato.
#	Se non si trova lo stato del bot si scrive.
#	Se si trova lo stato del bot si scrive.
def spegniti(msg):
	nome = msg['chat']['id']
	trovato = False
	bot.sendAudio(nome, 'CQADBAADHwQAAlJYQFI_7rfAc1YllQI')
	with open('stato.txt','r') as f:
		for line in f:
			l = line.split('|')
			if l[0] == str(nome):
				trovato = True
				break
		f.close()
		if trovato == False:
			with open('stato.txt','a') as nt:
				nt.write(str(nome)+'|On|\n')

		else:
			with open('stato.txt','r') as t:
				lines = t.readlines()
				t.close()

			with open('stato.txt','w') as t:
				for line in lines:
					l = line.split('|')
					if l[0] == str(nome):
						t.write(str(nome)+'|Off|\n')
					else:
						t.write(line)
				t.close()

#Funzione utile a trovare lo stato del bot in una chat.
#I parametri passati sono: il messaggio.
#Ritorana lo stato del bot se si trova.
#Ritorna 'On' se lo stato del bot non si trova.
def stato(msg):
	nome = msg['chat']['id']
	trovato = False
	with open('stato.txt','r') as f:
		for line in f:
			l = line.split('|')
			if l[0] == str(nome):
				trovato = True
				break
		f.close()
	if trovato == True:
		return str(l[1])
	else:
		return 'On'

#Funzione utile a cancellare un messaggio.
#I parametri passati sono: il messaggio stesso.
#Agisce in modo diverso in base a:
#	Se il messaggio è una risposta
#	Se il messaggio non è una risposta
#	Se il messaggio è scritto il privato
#	Se non è admin
def zittoF(msg):
	chat_id = msg['chat']['id']
	try:
		msg['reply_to_message'] != ''
		if msg['chat']['type'] != 'private':
			try:
				bot.deleteMessage((chat_id, msg['reply_to_message']['message_id']))
				bot.deleteMessage((chat_id, msg['message_id']))
			except:
				mex('Potrei non essere admin', chat_id)
		else:
			try:
				bot.deleteMessage((chat_id, msg['reply_to_message']['message_id']))
			except:
				mex('Non posso cancellare i tuoi messaggi in privato, stupidino', chat_id)
	except:
		mex("Rispondi a un messaggio con '/zitto' per cancellarlo", chat_id)


#Funzione utile a pinnare un messaggio.
#I parametri passati sono: il messaggio stesso.
#Se rileva un errore pinnando il messaggio farà notare che il bot non è admin o il gruppo non è un supergruppo.
def pinna(msg):
	chat_id = msg['chat']['id']
	try:
		reply_to_message = msg['reply_to_message']
		bot.pinChatMessage(chat_id, reply_to_message['message_id'], True)
		if msg['from']['id'] == 203240148:
			mex("Pinnato, mia Eccellenza", chat_id)
	except:
		mex("Va che non sono admin\nOppure non sono in un supergruppo", chat_id)


#Funzione utile a verificare se nel messaggio inviato è presente una certa stringa "com".
#I parametri passati sono: la stringa da controllare.
#Ritorna True se la stringa è presente nel comando, ritorna False se la stringa non è presente nel comando.
def com(com):
	global command
	if com in command:
		return True
	else:
		return False


#Funzione utile a controllare, con l'ausilio di "def com", a controllare se il messaggio contiene una parola o una frase dedicata.
#I parametri passati sono: il messaggio stesso.
#Le frasi dedicate sono salvate in 'dedicati.txt'.
#Ogni gruppo con l'ausilio di /aggcom e /delcom può modificare i le frasi dedicate alla propria chat.
def dedicati(msg):
	chat_id = msg['chat']['id']
	with open('dedicati.txt','r') as g:
		for line in g:
			finale=line.split('/',1)
			if com(finale[0].lower()):
				mex(finale[1], chat_id)
		g.close()

	if msg['chat']['type'] != 'private':
		if os.path.isfile('gruppi/'+str(chat_id)+'.txt'):
			with open('gruppi/'+str(chat_id)+'.txt','r') as g:
				for line in g:
					finale=line.split('|',1)
					if com(finale[0].lower()):
						mex(finale[1], chat_id)
			g.close()


#Funzione utile a inviare messaggi a un chat_id.
#I parametri passati sono: il messaggio da inviare, il chat_id a cui inviarlo
#Non è possibile specificare il messaggio come risposta o aggiungere altri parametri, in quel caso è consigliabile l'utilizzo di bot.sendMessage.
def mex(mess, cid, risp = True):
	global msgGlobal
	if risp == False:
		bot.sendMessage(cid, mess)
	else:
		bot.sendMessage(cid, mess, reply_to_message_id = msgGlobal['message_id'])


#Funzione utile a gestire le query arrivate dalle chat.
#I parametri passati sono il messaggio, e quindi la query, da processare.
#È la prima ad essere chiamata, assieme ad 'handle', da "MessageLoop".
#Questa funzione è divisa in tre parti fondamentali:
#	La dichiarazione delle variabili.
#	La stampa della 'Callback Query'
#	L'esecuizione di diverse istruzioni in base al 'query_data'
def queryes(msg):
	global tris, ttt, i
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	chat_id = msg['message']['chat']['id']

	print('Callback Query:', query_id, from_id, query_data)
	if query_data == 'Download':
		bot.sendDocument(from_id, open('changelog.txt'))
	elif query_data == 'Messaggio':
		with open('changelog.txt','r') as changelog:
			chglog = changelog.read()
			changelog.close()

		mex('Di seguito il changelog della versione: '+version, from_id)
		mex(chglog, from_id, False)
	elif query_data[2] == 't':
		if not from_id in giocatori and not len(giocatori) == 2:
			giocatori.append(from_id)
			mex(trovanome(from_id)+' ha iniziato a giocare', chat_id, False)

		prox = giocatori[i]
        #Gestione del comando /tictactoe
		if from_id in giocatori and prox == from_id:
			pos0 = int(query_data[0])-1
			pos1 = int(query_data[1])-1
			i += 1
			i %= 2
			if from_id == giocatori[0]:
				mossa = '🅾'
			else:
				mossa = '❎'
			ttt[pos1][pos0] = InlineKeyboardButton(text = mossa, callback_data = 'xxx')

			tictactoe = InlineKeyboardMarkup(inline_keyboard = ttt)
			edited = telepot.message_identifier(tris)
			try:
				players = trovanome(giocatori[0])+' '+trovanome(giocatori[1])
			except:
				players = trovanome(giocatori[0])

			try:
				bot.editMessageText(edited, 'Giocatori: '+players, reply_markup = tictactoe)
			except:
				print 'Manca un giocatore ----------------------------'



#Funzione utile a gestire i messaggi arrivati dalle chat.
#I parametri passati sono: il messaggio da processare.
#È la prima ad essere chiamata, insieme a 'queryes', da "MessageLoop".
#Questa funzione è divisa in quattro parti fondamentali:
#	La dichiarazione delle variabili.
#	La formattazione del comando, estrapolandolo anche da file multimediali.
#	La stampa a video del comando/messaggio arrivato.
#	Il controllo della presenza del messaggio, con l'ausilio di "def com", in uno dei comandi specificati da if e elif.
def handle(msg):
	#Variabili principali
	global chat_idScon, command, version, msgGlobal, zitto, bpost, titolo, s
	msgGlobal = msg
	ran = random.random()
	chat_id = msg['chat']['id']

	#Formattazione del messaggio arrivato.
	#Per comodità del controllo tutti i messaggi vengono duplicati in una versione tutta in minuscolo (.lower()).
	try:
		commandH = msg['text']
		command = commandH.lower() #Il messaggio viene formattato in minuscolo

	except:
		#Se l'estrapolazione del messaggio come testo fallisce si tenta di estrapolarlo dalla 'caption' del contenuto multimediale.
		try:
			commandH = msg['caption']
			command = commandH.lower() #Il messaggio viene formattato in minuscolo

		except:
		#Se l'estrapolazione del messaggio come 'caption' fallisce si descrive il messaggio come 'Contenuto multimediale', ad esempio un messaggio audio.
			commandH = 'Contenuto multimediale'
			command = commandH

	#Si cerca in primo luogo di dare un username a chi ha inviato un messaggio.
	try:
		username = msg['from']['username']
		print username+': '+commandH+'        ['+str(chat_id)+']'

	except:
		#Se questo non ha un username gli viene affidato lo username: 'No Username'.
		print 'No Username: '+commandH+'      ['+str(chat_id)+']'

	snomi(msg)	#Ogni messaggio arrivato viene, in una classe esterna a questo file, processato in modo da estrapolare da esso: Username, Nome, Cognome e ID del mittente.

	if bpost==2 and chat_id == 203240148:
		bpost=0
		post(titolo, commandH)

	if bpost==1 and chat_id == 203240148:
		bpost=2
		titolo=commandH
		mex("Corpo:",203240148)

	if com('/post') and chat_id == 203240148:
		bpost=1
		mex("Titolo:",203240148)

	#Se il messaggio contiene '/risp' e il mittente è Nespoli esso verrà inviato dal bot a un ID specificato nelle righe seguenti di questo codice.
	if com('/risp') and chat_id == 203240148:
		mex(commandH[5:], chat_idScon, False)

	#Se il messaggio contiene '/idrisp' e il mittente è Nespoli esso verrà inviato dal bot a un ID specificato nel messaggio.
	if com('/idrisp') and chat_id == 203240148:
		finale = commandH.split(' ',2)
		mex(finale[2], int(finale[1]), False)

	#Se il messaggio contiene '@nespbot': L'id del messaggio viene salvato per essere usato nella funzione /risp.
	#									  Esso viene inviato in privato a Nespoli che con il comando /risp potrà rispondere.
	if com("@nespbot"):
		chat_idScon = chat_id
		mex(username+': '+commandH, 203240148, False)

    #Se il messaggio contiene '/bug': Viene inviato un messaggio di report a Nespoli(203240148)
	if command[:4] == '/bug':
		mex('Bug:\n\n'+'Nome: @'+username+'\n\nMessaggio: '+commandH, 203240148, False)

	#Se la chat non è privata, allora è un gruppo o un supergruppo.
	#Ogni messaggio viene, in una classe esterna a questo file, processato in modo da estrapolare da esso: il nome del gruppo e ID del gruppo.
	if msg['chat']['type'] != 'private':
		sgruppi(msg)

	#Se il messaggio contiene 'nespoli' esso viene mandato nella forma originale in chat privata a Nespoli.
	if com('nespoli'):
		mex(u'Hanno scritto questo su un gruppo:\n'+unicode(commandH)+u'\n\n'+unicode(msg['chat']['title'])+u'\n\n'+unicode(chat_id), '203240148', False)

	if command[:7] == '/avvisa':
		avverti(msg, commandH)

	#Accendi e spegni il bot
	if command == '/spegniti':
		spegniti(msg)
	if command == '/accenditi':
		accenditi(msg)

	#Se stato(msg) resistituisce 'Off' il bot non parla.
	if stato(msg) == 'On':

		#Se il messaggio contiene '/start' viene presentato in breve la funzione del bot.
		if command[:6] == '/start':
			mex("Ciao! Io sono Nespbot, il bot di Nespoli. \nL'avresti mai detto?", chat_id)

		#Cancella il messaggio a cui si risponde
		elif command[:6] == ('/zitto'):
			zittoF(msg)

		#Se il messaggio equivale a 'nespo pinna' ed è una risposta ad un messaggio, il messaggio a cui si risponde viene pinnato.
		elif command == 'nespo pinna' and msg['reply_to_message'] != '':
			pinna(msg)

		#Se il messaggio equivale a '/aggcom' vengono inviati dei messaggi esplicativi del comando.
		elif command == ('/aggcom') or command == ('/aggcom@nespbot'):
			mex('Il comando /aggcom si utilizza così:', chat_id)
			mex('/aggcom <parola dedicata>|<risposta>', chat_id, False)
			mex('/shwcom per vedere i comandi personalizzati', chat_id, False)

		#Se il messaggio equivale a '/delcom' vengono inviati dei messaggi esplicativi del comando.
		elif command == ('/delcom') or command == ('/delcom@nespbot'):
			mex('Il comando /delcom si utilizza così:', chat_id)
			mex('/delcom <parola dedicata>|<risposta>', chat_id, False)
			mex('/shwcom per vedere i comandi personalizzati', chat_id, False)

		#Se il messaggio equivale a '/shwcom' il bot invia, tramite una classe esterna a questo file, la serie di comandi personalizzati della chat specificati con '/aggcom' e '/delcom'.
		elif command == ('/shwcom') or command == ('/shwcom@nespbot'):
			if msg['chat']['type'] != 'private':
				shwcom(msg)
			else:
				mex('Comando non utilizzabile nelle chat private', chat_id)

		#Se il messaggio contine '/aggcom' il bot salva, tramite una classe esterna a questo file, la parola o la frase dedicata con la sua risposta dedicata.
		elif com('/aggcom'):
			if msg['chat']['type'] != 'private':
				aggcom(commandH, msg)
				mex(commandH[8:]+' aggiunto!', chat_id)
			else:
				mex('Comando non utilizzabile nelle chat private', chat_id)

		#Se il messaggio contiene '/delcom' il bot rimuove, tramite una classe esterna a questo file, la parola o la frase dedicata con la sua risposta dedicata.
		elif com('/delcom'):
			if msg['chat']['type'] != 'private':
				delcom(commandH, msg)
			else:
				mex('Comando non utilizzabile nelle chat private', chat_id)

		#Se il messaggio equivale a '/test' vengono inviati alla chat tutti i contenuti del messaggio.
		elif command[:5] == '/test':
			mex(msg, chat_id)

		#Se il messaggio equivale a '/version' viene inviata la versione attuale del bot.
		elif command[:8] == '/version':
			mex(version, chat_id)

		#Se il messaggio equivale a '/changelog' viene inviato il changelog dell'ultima versione.
		elif command[:10] == '/changelog':
			comandi =[[
				InlineKeyboardButton(text='⬇️Download⬇️', callback_data='Download'),
				InlineKeyboardButton(text='✉️Messaggio✉️', callback_data='Messaggio'),
				]]
			keyboard = InlineKeyboardMarkup(inline_keyboard=comandi)
			bot.sendMessage(chat_id, "Come preferisci visualizzare il changelog?", reply_markup=keyboard)

		#Se il meesaggio equivale a '/download' viene inviato il codice del bot.
		elif command[:9] == '/download':
			mex('Nespbot è il file principale mentre scose è il file contenente alcune funzioni esterne', chat_id)
			bot.sendDocument(chat_id, open('Nespbot.py'))
			bot.sendDocument(chat_id, open('scose.py'))


		#Se il messaggio equivale a '/help' viene inviata una lista dei comandi nella versione attuale
		elif command[:5] == '/help':
			with open('help.txt','r') as h:
				cmd = h.read()
			h.close()
			mex('Di seguito la lista dei comandi nella versione: '+version, chat_id)
			mex(cmd, chat_id, False)

		#Se il messaggio contiene '/r8' in bot invierà, in risposta al messaggi a cui il mittente ha risposto o, in alternativa, al messaggi stesso, un numero che va da 3 a 10.
		elif com('/r8'):
			ran = random.randrange(30,100,1)
			try:
				reply_to_message = msg['reply_to_message']['message_id']
				bot.sendMessage(chat_id, str(ran/10)+'/10 -IGN', reply_to_message_id = reply_to_message)
			except:
				mex(str(ran/10)+'/10 -IGN', chat_id)

		#gioca anche tu a tris!
		elif command[:10] =='/tictactoe':
			tictactoe(msg)

		#erano bei tempi!
		elif com('bei tempi'):
			bot.sendVoice(chat_id, 'AwADBAADGgUAAiqsaVMpAAFy4SiYzmIC')

		elif com('fai una capriola'):
			mex('Non posso farlo', chat_id)

		#Se nessuno di elif viene soddisfatto si passa alla funzione di default 'dedicati'.
		else:
			dedicati(msg)


#Token del bot.
bot = telepot.Bot(token.Token)

#Istruzione richiamante 'handle' per i messaggi e 'queryes' per le query
MessageLoop(bot, {'chat': handle,
				  'callback_query': queryes}).run_as_thread()

#Non lo so, c'è sempre stato e funziona, non lo voglio toccare.
while 1:
    time.sleep(1)
