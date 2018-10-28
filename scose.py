# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import telegram
import telepot
import chiave

#Token del bot.
bot = telepot.Bot(chiave.Token)


#Salva, in caso non fossero gia salvati: Username, Nome, Cognome e ID del mittente nel file: 'nomi.txt'.
class snomi:
	def __init__(self, msg):
		self.msg = msg
		with open("nomi.txt", "a+r") as nomi:
			finid='lol'
			for line in nomi:
				ident = line.split(': ',1)
				if int(msg['from']['id']) != int(ident[1]):
					finid = msg['from']['id']
				else:
					finid='n.d.'
					break

			if finid != 'n.d.':
				try:
					username = msg['from']['username']
				except:
					username = 'N.D.' 					#Se non ha un Username gli viene assegnato: 'N.D.'.
				try:
					nome = msg['from']['first_name']
				except:
					nome = 'noname'						#Se non ha un nome gli viene assegnato: 'noname'.
				try:
					cognome = msg['from']['last_name']
				except:
					cognome = 'nosurname'				#Se non ha un cognome gli viene assegnato: 'nosurname'.
				nomi.write(('@'+username+' | '+unicode(nome)+' '+unicode(cognome)+' '+': '+unicode(msg['from']['id'])+'\n'))
			nomi.close()


#Salva, in caso non fossero gia salvati: Nome e ID del gruppo in: 'gruppi.txt'.
class sgruppi:
	def __init__(self, msg):
		self.msg = msg
		with open("gruppi.txt","a+r") as gruppi:
			for line in gruppi:
				l = line.split('|')
				if unicode(l[1]) == unicode(msg['chat']['id']):
					nome = 'n.d.'
					break
				else:
					nome = msg['chat']['title']
			if unicode(nome) != u'n.d.':
				gruppi.write(unicode(nome)+'|'+unicode(msg['chat']['id'])+'|\n')

#Controlla la presenza dell'ID del gruppo e ne salva quindi il nome.
#Se non esiste un file personale del gruppo lo crea.
#Se esiste un file personale del gruppo salva il messaggio dedicato con la sua risposta nel file del gruppo.
class aggcom:
	def __init__(self, command, msg):
		self.command = command
		self.msg = msg
		with open("gruppi.txt","a+r") as gruppi:
			for line in gruppi:
				l = line.split('|')
				if unicode(l[1]) == unicode(msg['chat']['id']):
					nome = unicode(l[1])
					break
			gruppi.close()
	
		if not os.path.isfile('gruppi/'+nome+'.txt'):
			with open('gruppi/'+nome+'.txt','w+') as f:
				f.write(u'/nomegruppo|'+unicode(msg['chat']['title'])+u'\n')
				f.close
	
		with open('gruppi/'+nome+'.txt',"a+r") as gruppo:
			comm = 'Buongiorno'
			for line in gruppo:
				l = line.split('|')
				if unicode(line) == unicode(command[8:]):
					comm = 'Buongiorno'
					break
				else:
					comm = unicode(command[8:])
			if comm != 'Buongiorno':
				gruppo.write(unicode(comm)+'\n')
			gruppo.close()

#Controlla la presenza dell'ID del gruppo e ne salva quindi il nome.
#Rimuove il messaggio dedicato con la sua risposta nel file del gruppo.
class delcom:
	def __init__(self, command, msg):
		self.command = command
		self.msg = msg
		with open("gruppi.txt","a+r") as gruppi:
			for line in gruppi:
				l = line.split('|')
				if unicode(l[1]) == unicode(msg['chat']['id']):
					nome = unicode(l[1])
					break
			gruppi.close()
	
		f = open('gruppi/'+nome+'.txt',"r")
		lines = f.readlines()
		f.close()
		f = open('gruppi/'+nome+'.txt',"w")
		for line in lines:
			if line != command[8:]+"\n":
				f.write(line)

#Controlla la presenza dell'ID del gruppo e ne salva quindi il nome.
#Manda nella chat in cui è stato digitato il messaggio una lista contenente i messaggi personalzzati con la loro risposta
class shwcom:
	def __init__(self, msg):
		self.msg = msg
		chat_id = msg['chat']['id']
		with open("gruppi.txt","a+r") as gruppi:
			for line in gruppi:
				l = line.split('|')
				if unicode(l[1]) == unicode(msg['chat']['id']):
					nome = unicode(l[1])
					break
			gruppi.close()
	
		f = open('gruppi/'+nome+'.txt',"r")
		lines = f.readlines()
		f.close()
		bot.sendMessage(chat_id, ''.join(lines), reply_to_message_id = msg['message_id'])

