import pygame
from pygame.locals import *
import os
import serial

def agrid(canvas, ascale):
	for i in range(-5,5):
		label=sfnt.render(str(round(40*i/ascale,2)),1,fpen,bg)
		canvas.blit(label,(5,195-40*i))

pygame.font.init()


h,w=400,800										
ascale=1										
fs=250											
fnt=pygame.font.SysFont("arial",15)				
sfnt=pygame.font.SysFont("arial",11)			
bg=pygame.Color(255,255,255)					
gpen=pygame.Color(150,150,150)					
spen=pygame.Color(0,0,255)						
wpen=pygame.Color(255,0,0)						
fpen=pygame.Color(0,0,0)					


grid=pygame.Surface((w,h))
grid.fill(bg,((0,0),(w,h)))


taxis=pygame.Surface((w,20))
taxis.fill(bg,((0,0),(w,20)))


aaxis=pygame.Surface((50,h))
aaxis.fill(bg,((0,0),(50,h)))
agrid(aaxis,ascale)


hor=0
hinc=0.2*fs
ctr=0

for i in range(-5,5):
	if not(i):														
		sflag=1
	else:
		sflag=0
	pygame.draw.line(grid,gpen,(0,200-40*i),(w,200-40*i),1+sflag)	

while hor<w:
	if not(ctr%5):												
		sflag=1
	else:
		sflag=0
	pygame.draw.line(grid,gpen,(hor,0),(hor,h),1+sflag)				
	num=sfnt.render(str(round(hor/fs,2))+"s",1,fpen,bg)				
	taxis.blit(num,(hor,0))
	hor+=hinc
	ctr+=1


pygame.init()
screen=pygame.display.set_mode((w+50,h+20))						
pygame.display.set_caption("Srcotron EKG")
screen.fill(bg,((0,0),(w+50,h+20)))
screen.blit(taxis,(50,0))
screen.blit(aaxis,(0,20))
canvas=pygame.Surface((w,h))									
canvas.fill(bg,((0,0),(w,h)))
canvas.blit(grid, (0,0))
pygame.display.flip()

# serial init
s=serial.Serial()
s.baudrate=57600

s.open()


time=[]
signal=[]
pulse=[]

# log file
log = open("log.csv","w")
log.write("time, signal, pulse_flag\n")

running=True

ctr=0
reads=0
ppoint=(0,0)
lastR=0
while running:
	
	if pygame.event.peek("QUIT"):																		
		running = False
	for event in pygame.event.get():																
		print(event)
	keys=pygame.key.get_pressed()																	
	if keys[pygame.K_UP]!=0:
		ascale+=0.04
		aaxis.fill(bg,((0,0),(50,h)))
		agrid(aaxis,ascale)
		screen.blit(aaxis,(0,20))
	if keys[pygame.K_DOWN]!=0:
		ascale-=0.04
		aaxis.fill(bg,((0,0),(50,h)))
		agrid(aaxis,ascale)
		screen.blit(aaxis,(0,20))

	try:																							
		if ctr==w:																					
			ctr=0
			canvas.blit(grid, (0,0))
			ppoint=(0,ppoint[1])
		a=s.readline()																				
		data=a.split()																				
		time.append(int(data[0]))
		signal.append(float(data[1]))
		pulse.append(int(data[4]))
		loc=200-int(ascale*float(signal[reads]))													
		pygame.draw.line(canvas,spen,ppoint,(ctr,loc),1)
		ppoint=(ctr,loc)																			
		if data[4]=='1':																			
			label=fnt.render("T="+str(round((reads-lastR)*1000/fs,2))+"ms",1,fpen,bg)
			canvas.blit(label,(ctr,h-20))
			lastR=reads
		screen.blit(canvas,(50,20))
		pygame.display.flip()																		
		
		ctr+=1
		reads+=1
		log.write(data[0]+", "+data[1]+", "+data[4]+"\n")											
	except:
		print("step failed")
os.system("pause")
log.close()
