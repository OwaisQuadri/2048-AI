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
    #high score
    with open('highScore.txt', 'r') as f:
        f.seek(0)
        highScore=(int(float(f.read())))
    score=0
    isGameOver=False
    moved=False
    board=[0 for i in range(16)]
    def __init__(self):
        self.board=[0 for i in range(16)]
        self.addTile()
        self.addTile()
        self.score=0
        self.isGameOver=False
    def prnt(self):
        for x in range(0,4):
                print(self.board[4*x],self.board[4*x+1],self.board[4*x+2],self.board[4*x+3])
    def restart(self):
        self.__init__()
    def addTile(self):
        mt=[]
        curr=0
        for sq in self.board:
            if sq == 0:
                mt.append(curr)
            curr+=1
        if len(mt) != 0:
            index=random.choice(mt)
            
            self.board[index]=random.choice([2,4])
        else:
            #partly game over (game is over when there are no more possible moves) 
            print("GameOver!")
    #movement
    def swipe(self,dir):
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
                    if self.board[index] != 0:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=self.board[index]#add current to latest entry in L
                                #add points
                                self.score+=self.board[index]
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
                        B[i_col+out]=0
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
                    if self.board[index] != 0:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=self.board[index]#add current to latest entry in L
                                #add points
                                self.score+=self.board[index]
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
                        B[i_col+out]=0
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
                    if self.board[index] != 0:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=self.board[index]#add current to latest entry in L
                                #add points
                                self.score+=self.board[index]
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
                        B[i_row*4+out]=0
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
                    if self.board[index] != 0:#if not zero
                        if (len(L) <1) or (joined==True):#if size <= 1,
                            L.append(self.board[index])#joined = false and append to blank list L
                            joined=False
                        else:#if size > 1, and joined == False
                            if self.board[index] == L[len(L)-1] :#if current is equal to latest entry in L
                                L[len(L)-1]+=self.board[index]#add current to latest entry in L
                                #add points
                                self.score+=self.board[index]
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
                        B[i_row*4+out]=0
                    out+=1
        else:
            #else do something i guess
            print("else")
        #update score
        if self.score > self.highScore:
            self.highScore=self.score
            with open('highScore.txt', 'w') as f:
                f.write(str(self.highScore))
        #once the loop completes, outside all the if/elif/else statements:
        # do g.setBoard with B, which is the overall board list
        self.set_board(B,b4)
    
    #board getter setter
    def get_board(self):
        return self.board
    def set_board(self,b,b4):
            if b == b4:
                self.moved=False
            else:
                self.board = b 
                self.moved=True
    #gameover setter getter
    def setGameOver(self, xyz):
        self.isGameOver=xyz
    def getGameOver(self):
        #function to check if game is over
        #if game is over cover game with translucent screen that says "press 'SPC' to try again"
        #if there are no more empty slots and none of the same numbers next to one another, game is over
        #first loop through entire array once and check for no zeros
            #if any zeros, return with no action
        #else loop through rows to check for adgacent same numbers
            #if any, return with no action
        #else loop through cols to check for adgacent same numbers
            #if any, return with no action    
        return self.isGameOver
    #moved setter getter
    def setMoved(self, xyz):
        self.moved=xyz
    def getMoved(self):
        return self.moved
    #score getter and maybe setter if needed
    def getScore(self):
        return self.score
    #get highscore
    def getHighScore(self):
        return self.highScore
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
            # render title
            label = TitleFont.render("2048", 1, FONT_8PLUS)
            screen.blit(label, (360, 50))
            #render score
            score = inGameFont.render(("Score: "+str(g.getScore())),1,FONT_24)
            screen.blit(score,(200,550))
            #highscore
            highscoredisplay = inGameFont.render(("High Score: "+str(g.getHighScore())),1,FONT_24)
            screen.blit(highscoredisplay,(200,575))
            
            # keyboard handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('w'):
                        g.swipe("up")
                        if (g.getMoved()):
                            g.addTile()
                        else:
                            g.getGameOver()
                    if event.key == ord('s'):
                        g.swipe("down")
                        if (g.getMoved()):
                            g.addTile()
                        else:
                            g.getGameOver()
                    if event.key == ord('d'):
                        g.swipe("right")
                        if (g.getMoved()):
                            g.addTile()
                        else:
                            g.getGameOver()
                    if event.key == ord('a'):
                        g.swipe("left")
                        if (g.getMoved()):
                            g.addTile()
                        else:
                            g.getGameOver()
                    if event.key == ord(' '):
                        g.restart()
                # if event.type == pygame.KEYUP:
                #     if event.key == ord('w'):
                #     if event.key == ord('s'):
                #     if event.key == ord('d'):
                #     if event.key == ord('a'):
                #     if event.key == ord(' '):
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    exit(0)
                #update
                pygame.display.flip()
#call main
if __name__ == '__main__':
    main(width,height)