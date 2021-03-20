#imports
import pygame
import sys
import os
import random
#init pygame 
pygame.init()
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.image.load(r'./2048_logo.png'))
pygame.font.init()
#init my font
TitleFont = pygame.font.Font(r'./csb.ttf', 36)
inGameFont= pygame.font.Font(r'./csb.ttf', 24)
# dimensions
width, height = 80*10, 80*8
screen=pygame.display.set_mode((width, height))
#global variables

#define colours
FONT_24=(119,110,101)
FONT_8PLUS=(249,246,242)
BG_BG=(250,248,239)
BG_GRID=(183,173,160)
BG_NULL=(205,192,180)
BG_2=(238,228,218)
BG_4=(237,224,200)
BG_8=(242,177,121)
BG_16=(245,149,99)
BG_32=(246,124,95)
BG_64=(246,94,59)
BG_128=(237,207,114)
BG_256=(237,204,97)
BG_512=(237,200,80)
BG_1024=(237,197,63)
BG_2048=(237,194,46)
BG_HIGH=(60,58,50)
#define static renders
bg=pygame.image.load(r'./bg.png')
#game state class
class Game(object):
    isGameOver=False
    moved=False
    board=[0 for i in range(16)]
    def __init__(self):
        self.board=[0 for i in range(16)]
        self.addTile()
        self.addTile()
    def prnt(self):
        for x in range(0,4):
                print(self.board[4*x],self.board[4*x+1],self.board[4*x+2],self.board[4*x+3])
    def restart(self):
        self.__init__()
    def addTile(self):
        mt=[]
        curr=0
        for sq in self.board:
            print(curr,": ", sq)
            if sq == 0:
                mt.append(curr)
            curr+=1
        if len(mt) != 0:
            index=random.choice(mt)
            print(index)
            self.board[index]=random.choice([2,4])
        else:
            #partly game over (game is over when there are no more possible moves) 
            print("GameOver!")
        self.prnt()
    
    #board getter setter
    def get_board(self):
        return self.board
    def set_board(self,b):
        if b == self.board:
            moved=False
        else:
            this.board = b 
            this.moved=True
    #gameover setter getter
    def setGame(self, xyz):
        self.isGameOver=xyz
    def getGame(self):
        return self.isGameOver
    #moved setter getter
    def setMoved(self, xyz):
        self.moved=xyz
    def getMoved(self):
        return self.moved
#main class
class main(object):
    def __init__(self,width,hieght):
        self.width=width
        self.height=hieght
        self.Main()
    

    def Main(self):
        #Put all variables up here
        #initialize game state
        g= Game() 
        #render tiles based on spot in grid
        def drawTile(x,y,val):
            size=100
            fx,fy=pos_x,pos_y
            if val == 0 :
                #draw box 
                pygame.draw.rect(screen,BG_NULL,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("", 1, FONT_24)
                screen.blit(num, ((fx+(x*90))+5, (fy+(y*90))+25))
            if val == 2 :
                #draw box 
                pygame.draw.rect(screen,BG_2,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("2", 1, FONT_24)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            if val == 4 :
                #draw box 
                pygame.draw.rect(screen,BG_4,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("4", 1, FONT_24)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            if val == 8 :
                #draw box 
                pygame.draw.rect(screen,BG_8,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("8", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            if val == 16 :
                #draw box 
                pygame.draw.rect(screen,BG_16,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("16", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            if val == 32 :
                #draw box 
                pygame.draw.rect(screen,BG_32,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("32", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            if val == 64 :
                #draw box 
                pygame.draw.rect(screen,BG_64,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("64", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            if val == 128 :
                #draw box 
                pygame.draw.rect(screen,BG_128,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("128", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            if val == 256 :
                #draw box 
                pygame.draw.rect(screen,BG_256,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("256", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            if val == 512 :
                #draw box 
                pygame.draw.rect(screen,BG_512,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("512", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            if val == 1024 :
                #draw box 
                pygame.draw.rect(screen,BG_1024,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("1024", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+25, (fy+(y*size-3*y))+35))
            if val == 2048 :
                #draw box 
                pygame.draw.rect(screen,BG_2048,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("2048", 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+25, (fy+(y*size-3*y))+35))
            
        #inf loop for game
        while 1:
            
            # load background
            screen.fill((250,248,239))
            #load 4x4 grid
            grid_position=(200,150)
            pos_x,pos_y=200,150
            #null background
            pygame.draw.rect(screen,BG_NULL,[200,150,400,400])
            #visual update
            #drawTile(x,y,value)
            for x in range(0,4):
                for y in range(0,4):
                    drawTile(x,y,g.board[x+4*y])
            
            #grid border
            screen.blit(bg,grid_position)#always on top
            #title label
            pygame.draw.rect(screen,BG_2048,[355,25,100,100])
            # render text
            label = TitleFont.render("2048", 1, FONT_8PLUS)
            screen.blit(label, (360, 50))

            
            # keyboard handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('w'):
                        g.addTile()
                        print("up")
                    if event.key == ord('s'):
                        g.addTile()
                        print("down")
                    if event.key == ord('d'):
                        g.addTile()
                        print("right")
                    if event.key == ord('a'):
                        g.addTile()
                        print("left")
                    if event.key == ord(' '):
                        g.restart()
                        print("spc")
                if event.type == pygame.KEYUP:
                    if event.key == ord('w'):
                        print("up-release")
                    if event.key == ord('s'):
                        print("down-release")
                    if event.key == ord('d'):
                        print("right-release")
                    if event.key == ord('a'):
                        print("left-release")
                    if event.key == ord(' '):
                        print("spc-release")
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    exit(0)
                #update
                pygame.display.flip()
#call main
if __name__ == '__main__':
    main(width,height)