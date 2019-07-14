import os
import sys
import time
import pygame

flag_FULL = False; pre_flag_FULL = False
flag_CONN = False; pre_flag_CONN = False
flag_TURN = 1; pre_flag_TURN = 1

backgroundSize = (1280, 720)

gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
pygame.display.set_caption('SMART BOARD GAME')

Door_Path = "/home/pi/SmartBoardGame/Board/Source/Open_Door/"

Door_Squares = [587, 708, 503, 362, 849, 981, 230, 107]
Door_Floors = [90, 223, 223, 356, 356, 489, 489, 622]

def InitBackground():
    DrawBackground()
    DrawDoor()

##  def Changed():
##      res = 0
##  
##      global flag_FULL
##      global flag_CONN
##      global flag_TURN
##      global flag_C_ORDER
##  
##      global pre_flag_FULL
##      global pre_flag_CONN
##      global pre_flag_TURN
##      global pre_flag_C_ORDER
##  
##      if pre_flag_FULL != flag_FULL:
##          res = 1
##      elif pre_flag_CONN != flag_CONN:
##          res = 1
##      elif pre_flag_TURN != flag_TURN:
##          res = 1
##      elif pre_flag_ORDER != flag_ORDER:
##          res = 1
##  
##      pre_flag_FULL = flag_FULL
##      pre_flag_CONN = flag_CONN
##      pre_flag_TURN = flag_TURN
##      pre_flag_ORDER = flag_ORDER
##  
##      return res

def DrawCharacter(players):
    for player in players:
        if player.turn == True:
            path = player.path[1].replace('N', player.direction + str(player.action))
        else:
            path = player.path[0].replace('N', str(player.action))

        gameDisplay.blit(pygame.image.load(path), tuple(player.pos))
        print("Color: {}/Pos: {}".format(player.color, player.pos))

def DrawDoor():
    for i in range(0, 8):
        gameDisplay.blit(pygame.image.load(Door_Path + "Open_Door1.png"), (Door_Squares[i], Door_Floors[i]))

def DrawBackground():
    gameDisplay.blit(pygame.image.load("./Source/BG.png"),(0,0))

    if not flag_CONN:
        gameDisplay.blit(pygame.image.load("./Source/Connect Failed.png"), (30, 5))

def OpenDoor(num):
    os.system("mpg123 -q BGM/Close_Door.mp3 &")

    for i in range(1, 8):
        gameDisplay.blit(pygame.image.load(Door_Path + "Open_Door"+ str(i)  +".png"),(Door_Squares[num], Door_Floors[num]))
        time.sleep(0.1)
        pygame.display.update()

def CloseDoor(num):
    os.system("mpg123 -q BGM/Close_Door.mp3 &")
    for i in range(7, 0, -1):
        gameDisplay.blit(pygame.image.load(Door_Path + "Open_Door"+ str(i)  +".png"),(Door_Squares[num], Door_Floors[num]))
        time.sleep(0.1)
        pygame.display.update()

def ChangeFULL():
    global flag_FULL

    if flag_FULL == 1:
        gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        flag_FULL = 0
    else:
        gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
        flag_FULL = 1

def ChangeCONN(status):
    global flag_CONN

    if status == True:
        flag_CONN = 1
    else:
        flag_CONN = 0
