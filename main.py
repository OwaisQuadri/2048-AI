#imports
import copy
import pygame
import sys
import os
import random
import copy
import time
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
    
    def swipe(self,dir):
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
    #utility score 
    def getUtility(self):
        #combination of score, #of empty tiles, highest tile number, and if highest tile is at index 5,6,9 or 10
        util=0
        #score is score
        util+= self.getScore()-offset
        #empty tiles * highgest tile number
        util += (self.empty_spaces*max(self.board))
        middleFour=[5,6,9,10]
        maxTileIndex=self.board.index(max(self.board))
        if  maxTileIndex not in middleFour:
            #if not in middle, unincentivise by reducing utility by 75%
        util+=offset
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
        while 1:
            #every tick
            
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
                total_games,numOf_512,numOf_1024,numOf_2048,numOf_4096,numOf_8192=0,0,0,0,0,0
                if not g.recorded:
                    highest_tile=max(g.get_board())-offset
                    
                    with open('records.txt', 'r') as f:
                        f.seek(0)
                        c=0
                        for line in f:
                            if c==0:
                                for word in line.split():
                                    total_games=int(float(word))
                            elif c==1:
                                for word in line.split():
                                    numOf_512=int(float(word))
                            elif c==2:
                                for word in line.split():
                                    numOf_1024=int(float(word))
                            elif c==3:
                                for word in line.split():
                                    numOf_2048=int(float(word))
                            elif c==4:
                                for word in line.split():
                                    numOf_4096=int(float(word))
                            elif c==5:
                                for word in line.split():
                                    numOf_8192=int(float(word))
                            c+=1
                    #update with this current game
                    total_games+=1
                    if highest_tile >= 512:
                        numOf_512+=1
                    if highest_tile >= 1024:
                        numOf_1024+=1
                    if highest_tile >= 2048:
                        numOf_2048+=1
                    if highest_tile >= 4096:
                        numOf_4096+=1
                    if highest_tile >= 8192:
                        numOf_8192+=1
                    
                    #output percentages in console
                    percent_512=(numOf_512/total_games)*100
                    percent_1024=(numOf_1024/total_games)*100
                    percent_2048=(numOf_2048/total_games)*100
                    percent_4096=(numOf_4096/total_games)*100
                    percent_8192=(numOf_8192/total_games)*100
                    print('')
                    print("Number of games played: ",total_games)
                    print("")
                    print("512: ",percent_512,"%")
                    print("1024: ",percent_1024,"%")
                    print("2048: ",percent_2048,"%")
                    print("4096: ",percent_4096,"%")
                    print("8192: ",percent_8192,"%")
                    
                    with open('records.txt', 'w') as f:
                        f.write(str(total_games))
                        f.write("\n")
                        f.write(str(numOf_512))
                        f.write("\n")
                        f.write(str(numOf_1024))
                        f.write("\n")
                        f.write(str(numOf_2048))
                        f.write("\n")
                        f.write(str(numOf_4096))
                        f.write("\n")
                        f.write(str(numOf_8192))
                    g.recorded=True
                #restart game
                restart = pygame.event.Event(pygame.KEYDOWN, key=ord(" ")) #autorestart (comment out if not testing)
                pygame.event.post(restart)
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
        g[0].swipe("up")
        g[0].swipe("up")
        g[0].swipe("up")
        #
        g[1].swipe("up")
        g[1].swipe("up")
        g[1].swipe("right")
        #
        g[2].swipe("up")
        g[2].swipe("up")
        g[2].swipe("down")
        #
        g[3].swipe("up")
        g[3].swipe("up")
        g[3].swipe("left")
        #
        g[4].swipe("up")
        g[4].swipe("right")
        g[4].swipe("up")
        #
        g[5].swipe("up")
        g[5].swipe("right")
        g[5].swipe("right")
        #
        g[6].swipe("up")
        g[6].swipe("right")
        g[6].swipe("down")
        #
        g[7].swipe("up")
        g[7].swipe("right")
        g[7].swipe("left")
        #
        g[8].swipe("up")
        g[8].swipe("down")
        g[8].swipe("up")
        #
        g[9].swipe("up")
        g[9].swipe("down")
        g[9].swipe("right")
        #
        g[10].swipe("up")
        g[10].swipe("down")
        g[10].swipe("down")
        #
        g[11].swipe("up")
        g[11].swipe("down")
        g[11].swipe("left")
        #
        g[12].swipe("up")
        g[12].swipe("left")
        g[12].swipe("up")
        #
        g[13].swipe("up")
        g[13].swipe("left")
        g[13].swipe("right")
        #
        g[14].swipe("up")
        g[14].swipe("left")
        g[14].swipe("down")
        #
        g[15].swipe("up")
        g[15].swipe("left")
        g[15].swipe("left")
        #
        g[16].swipe("right")
        g[16].swipe("up")
        g[16].swipe("up")
        #
        g[17].swipe("right")
        g[17].swipe("up")
        g[17].swipe("right")
        #
        g[18].swipe("right")
        g[18].swipe("up")
        g[18].swipe("down")
        #
        g[19].swipe("right")
        g[19].swipe("up")
        g[19].swipe("left")
        #
        g[20].swipe("right")
        g[20].swipe("right")
        g[20].swipe("up")
        #
        g[21].swipe("right")
        g[21].swipe("right")
        g[21].swipe("right")
        #
        g[22].swipe("right")
        g[22].swipe("right")
        g[22].swipe("down")
        #
        g[23].swipe("right")
        g[23].swipe("right")
        g[23].swipe("left")
        #
        g[24].swipe("right")
        g[24].swipe("down")
        g[24].swipe("up")
        #
        g[25].swipe("right")
        g[25].swipe("down")
        g[25].swipe("right")
        #
        g[26].swipe("right")
        g[26].swipe("down")
        g[26].swipe("down")
        #
        g[27].swipe("right")
        g[27].swipe("down")
        g[27].swipe("left")
        #
        g[28].swipe("right")
        g[28].swipe("left")
        g[28].swipe("up")
        #
        g[29].swipe("right")
        g[29].swipe("left")
        g[29].swipe("right")
        #
        g[30].swipe("right")
        g[30].swipe("left")
        g[30].swipe("down")
        #
        g[31].swipe("right")
        g[31].swipe("left")
        g[31].swipe("left")
        #
        g[32].swipe("down")
        g[32].swipe("up")
        g[32].swipe("up")
        #
        g[33].swipe("down")
        g[33].swipe("up")
        g[33].swipe("right")
        #
        g[34].swipe("down")
        g[34].swipe("up")
        g[34].swipe("down")
        #
        g[35].swipe("down")
        g[35].swipe("up")
        g[35].swipe("left")
        #
        g[36].swipe("down")
        g[36].swipe("right")
        g[36].swipe("up")
        #
        g[37].swipe("down")
        g[37].swipe("right")
        g[37].swipe("right")
        #
        g[38].swipe("down")
        g[38].swipe("right")
        g[38].swipe("down")
        #
        g[39].swipe("down")
        g[39].swipe("right")
        g[39].swipe("left")
        #
        g[40].swipe("down")
        g[40].swipe("down")
        g[40].swipe("up")
        #
        g[41].swipe("down")
        g[41].swipe("down")
        g[41].swipe("right")
        #
        g[42].swipe("down")
        g[42].swipe("down")
        g[42].swipe("down")
        #
        g[43].swipe("down")
        g[43].swipe("down")
        g[43].swipe("left")
        #
        g[44].swipe("down")
        g[44].swipe("left")
        g[44].swipe("up")
        #
        g[45].swipe("down")
        g[45].swipe("left")
        g[45].swipe("right")
        #
        g[46].swipe("down")
        g[46].swipe("left")
        g[46].swipe("down")
        #
        g[47].swipe("down")
        g[47].swipe("left")
        g[47].swipe("left")
        #
        g[48].swipe("left")
        g[48].swipe("up")
        g[48].swipe("up")
        #
        g[49].swipe("left")
        g[49].swipe("up")
        g[49].swipe("right")
        #
        g[50].swipe("left")
        g[50].swipe("up")
        g[50].swipe("down")
        #
        g[51].swipe("left")
        g[51].swipe("up")
        g[51].swipe("left")
        #
        g[52].swipe("left")
        g[52].swipe("right")
        g[52].swipe("up")
        #
        g[53].swipe("left")
        g[53].swipe("right")
        g[53].swipe("right")
        #
        g[54].swipe("left")
        g[54].swipe("right")
        g[54].swipe("down")
        #
        g[55].swipe("left")
        g[55].swipe("right")
        g[55].swipe("left")
        #
        g[56].swipe("left")
        g[56].swipe("down")
        g[56].swipe("up")
        #
        g[57].swipe("left")
        g[57].swipe("down")
        g[57].swipe("right")
        #
        g[58].swipe("left")
        g[58].swipe("down")
        g[58].swipe("down")
        #
        g[59].swipe("left")
        g[59].swipe("down")
        g[59].swipe("left")
        #
        g[60].swipe("left")
        g[60].swipe("left")
        g[60].swipe("up")
        #
        g[61].swipe("left")
        g[61].swipe("left")
        g[61].swipe("right")
        #
        g[62].swipe("left")
        g[62].swipe("left")
        g[62].swipe("down")
        #
        g[63].swipe("left")
        g[63].swipe("left")
        g[63].swipe("left")
        
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
        for width in range(1):
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
                        utility=g[i].getUtility()
                        
                        leaf_node_values.append( utility )
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
            
            # average wasd leaf nodes and use highest
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
            # leaf_index=leaf_node_values.index(root_node_value,21)
            # # print(root_node_value," at ",leaf_index)
            # if leaf_index >=21 and leaf_index < 37:
            #     output.append('w')
            # if leaf_index >=37 and leaf_index < 53:
            #     output.append('d')
            # if leaf_index >=53 and leaf_index < 69:
            #     output.append('s')
            # if leaf_index >=69 and leaf_index <= 85:
            #     output.append('a')
        
        # out=random.choice(output)
        # # print("out: ",output)
        # return out
    
#call main
if __name__ == '__main__':
    main(width,height)