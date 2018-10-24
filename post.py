# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class post:
	def __init__(self, titolo, corpo):
		self.titolo = titolo
		self.corpo = corpo

		h = open('/var/www/blog/resources/menu.txt','r')
		side=h.readlines()
		side=''.join(side)
		h.close()

		f = open('/var/www/blog/resources/blog.txt','r+')
		lines = f.readlines()
		f.seek(0)
		f.write('<h3>'+titolo+'</h3>'+'\n'+'<p>'+corpo+'</p>')
		for line in lines:
			f.write(line)
		f.close()
		
		f = open('/var/www/blog/resources/blog.txt','r')
		blog = f.readlines()
		blog=''.join(blog)

		c = open('/var/www/blog/alaura.html','w')

		c.write(str(side)+'\n'+str(blog)+'<div style="height: 40vw;"></div></div></div></body></html>')
