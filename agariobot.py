#!/usr/bin/python

import math,random,pygame,agario

def bot(screen,self,gcX,gcY,rcX,rcY):

	def convertxy(x,y):
		x=(x)*self.screen_resolution[0]/self.screen_multi/(self.gright-self.gleft)
		y=(y)*self.screen_resolution[1]/self.screen_multi/(self.gtop-self.gbottom)
		return x-rcX,y-rcY
	def convertxy_int(x,y):
		x=(x)*self.screen_resolution[0]/self.screen_multi/(self.gright-self.gleft)
		y=(y)*self.screen_resolution[1]/self.screen_multi/(self.gtop-self.gbottom)
		return int(x-rcX),int(y-rcY)
	def moveaway(gcX,gcY,dot):
		x = gcX- dot.x
		y = gcY - dot.y
		newx = (gcX+x)*2
		newy = (gcY+y)*2
		print "oldx", newx
		print "oldy", newy
		if newy > 10000 or newy < 20:
			newy = random.randrange(20, 10000)
		if newx > 10000 or newx < 20:
			newx = random.randrange(20, 10000) 
		print "newx", newx
		print "newy", newy
		self.moveto(gcX+x, gcY+y)

	mydots={x:self.dots[x] for x in self.myids}	

	otherdots={x:self.dots[x] for x in  filter(lambda x: (x not in self.myids) and (self.dots[x].active==True),self.dots)}

	mylowarea=sorted(mydots.values(),key=lambda x:x.area)[0].area
	mybigarea=sorted(mydots.values(),key=lambda x:x.area)[-1].area

	eater2=(255,0,0)
	eater2_min=(255,0,0)
	eater2_max=(255,0,64)
	eater1=(255,128,128)
	eater1_min=(255,128,0)
	eater1_max=(255,128,64)
	neutral=(128,128,128)
	food1=(128,255,128)
	food1_min=(128,255,0)
	food1_max=(128,255,64)
	food2=(0,255,0)
	virus=(0,0,0)
	food=(0,0,0)

	critSplit=.5*1.5
	critBlob=.33*1.5

	deater=[]
	dplayer=[]
	dvirus=[]
	dfood=[]


	for dot in otherdots.values():
		if dot.size<15:
			dfood.append(dot)
			dot.color=food
		elif dot.type==agario.VIRUS:
			dot.color=virus
			dvirus.append(dot)
		else: # dot.type==agario.NORMAL:
			if dot.area > mylowarea:
				deater.append(dot)
			# food
			if dot.area < 0.70*mylowarea:
				if dot.name != "":
					dplayer.append(dot)
				else:
					dfood.append(dot)
	
	try:
		self.bot3counter-=1
		if self.bot3counter==0:
			self.bot3counter=2
		else:
			return
	except:
		self.bot3counter=1

	nearfood=sorted(dfood,key=lambda x:x.dist(gcX,gcY))
	neareater=sorted(deater,key=lambda x:x.dist(gcX,gcY))
	nearviruses=sorted(dvirus,key=lambda x:x.dist(gcX,gcY))
	nearplayers=sorted(dplayer,key=lambda x:x.dist(gcX,gcY))

	existing = 0

	if len(nearfood) > 0:
		existing += 1
	if len(neareater) > 0:
		existing += 2
	if len(nearviruses) > 0:
		existing += 4
	if len(nearplayers) > 0:
		existing += 8

	print "State: ", existing
	print "gcY", gcY
	print "gcX", gcX

	if existing == 0:
		self.moveto(m.x, m.y)
	elif existing == 1:
		m = nearfood[0]
		#if mylowarea > 5000:
		#	self.split()
		self.moveto(m.x, m.y)
	elif existing == 2:
		m = neareater[0]
		moveaway(gcX, gcY,m)
	elif existing == 3:
		m = neareater[0]
		moveaway(gcX, gcY, m)
	elif existing == 4:
		m = nearviruses[0]
		moveaway(gcX, gcY, m)
	elif existing == 5:
		m = nearviruses[0]
		n = nearfood[0]
		if (m.dist(gcX, gcY)+ m.area) < (n.dist(gcX, gcY) + n.area):
			self.moveto(-m.x, -m.y)
		else:
			self.moveto(n.x, n.y)
	elif existing == 6:
		m = neareater[0]
		moveaway(self, m)
	elif existing == 7:
		m = neareater[0]
		moveaway(gcX, gcY,m)
	elif existing == 8:
		m = nearplayers[0]
		self.moveto(m.x, m.y)
		if (m.dist(gcX, gcY) < mybigarea+150) and (mybigarea*.75 > m.area*2):
			self.split
	elif existing == 9:
		m = nearplayers[0]
		self.moveto(m.x, m.y)
		if (m.dist(gcX, gcY) < mybigarea+150) and (mybigarea*.75 > m.area*2):
			self.split
	elif existing == 10:
		m = neareater[0]
		moveaway(gcX, gcY, m)
	elif existing == 11:
		m = neareater[0]
		moveaway(gcX, gcY,m)
	elif existing == 12:
		m = nearviruses[0]
		n = nearplayers[0]
		if (m.dist(gcX, gcY)+ m.area) < (n.dist(gcX, gcY) + n.area):
			moveaway(gcX, gcY,m)
		else:
			self.moveto(n.x, n.y)
	elif existing == 13:
		m = nearviruses[0]
		n = nearplayers[0]
		if (m.dist(gcX, gcY)+ m.area) < (n.dist(gcX, gcY) + n.area):
			moveaway(gcX, gcY,m)
		else:
			self.moveto(n.x, n.y)
			if (n.dist(gcX, gcY) < mybigarea+150) and (mybigarea*.75 > n.area*2):
				self.split
	elif existing == 14:
		m = neareater[0]
		moveaway(gcX, gcY,m)
	elif existing == 15:
		m = neareater[0]
		moveaway(gcX, gcY,m)

