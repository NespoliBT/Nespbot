# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#librerie utili
import telepot
from telepot.loop import MessageLoop
import time

#librerie personali
from discover import *			#fetching informazioni e archiviazione
from tools import *				#utlità del bot
import chiave 					#token del bot


def handle(msg):

	#ottiene tutte le informazioni utili dal messaggio
	info = discover(msg).get()
	
	pID = info[0]				#id dell'utente
	command = info[1]			#comando inviato dall'utente
	capitalCommand = info[2]	#comando comprensivo di maiuscole inviato dall'utente
	username = info[3]			#username dell'utente
	private = info[4]			#identifica se la chat è privata(True) o pubblica(False)
	strprivate = info[5]		#stringa contenente il tipo di chat(Private, Public)+

	#visualizza informazioni principali dei messaggi per debugging
	print("from: "+username+"   ["+pID+"]\n   command: "+command+"   ["+strprivate+"]")


#inizializzazione del bot
bot = telepot.Bot(chiave.Token)

#ogni messaggio viene inoltrato a "handle" per consumarlo
MessageLoop(bot, handle).run_as_thread()

while 1:
	time.sleep(1)


