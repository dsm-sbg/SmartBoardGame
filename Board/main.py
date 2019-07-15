import os
import sys
import time
import pygame
import traceback

from Character import *
from BG import *

def GetTraceBackStr():
    lines = traceback.format_exc().strip().split("\n")
    rl = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()

    for i in range(0, len(lines), 2):
        rl.append("^\t%s at %s" % (lines[i].strip(), lines[i+1].strip()))

    return '\n'.join(rl)

index = 0
nowTurn = 0
players = []

os.system("sudo ./AudioRepeat.sh BGM/Egypt_Theme.mp3 &")
pygame.init()

crashed = False
try:
    InitBackground()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type is pygame.KEYDOWN:
                print(event)

                if event.key == pygame.K_f:
                    ChangeFULL()

                if event.key == pygame.K_c:
                    ChangeCONN(False)

                if event.key == pygame.K_q:
                    crashed = True

                if event.key == pygame.K_d:
                    OpenDoor(7)
                    CloseDoor(7)
                    OpenDoor(6)
                    CloseDoor(6)

                if event.key == pygame.K_1:
                    nowTurn = 0
                    if not flag_RED:
                        flag_RED = True
                        players.append(Player(index, 1, 1, "Red"))
                        index = index + 1

                if event.key == pygame.K_2:
                    nowTurn = 1
                    if not flag_BLUE:
                        flag_BLUE = True
                        players.append(Player(index, 2, 2, "Blue"))
                        index = index + 1

                if event.key == pygame.K_3:
                    if not flag_GREEN:
                        flag_GREEN = True
                        players.append(Player(index, 0, 0, "Green"))
                        index = index + 1

                if event.key == pygame.K_4:
                    nowTurn = 3
                    if not flag_PURPLE:
                        flag_PURPLE = True
                        players.append(Player(index, 3, 2, "Purple"))
                        index = index + 1

                if event.key == pygame.K_t:
                    nowTurn = nowTurn + 1
                    nowTurn = nowTurn % 4

            elif event.type is pygame.KEYUP:
                if event.key == pygame.K_c:
                    ChangeCONN(True)

        InitBackground()
        DrawCharacter(players)
        pygame.display.update()

        for player in players:
            player.CheckTurn(nowTurn)

except Exception as e:
    print(GetTraceBackStr())

finally:
    os.system("sudo killall AudioRepeat.sh")
    os.system("sudo killall mpg123")
    os.system("sudo killall python3")
    pygame.quit()
