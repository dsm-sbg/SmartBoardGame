import os
import sys
import time
import pygame

flag_FULL = False; pre_flag_FULL = False
flag_CONN = False; pre_flag_CONN = False
flag_TURN = 1; pre_flag_TURN = 1
flag_DOOR = 0; pre_flag_DOOR = 0

backgroundSize = (1280, 720)
frame = 1
i = 0

gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
pygame.display.set_caption('SMART BOARD GAME')

Default_Path = "/home/pi/SmartBoardGame/Board/Source/"
Door_Path = Default_Path + "Open_Door/"

Door_Squares = [587, 708, 503, 362, 849, 981, 230, 107]
Door_Floors = [90, 223, 223, 356, 356, 489, 489, 622]

def InitBackground():
    DrawBackground()
    DrawDoor()

def Changed():
    res = 0

    global flag_FULL
    global flag_CONN
    global flag_TURN

    global pre_flag_FULL
    global pre_flag_CONN
    global pre_flag_TURN

    if pre_flag_FULL != flag_FULL:
        res = 1
    elif pre_flag_CONN != flag_CONN:
        res = 1
    elif pre_flag_TURN != flag_TURN:
        res = 1

    pre_flag_FULL = flag_FULL
    pre_flag_CONN = flag_CONN
    pre_flag_TURN = flag_TURN

    return res

def SetDoor(door):
    global flag_DOOR

    flag_DOOR = door

def Frame(players):
    global flag_DOOR
    global pre_flag_DOOR
    global frame

    global i

    print("flag_DOOR: ", flag_DOOR)
    print("pre_flag_DOOR: ", pre_flag_DOOR)

    DrawBackground()
    DrawDoor()

    if flag_DOOR != 0:
        if flag_DOOR != pre_flag_DOOR:
            if flag_DOOR < 0:
                i = 7
            elif flag_DOOR > 0:
                i = 1
            pre_flag_DOOR = flag_DOOR

        gameDisplay.blit(pygame.image.load(Door_Path + str(i) +".png"),(Door_Squares[(abs(flag_DOOR) - 1) * 2], Door_Floors[(abs(flag_DOOR) - 1) * 2]))
        gameDisplay.blit(pygame.image.load(Door_Path + str(i) +".png"),(Door_Squares[(abs(flag_DOOR) - 1) * 2 + 1], Door_Floors[(abs(flag_DOOR) - 1) * 2 + 1]))

        if flag_DOOR < 0:
            i = i - 1
            if i == 0:
                flag_DOOR = 0
        elif flag_DOOR > 0:
            i = i + 1
            if i == 8:
                flag_DOOR = 0

    for player in players:
        action = player.action
        if player.turn == True:
            path = player.path[1].replace('N', player.direction + str(action))
        else:
            path = player.path[0].replace('N', str(action))
        gameDisplay.blit(pygame.image.load(path), tuple(player.pos))
        player.action = (player.action % 8) + 1

    if not flag_CONN:
        gameDisplay.blit(pygame.image.load(Default_Path + "Connect Failed.png"), (30, 5))

    frame = frame + 1
    time.sleep(0.003)
def DrawDoor():
    for i in range(0, 8):
        gameDisplay.blit(pygame.image.load(Door_Path + "1.png"), (Door_Squares[i], Door_Floors[i]))

def DrawBackground():
    gameDisplay.blit(pygame.image.load(Default_Path + "BG.png"),(0,0))

def OpenDoor(num):
    os.system("mpg123 -q " + Default_Path + "BGM/Open_Door.mp3 &")

    for i in range(1, 8):
        gameDisplay.blit(pygame.image.load(Door_Path + "Open_Door"+ str(i)  +".png"),(Door_Squares[num], Door_Floors[num]))
        time.sleep(0.1)
        pygame.display.update()

def CloseDoor(num):
    os.system("mpg123 -q " + Default_Path + "BGM/Close_Door.mp3 &")
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
