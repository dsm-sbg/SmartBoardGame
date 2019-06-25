import os
import sys
import time
import pygame

flag_FULL = False; pre_flag_FULL = False
flag_CONN = False; pre_flag_FULL = False
flag_TURN = 1; pre_flag_FULL = 1

backgroundSize = (1280, 720)

gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
pygame.display.set_caption('SMART BOARD GAME')

Door_Path = "/home/pi/SmartBoardGame/Board/Source/Open_Door/"
Door_Squares = [587, 708, 503, 362, 849, 981, 230, 107]

Door_Floors = [90, 223, 223, 356, 356, 489, 489, 622]

def InitBackground():
    pygame.init()

    DrawBackground()
    time.sleep(1)

    DrawDoor()
    time.sleep(1)

def Changed():
    res = 0

    global flag_FULL
    global flag_CONN
    global flag_TURN

    global pre_flag_FULL
    global pre_flag_CONN
    global pre_flag_TURN

    if pre_flag_FULL != flag_FULL :
        res = 1
    elif pre_flag_CONN != flag_CONN :
        res = 1
    elif pre_flag_TURN != flag_TURN :
        res = 1

    pre_flag_FULL = flag_FULL
    pre_flag_CONN = flag_CONN
    pre_flag_TURN = flag_TURN

    return res

def DrawCharacter(source):
    character_u = GIFImage(charictor_u_path)
    character_a = GIFImage(charictor_a_path)

    character_u.render(gamedisplay, (100, 100))
    character_u.render(gamedisplay, (300, 300))

def DrawDoor():
    for i in range(0, 8):
        gameDisplay.blit(pygame.image.load(Door_Path + "Open_Door1.png"), (Door_Squares[i], Door_Floors[i]))

def DrawBackground():
    gameDisplay.blit(pygame.image.load("./BG.png"),(0,0))

    if not flag_CONN:
        gameDisplay.blit(pygame.image.load("./Connect Failed.png"), (30, 5))

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
