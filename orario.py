# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import telegram
import telepot
import chiave
import datetime


#Token del bot.
bot = telepot.Bot(chiave.Token)

def mex(mess, cid):
	bot.sendMessage(cid, mess)


class orario:
	def __init__(self):
		giorni=["domenica","lunedì","martedì","mercoledì","giovedì","venerdì","sabato"]
		self.giorni = giorni
		self.giorno=int(datetime.date.today().strftime("%w"))
		self.g=giorni[self.giorno]
		print self.g

		
	def get(self, chat_id):
		self.chat_id = chat_id
		mex("Di seguito l'orario di oggi:", chat_id)
		with open("orari/"+str(chat_id)+"/"+str(self.giorno)+".txt", "r") as orario:
			for line in orario:
				l = line.split(" | ")
				ora = l[0]
				materia = l[1]
				prof = l[2]
				aula = l[3]
				note = l[4]
				mex("Ora: "+ora+"\nMateria: "+materia+"\nProf: "+prof+"\nAula: "+aula+"\nNote: "+note, chat_id)
			orario.close()
			
	def setup(self, chat_id, command="ND"):
		self.chat_id = chat_id
		g = self.g
		giorni = self.giorni
		if command != "ND":
			with open("orari/"+str(chat_id)+"/sts.txt","r") as sts:
				r = sts.readline()
				r = r.split(" | ")
				n=r[0]
				y=r[1]
				print n, r

				sts.close()
		else:
			os.makedirs("orari/"+str(chat_id))
			n=0
			y=0

			
		if int(y) < 7:
			g=giorni[int(y)]
			mex("Inserisci i dati di "+g+"\n\nFormat:\nOra | Materia | Prof | Aula | Note", chat_id)
		if command != "ND":


			with open("orari/"+str(chat_id)+"/"+str(n)+".txt","w+") as defin:
				defin.write(command)
			with open("orari/"+str(chat_id)+"/sts.txt","w+") as sts:
				sts.write(str(int(n)+1)+" | "+str(int(y)+1))
		else:
			with open("orari/"+str(chat_id)+"/sts.txt","w+") as sts:
				sts.write("0 | 1")
				
		if int(n)+1==7:
			print "sono arrivato fino a qui"
			return True
		else:
			return False
		