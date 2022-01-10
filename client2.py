import pygame as pg
from network import Network
from pygame.locals import *

pg.init()

class Window:
	def __init__(self):
		self.width=300
		self.height=300
		self.win=pg.display.set_mode((self.width,self.height))
		pg.display.set_caption("Tic Tac Toe Client 2")

	def drawWindow(self,Player1,Player2):
		bg=(255,255,200)
		grid=(50,50,50)
		lineWidth=4
		self.win.fill(bg)
		for x in range(1,3):
			pg.draw.line(self.win,grid,(0,x*100),(self.width,x*100),lineWidth)
			pg.draw.line(self.win,grid,(x*100,0),(x*100,self.height),lineWidth)
		Player1.draw(self.win)
		Player2.draw(self.win)
	def readPos(self,posn):
		posn=posn.split(",")
		return int(posn[0]),int(posn[1]),int(posn[2])

	def makePos(self,posn):
		return str(posn[0])+","+str(posn[1])+","+str(posn[2])

class Player:
	def __init__(self,nos):
		self.board=[[0,0,0] for _ in range(3)]
		self.id=nos
		self.curpos=(None,None)
	def moves(self,pos,opponent):
		#print("CUR POS: ",pos)
		self.curpos=pos
		x,y=pos
		x=x//100
		y=y//100
		if self.board[x][y]==0 and opponent.board[x][y]==0:
			self.board[x][y]=1
	def draw(self,win):
		green = (0,255,0)
		red = (255,0,0)
		x_pos=0
		for x in self.board:
			y_pos=0
			for y in x:
				if y==1 and self.id==1:
					pg.draw.line(win,green,(x_pos*100+15,y_pos*100+15),(x_pos*100+85,y_pos*100+85),4)
					pg.draw.line(win,green,(x_pos*100+15,y_pos*100+85),(x_pos*100+85,y_pos*100+15),4)
				elif y==1 and self.id==2:
					pg.draw.circle(win,red,(x_pos*100+50,y_pos*100+50),38,4)	
				y_pos+=1
			x_pos+=1
	def resetBoard(self):
		self.board=[[0,0,0] for _ in range(3)]						
def checkWinner(Player):
	win1,win2,win3,win4=(True,True,True,True)
	for i in range(3):
		win1=True
		win2=True
		for j in range(3):	
			win1&=Player.board[i][j]
			win2&=Player.board[j][i]
		if win1 or win2:
			break
	for i in range(3):
		win3&=Player.board[i][i]
		win4&=Player.board[i][2-i]

	return win1 or win2 or win3 or win4		

def checkDraw(Player1,Player2):
	count=0
	for i in range(3):
		for j in range(3):
			if(Player1.board[i][j] or Player2.board[i][j]):
				count+=1
	if count==9:
		return True
	return False

def drawWinner(winner,window):
	font=pg.font.SysFont(None,40)
	if winner != "Draw":
		winText=winner+" Wins!"
	else:
		winText="Draw!"	
	winImg=font.render(winText,True,(0,0,255))
	pg.draw.rect(window.win,(0,255,0),(window.width//2-100,window.height//2-60,200,50))
	window.win.blit(winImg,(window.width//2-100,window.height//2-50))

def drawPlayAgain(window):
	font=pg.font.SysFont(None,40)
	againRect=Rect(window.width//2-80,window.height//2,160,50)
	againText="Play again?"
	againImg=font.render(againText,True,(0,0,255))
	pg.draw.rect(window.win,(0,255,0),againRect)
	window.win.blit(againImg,(window.width//2-80,window.height//2+10))
	return againRect

def main():
	gameOver=0
	winner=None

	window=Window()
	
	n=Network()

	Player1=Player(1)
	Player2=Player(2)
	
	run=True
	clicked=False

	while run:

		if gameOver == 0:
			revMov=n.latestMov
			if len(revMov)!=0:
				posn=window.readPos(revMov)
				if posn[2]==1:
					Player1.moves((posn[0],posn[1]),Player2)
			window.drawWindow(Player1,Player2)
			pg.display.update()

			if(checkWinner(Player1)):
				print("Player1 wins!")
				winner="Player1"
				gameOver=1
			if(checkWinner(Player2)):
				print("Player2 wins!")
				winner="Player2"
				gameOver=1
		for event in pg.event.get():
			if event.type==pg.QUIT:
				run=False
				break
			if gameOver==0:
				if event.type==pg.MOUSEBUTTONDOWN and clicked==False:
					clicked=True
				if event.type==pg.MOUSEBUTTONUP and clicked==True:
					clicked=False
					Player2.moves(pg.mouse.get_pos(),Player1)
					n.send(window.makePos((Player2.curpos[0],Player2.curpos[1],2)))
			else:
				if event.type==pg.MOUSEBUTTONDOWN and clicked==False:
					print("REACHED")
					clicked=True
				if event.type==pg.MOUSEBUTTONUP and clicked==True:
					clicked=False
					pos=pg.mouse.get_pos()
					if againRect.collidepoint(pos):
						Player1.resetBoard()
						Player2.resetBoard()
						winner=None
						gameOver=0
						clicked=False
						n.reset()
						pg.display.update()
		window.drawWindow(Player1,Player2)

		if gameOver == 0:
			if(checkWinner(Player1)):
				print("Player1 wins!")
				winner="Player1"
				gameOver=1
			if(checkWinner(Player2)):
				print("Player2 wins!")
				winner="Player2"
				gameOver=1

			if(checkDraw(Player1,Player2)):
				print("Draw!")
				winner="Draw"
				gameOver=1

		if gameOver == 1:
			drawWinner(winner,window)
			againRect=drawPlayAgain(window)

		pg.display.update()
	pg.quit()

main()