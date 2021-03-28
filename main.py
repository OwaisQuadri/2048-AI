#imports
import copy
import pygame
import sys
import os
import random
import copy
import datetime
from statistics import mean
from pynput.keyboard import Key,Controller
keyboard=Controller()
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
offset=500
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
    #high score
    with open('highScore.txt', 'r') as f:
        f.seek(0)
        highScore=(int(float(f.read())))
        isGameOver=False
    moved=False
    def __init__(self):
        self.board=[offset for i in range(16)]
        self.addTile()
        self.addTile()
        self.__score=offset
        self.isGameOver=False
        self.recorded=False    
    def duplicate(self,get):
        if get:
            L=[]
            score=[]
            with open('currentBoard', 'r') as f:
                f.seek(0)
                c=0
                for line in f:
                    if c==0:
                        for word in line.split():
                            L.append(int(float(word)))
                    elif c==1:
                        for word in line.split():
                            score.append(int(float(word)))
                    c+=1
            self.board=L
            self.setScore(score[0])           
        else:
            with open('currentBoard', 'w') as f:
                boardString=""
                for b in self.board:
                    boardString+=str(b)+" "
                f.write(boardString)
                f.write("\n")
                f.write(str(self.getScore()))
    def prnt(self):
        for x in range(4):
            print(str(self.board[4*x]-offset)," ",str(self.board[4*x+1]-offset)," ",str(self.board[4*x+2]-offset)," ",str(self.board[4*x+3]-offset))
    def restart(self):
        self.__init__()
    
    def addTile(self):
        mt=[]
        curr=0
        #if there are any empty squares
        for sq in self.board:
            if sq == offset:
                #add to empty square list
                mt.append(curr)
            curr+=1
        #if empty array isnt empty there are avail spaces
        self.empty_spaces=len(mt)
        if self.empty_spaces != 0:
            #randomly select square
            index=random.choice(mt)
            #randomly select value
            self.board[index]=offset+random.choice([2,2,2,2,2,2,2,2,2,4])
            self.empty_spaces-=1
    #movement
    
    def swipe(self,dir,test=False):
        self.moved=False
        joined=False
        #create empty list L and B
        L=[]
        B=self.board
        #initial array
        b4=[]
        if dir=="up":
            #then
            # 0 < 4 < 8 < 12
            # loop through list by columns
            # we want order 0,4,8,12,  1,5,9,13,  2,6,10,14,  3,7,11,15
            
            for i_col in range(4):
                for i_row in range (4):
                    #loop varaible index
                    index=i_col+(i_row*4)
                    #add to b4 list
                    iindex=i_row+4*i_col
                    b4.append(self.board[iindex])
                    #check if curr == (cur -1), add together and make joined=true
                    if self.board[index] != offset:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=(self.board[index]-offset)#add current to latest entry in L
                                #add points
                                self.__score=self.__score+self.board[index]-offset
                                joined=True#therefore joinging them (joined=True)
                            else:
                                #append the value as a new element to L
                                L.append(self.board[index])
                                #and joined remains False
                                joined=False
                #outside one loop,not both:
                #add current combined column/row (L) to overall board list B and empty L
                #starting at 0 and going up by 4 for output
                out=0
                while out <= 12 :
                    if len(L)!=0 :#if L has elements
                        #put them at the index i_col+out of B and remove from L
                        B[i_col+out]=L.pop(0)
                    else:#put 0 at same index
                        B[i_col+out]=offset
                    out+=4
        elif dir == "down":
            #then
            # 0 > 4 > 8 > 12
            # loop through list by columns
            # we want order 12,8,4,0,  ...
            for i_col in range(4):
                for i_row in range (4):
                    #loop varaible index
                    index=i_col+(12-i_row*4)
                    #add to b4 list
                    iindex=i_row+4*i_col
                    b4.append(self.board[iindex])
                    #check if curr == (cur -1), add together and make joined=true
                    if self.board[index] != offset:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=(self.board[index]-offset)#add current to latest entry in L
                                #add points
                                self.__score=self.__score+self.board[index]-offset
                                joined=True#therefore joinging them (joined=True)
                            else:
                                #append the value as a new element to L
                                L.append(self.board[index])
                                #and joined remains False
                                joined=False
                #outside one loop,not both:
                #add current combined column/row (L) to overall board list B and empty L
                #starting at 12 and going down by 4 for output
                out=12
                while out >= 0 :
                    if len(L)!=0 :#if L has elements
                        #put them at the index i_col+out of B and remove from L
                        B[i_col+out]=L.pop(0)
                    else:#put 0 at same index
                        B[i_col+out]=offset
                    out-=4
        elif dir == "right":
            #then
            # 0 > 1 > 2 > 3
            # loop through list by columns
            # we want order 0,1,2,3,  ...
            for i_row in range(4):
                for i_col in range (4):
                    #loop varaible index
                    index=(3-i_col)+(i_row*4)
                    #add to b4 list
                    iindex=4*i_row+i_col
                    b4.append(self.board[iindex])
                    #check if curr == (cur -1), add together and make joined=true
                    if self.board[index] != offset:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=(self.board[index]-offset)#add current to latest entry in L
                                #add points
                                self.__score=self.__score+self.board[index]-offset
                                joined=True#therefore joinging them (joined=True)
                            else:
                                #append the value as a new element to L
                                L.append(self.board[index])
                                #and joined remains False
                                joined=False
                #outside one loop,not both:
                #add current combined column/row (L) to overall board list B and empty L
                #starting at 0 and going up by 1 for output
                out=3
                while out >= 0 :
                    if len(L)!=0 :#if L has elements
                        #put them at the index i_col+out of B and remove from L
                        B[i_row*4+out]=L.pop(0)
                    else:#put 0 at same index
                        B[i_row*4+out]=offset
                    out-=1
        elif dir == "left":
            #then
            # 0 > 1 > 2 > 3
            # loop through list by columns
            # we want order 0,1,2,3,  ...
            for i_row in range(4):
                for i_col in range (4):
                    #loop varaible index
                    index=i_col+(i_row*4)
                    #add to b4 list
                    iindex=4*i_row+i_col
                    b4.append(self.board[iindex])
                    #check if curr == (cur -1), add together and make joined=true
                    if self.board[index] != offset:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=(self.board[index]-offset)#add current to latest entry in L
                                #add points
                                self.__score=self.__score+self.board[index]-offset
                                joined=True#therefore joinging them (joined=True)
                            else:
                                #append the value as a new element to L
                                L.append(self.board[index])
                                #and joined remains False
                                joined=False
                #outside one loop,not both:
                #add current combined column/row (L) to overall board list B and empty L
                #starting at 0 and going up by 1 for output
                out=0
                while out <= 3 :
                    if len(L)!=0 :#if L has elements
                        #put them at the index i_col+out of B and remove from L
                        B[i_row*4+out]=L.pop(0)
                    else:#put 0 at same index
                        B[i_row*4+out]=offset
                    out+=1
        else:
            pass
        #update score
        if self.__score > self.highScore:
            self.highScore=self.__score
            with open('highScore.txt', 'w') as f:
                f.write(str(self.highScore))
        #once the loop completes, outside all the if/elif/else statements:
        # do g.setBoard with B, which is the overall board list
        self.set_board(B,b4)
        if test:
            if self.moved:
                self.addTile()
    #board getter setter
    def get_board(self):
        return self.board
    def set_board(self,b,b4):
            if b != b4:
                self.board = b 
                self.moved=True
    #gameover setter getter
    def setGameOver(self, xyz):
        self.isGameOver=xyz
    def getGameOver(self):
        #function to check if game is over
        #if game is over cover game with screen that says "press 'SPC' to try again"
        #if there are no more empty slots and none of the same numbers next to one another, game is over
        #first loop through entire array once and check for no zeros
        for b in self.board:
            if b == offset :
                #if any zeros, return with isgameover=false
                self.isGameOver=False
                return self.isGameOver
        for j in range (4):#loop through rows to check for adgacent same numbers
            for i in range(1,4):
                index = i+4*j
                
                if self.board[index] == self.board[index-1]:
                    #if any, return with no action
                    self.isGameOver=False
                    return self.isGameOver
        for j in range (4):#loop through columns to check for adgacent same numbers
            for i in range(1,4):
                index = j+4*i
                
                if self.board[index] == self.board[index-4]:
                    #if any, return with no action
                    self.isGameOver=False
                    return self.isGameOver   
        self.isGameOver=True
        return self.isGameOver
    #moved setter getter
    def setMoved(self, xyz):
        self.moved=xyz
    def getMoved(self):
        return self.moved
    #score getter and maybe setter if needed
    def getScore(self):
        return self.__score
    def setScore(self,score):
        self.__score=score
    #get highscore
    def getHighScore(self):
        return self.highScore
#main class
class main(object):
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.Main()
    
    def Main(self):
        #Put all variables up here
        #initialize game state
        g= Game() 
        #initialize agent
        a=Agent(keyboard,g)
        #render tiles based on spot in grid
        def drawTile(x,y,value):
            size=100
            fx,fy=pos_x,pos_y
            val = value-offset
            if val == 0 :
                #draw box 
                pygame.draw.rect(screen,BG_NULL,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render("", 1, FONT_24)
                screen.blit(num, ((fx+(x*90))+5, (fy+(y*90))+25))
            elif val == 2 :
                #draw box 
                pygame.draw.rect(screen,BG_2,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_24)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            elif val == 4 :
                #draw box 
                pygame.draw.rect(screen,BG_4,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_24)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            elif val == 8 :
                #draw box 
                pygame.draw.rect(screen,BG_8,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+45, (fy+(y*size-3*y))+35))
            elif val == 16 :
                #draw box 
                pygame.draw.rect(screen,BG_16,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            elif val == 32 :
                #draw box 
                pygame.draw.rect(screen,BG_32,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            elif val == 64 :
                #draw box 
                pygame.draw.rect(screen,BG_64,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+39, (fy+(y*size-3*y))+35))
            elif val == 128 :
                #draw box 
                pygame.draw.rect(screen,BG_128,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            elif val == 256 :
                #draw box 
                pygame.draw.rect(screen,BG_256,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            elif val == 512 :
                #draw box 
                pygame.draw.rect(screen,BG_512,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+33, (fy+(y*size-3*y))+35))
            elif val == 1024 :
                #draw box 
                pygame.draw.rect(screen,BG_1024,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+25, (fy+(y*size-3*y))+35))
            elif val == 2048 :
                #draw box 
                pygame.draw.rect(screen,BG_2048,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+25, (fy+(y*size-3*y))+35))
            else:
                #draw box 
                pygame.draw.rect(screen,BG_HIGH,[(fx+(x*size)),(fy+(y*size)),size,size])
                #draw lettering
                num= inGameFont.render(str(val), 1, FONT_8PLUS)
                screen.blit(num, ((fx+(x*size-3*x))+25, (fy+(y*size-3*y))+35))
        highest_tile=0
        #inf loop for game
        my_prompts=[]
        moves=0
        starttime=datetime.datetime.now()
        while 1:
            #every in game tick we make 1 move
            #calculate moves per second in current run
            
            moves+=1
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
            # render title
            label = TitleFont.render("2048", 1, FONT_8PLUS)
            screen.blit(label, (360, 50))
            #render score
            score = inGameFont.render(("Score: "+str(g.getScore()-offset)),1,FONT_24)
            screen.blit(score,(200,550))
            #highscore
            highscoredisplay = inGameFont.render(("High Score: "+str(g.getHighScore()-offset)),1,FONT_24)
            screen.blit(highscoredisplay,(200,575))
            #render if game over screen
            if g.getGameOver() :
                #if game is over cover game with translucent screen that says "press 'SPC' to try again"
                endGame= inGameFont.render(("press 'SPC' to try again"),1,FONT_24)
                screen.blit(endGame,(200,600))
                total_games,numOf_512,numOf_1024,numOf_2048,numOf_128,numOf_256=0,0,0,0,0,0
                if not g.recorded:
                    highest_tile=max(g.get_board())-offset
                    
                    with open('records.txt', 'r') as f:
                        f.seek(0)
                        c=0
                        for line in f:
                            if c==0:
                                for word in line.split():
                                    total_games=int(float(word))
                            elif c==3:
                                for word in line.split():
                                    numOf_512=int(float(word))
                            elif c==4:
                                for word in line.split():
                                    numOf_1024=int(float(word))
                            elif c==5:
                                for word in line.split():
                                    numOf_2048=int(float(word))
                            elif c==1:
                                for word in line.split():
                                    numOf_128=int(float(word))
                            elif c==2:
                                for word in line.split():
                                    numOf_256=int(float(word))
                            c+=1
                    #update with this current game
                    total_games+=1
                    if highest_tile >= 512:
                        numOf_512+=1
                    if highest_tile >= 1024:
                        numOf_1024+=1
                    if highest_tile >= 2048:
                        numOf_2048+=1
                    if highest_tile >= 128:
                        numOf_128+=1
                    if highest_tile >= 256:
                        numOf_256+=1
                    
                    #output percentages in console
                    percent_512=(numOf_512/total_games)*100
                    percent_1024=(numOf_1024/total_games)*100
                    percent_2048=(numOf_2048/total_games)*100
                    percent_128=(numOf_128/total_games)*100
                    percent_256=(numOf_256/total_games)*100
                    print('')
                    print("Number of games played: ",total_games)
                    print("")
                    print("128: ",percent_128,"%")
                    print("256: ",percent_256,"%")
                    print("512: ",percent_512,"%")
                    print("1024: ",percent_1024,"%")
                    print("2048: ",percent_2048,"%")
                    totaltime=datetime.datetime.now()-starttime
                    moves_per_sec=moves/totaltime.seconds
                    print('')
                    print("Highest Tile: ",highest_tile)
                    print("moves per second: ",moves_per_sec)
                    with open('records.txt', 'w') as f:
                        f.write(str(total_games))
                        f.write("\n")
                        f.write(str(numOf_128))
                        f.write("\n")
                        f.write(str(numOf_256))
                        f.write("\n")
                        f.write(str(numOf_512))
                        f.write("\n")
                        f.write(str(numOf_1024))
                        f.write("\n")
                        f.write(str(numOf_2048))
                    g.recorded=True
                #restart game
                restart = pygame.event.Event(pygame.KEYDOWN, key=ord(" ")) #autorestart (comment out if not testing)
                pygame.event.post(restart)
                moves=0
                starttime=datetime.datetime.now()
            #save in file
            g.duplicate(False)
            #create event
            direction=a.think()
            newevent = pygame.event.Event(pygame.KEYDOWN, key=ord(direction)) #create the event
            pygame.event.post(newevent) #add the event to the queue
            # keyboard handling
                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == ord('w') :
                        g.swipe("up")
                        if (g.getMoved()):
                            g.addTile()
                            my_prompts=[]
                        else:
                            if( not g.getGameOver()):
                                my_prompts+='w'
                                backup = pygame.event.Event(pygame.KEYDOWN, key=ord(a.think(prompt=my_prompts)))
                                pygame.event.post(backup)
                    if event.key == ord('s'):
                        g.swipe("down")
                        if (g.getMoved()):
                            g.addTile()
                            my_prompts=[]
                        else:
                            if( not g.getGameOver()):
                                my_prompts+='s'
                                backup = pygame.event.Event(pygame.KEYDOWN, key=ord(a.think(prompt=my_prompts)))
                                pygame.event.post(backup)
                    if event.key == ord('d'):
                        g.swipe("right")
                        if (g.getMoved()):
                            g.addTile()
                            my_prompts=[]
                        else:
                            if( not g.getGameOver()):
                                my_prompts+='d'
                                backup = pygame.event.Event(pygame.KEYDOWN, key=ord(a.think(prompt=my_prompts)))
                                pygame.event.post(backup)
                    if event.key == ord('a'):
                        g.swipe("left")
                        if (g.getMoved()):
                            g.addTile()
                            my_prompts=[]
                        else:
                            if( not g.getGameOver()):
                                my_prompts+='a'
                                backup = pygame.event.Event(pygame.KEYDOWN, key=ord(a.think(prompt=my_prompts)))
                                pygame.event.post(backup)
                    if event.key == ord(' '):
                        g.restart()
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    exit(0)
                #update
                g.duplicate(False)
                pygame.display.flip()


class Agent(object):
    
    def __init__(self,keyboard,game):
        self.keyboard=keyboard
        self.g=game
    
    
    def helper(self, g):
        direction=["up","right","down","left"]
        #
        g[0].swipe("up",True)
        g[0].swipe("up",True)
        g[0].swipe("up",True)
        #
        g[1].swipe("up",True)
        g[1].swipe("up",True)
        g[1].swipe("right",True)
        #
        g[2].swipe("up",True)
        g[2].swipe("up",True)
        g[2].swipe("down",True)
        #
        g[3].swipe("up",True)
        g[3].swipe("up",True)
        g[3].swipe("left",True)
        #
        g[4].swipe("up",True)
        g[4].swipe("right",True)
        g[4].swipe("up",True)
        #
        g[5].swipe("up",True)
        g[5].swipe("right",True)
        g[5].swipe("right",True)
        #
        g[6].swipe("up",True)
        g[6].swipe("right",True)
        g[6].swipe("down",True)
        #
        g[7].swipe("up",True)
        g[7].swipe("right",True)
        g[7].swipe("left",True)
        #
        g[8].swipe("up",True)
        g[8].swipe("down",True)
        g[8].swipe("up",True)
        #
        g[9].swipe("up",True)
        g[9].swipe("down",True)
        g[9].swipe("right",True)
        #
        g[10].swipe("up",True)
        g[10].swipe("down",True)
        g[10].swipe("down",True)
        #
        g[11].swipe("up",True)
        g[11].swipe("down",True)
        g[11].swipe("left",True)
        #
        g[12].swipe("up",True)
        g[12].swipe("left",True)
        g[12].swipe("up",True)
        #
        g[13].swipe("up",True)
        g[13].swipe("left",True)
        g[13].swipe("right",True)
        #
        g[14].swipe("up",True)
        g[14].swipe("left",True)
        g[14].swipe("down",True)
        #
        g[15].swipe("up",True)
        g[15].swipe("left",True)
        g[15].swipe("left",True)
        #
        g[16].swipe("right",True)
        g[16].swipe("up",True)
        g[16].swipe("up",True)
        #
        g[17].swipe("right",True)
        g[17].swipe("up",True)
        g[17].swipe("right",True)
        #
        g[18].swipe("right",True)
        g[18].swipe("up",True)
        g[18].swipe("down",True)
        #
        g[19].swipe("right",True)
        g[19].swipe("up",True)
        g[19].swipe("left",True)
        #
        g[20].swipe("right",True)
        g[20].swipe("right",True)
        g[20].swipe("up",True)
        #
        g[21].swipe("right",True)
        g[21].swipe("right",True)
        g[21].swipe("right",True)
        #
        g[22].swipe("right",True)
        g[22].swipe("right",True)
        g[22].swipe("down",True)
        #
        g[23].swipe("right",True)
        g[23].swipe("right",True)
        g[23].swipe("left",True)
        #
        g[24].swipe("right",True)
        g[24].swipe("down",True)
        g[24].swipe("up",True)
        #
        g[25].swipe("right",True)
        g[25].swipe("down",True)
        g[25].swipe("right",True)
        #
        g[26].swipe("right",True)
        g[26].swipe("down",True)
        g[26].swipe("down",True)
        #
        g[27].swipe("right",True)
        g[27].swipe("down",True)
        g[27].swipe("left",True)
        #
        g[28].swipe("right",True)
        g[28].swipe("left",True)
        g[28].swipe("up",True)
        #
        g[29].swipe("right",True)
        g[29].swipe("left",True)
        g[29].swipe("right",True)
        #
        g[30].swipe("right",True)
        g[30].swipe("left",True)
        g[30].swipe("down",True)
        #
        g[31].swipe("right",True)
        g[31].swipe("left",True)
        g[31].swipe("left",True)
        #
        g[32].swipe("down",True)
        g[32].swipe("up",True)
        g[32].swipe("up",True)
        #
        g[33].swipe("down",True)
        g[33].swipe("up",True)
        g[33].swipe("right",True)
        #
        g[34].swipe("down",True)
        g[34].swipe("up",True)
        g[34].swipe("down",True)
        #
        g[35].swipe("down",True)
        g[35].swipe("up",True)
        g[35].swipe("left",True)
        #
        g[36].swipe("down",True)
        g[36].swipe("right",True)
        g[36].swipe("up",True)
        #
        g[37].swipe("down",True)
        g[37].swipe("right",True)
        g[37].swipe("right",True)
        #
        g[38].swipe("down",True)
        g[38].swipe("right",True)
        g[38].swipe("down",True)
        #
        g[39].swipe("down",True)
        g[39].swipe("right",True)
        g[39].swipe("left",True)
        #
        g[40].swipe("down",True)
        g[40].swipe("down",True)
        g[40].swipe("up",True)
        #
        g[41].swipe("down",True)
        g[41].swipe("down",True)
        g[41].swipe("right",True)
        #
        g[42].swipe("down",True)
        g[42].swipe("down",True)
        g[42].swipe("down",True)
        #
        g[43].swipe("down",True)
        g[43].swipe("down",True)
        g[43].swipe("left",True)
        #
        g[44].swipe("down",True)
        g[44].swipe("left",True)
        g[44].swipe("up",True)
        #
        g[45].swipe("down",True)
        g[45].swipe("left",True)
        g[45].swipe("right",True)
        #
        g[46].swipe("down",True)
        g[46].swipe("left",True)
        g[46].swipe("down",True)
        #
        g[47].swipe("down",True)
        g[47].swipe("left",True)
        g[47].swipe("left",True)
        #
        g[48].swipe("left",True)
        g[48].swipe("up",True)
        g[48].swipe("up",True)
        #
        g[49].swipe("left",True)
        g[49].swipe("up",True)
        g[49].swipe("right",True)
        #
        g[50].swipe("left",True)
        g[50].swipe("up",True)
        g[50].swipe("down",True)
        #
        g[51].swipe("left",True)
        g[51].swipe("up",True)
        g[51].swipe("left",True)
        #
        g[52].swipe("left",True)
        g[52].swipe("right",True)
        g[52].swipe("up",True)
        #
        g[53].swipe("left",True)
        g[53].swipe("right",True)
        g[53].swipe("right",True)
        #
        g[54].swipe("left",True)
        g[54].swipe("right",True)
        g[54].swipe("down",True)
        #
        g[55].swipe("left",True)
        g[55].swipe("right",True)
        g[55].swipe("left",True)
        #
        g[56].swipe("left",True)
        g[56].swipe("down",True)
        g[56].swipe("up",True)
        #
        g[57].swipe("left",True)
        g[57].swipe("down",True)
        g[57].swipe("right",True)
        #
        g[58].swipe("left",True)
        g[58].swipe("down",True)
        g[58].swipe("down",True)
        #
        g[59].swipe("left",True)
        g[59].swipe("down",True)
        g[59].swipe("left",True)
        #
        g[60].swipe("left",True)
        g[60].swipe("left",True)
        g[60].swipe("up",True)
        #
        g[61].swipe("left",True)
        g[61].swipe("left",True)
        g[61].swipe("right",True)
        #
        g[62].swipe("left",True)
        g[62].swipe("left",True)
        g[62].swipe("down",True)
        #
        g[63].swipe("left",True)
        g[63].swipe("left",True)
        g[63].swipe("left",True)
        
    def think(self,prompt=[]):
        if len(prompt)==3:
            if 'w' not in prompt:
                return 'w'
            if 'a' not in prompt:
                return 'a'
            if 's' not in prompt:
                return 's'
            if 'd' not in prompt:
                return 'd'
        wMean=[]
        aMean=[]
        sMean=[]
        dMean=[]
        for width in range(16):
            depth=3
            leaves=64
            w,a,s,d=[],[],[],[]
            #what is the score if we swipe in each direction and return the highest scoring direction
            direction=['up','right','down','left']
            leaf_node_values=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            g=[Game() for i in range(leaves)]
            for game in g:
                game = (game.duplicate(True))
            self.helper(g)
            
            for i in range(leaves):
                if i<16:
                    if 'w' in prompt :
                        leaf_node_values.append(0)
                    else:
                        leaf_node_values.append( g[i].getScore() )
                if i>=16 and i<32:
                    if 'd' in prompt :
                        leaf_node_values.append(0)
                    else:
                        leaf_node_values.append(g[i].getScore())
                if i>=32 and i<48:
                    if 's' in prompt :
                        leaf_node_values.append(0)
                    else:
                        leaf_node_values.append(g[i].getScore())
                if i>=48 and i<64:
                    if 'a' in prompt :
                        leaf_node_values.append(0)
                    else:
                        leaf_node_values.append(g[i].getScore())
            
            # print(leaf_node_values[0])
            # print(leaf_node_values[1:5])
            # print(leaf_node_values[5:21])
            # print("w: ",leaf_node_values[21:37])#w
            # print("d: ",leaf_node_values[37:53])#d
            # print("s: ",leaf_node_values[53:69])#s
            # print("a: ",leaf_node_values[69:85])#a
            
            # average wasd leaf nodes and use highest (expectimax)
            wMean.append(mean(leaf_node_values[21:37]))
            dMean.append(mean(leaf_node_values[37:53]))
            sMean.append(mean(leaf_node_values[53:69]))
            aMean.append(mean(leaf_node_values[69:85]))
        W=mean(wMean)
        A=mean(aMean)
        S=mean(sMean)
        D=mean(dMean)
        root_node_value=max([W,A,S,D])
        if root_node_value is W:
            return 'w'
        elif root_node_value is A:
            return 'a'
        elif root_node_value is S:
            return 's'
        else:
            return 'd'
    
#call main
if __name__ == '__main__':
    main(width,height)