import os
import sys
import time
import pygame
import traceback
import subprocess

from Character import *
from BG import *

turn = 0
index = 0
nowTurn = 0

players = []

os.system("sudo ./AudioRepeat.sh BGM/Egypt_Theme.mp3 &")
pygame.init()

crashed = False

def GetDice(turn):
    subprocess.run(['python3', "RF.py", str(turn)])

    f = open("result", 'r')
    result = f.readlines()
    print(result)
    while int(result[0]) != turn:
        time.sleep(0.001)

    return result

def GetTraceBackStr():
    lines = traceback.format_exc().strip().split("\n")
    rl = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()

    for i in range(0, len(lines), 2):
        rl.append("^\t%s at %s" % (lines[i].strip(), lines[i+1].strip()))

    return '\n'.join(rl)

try:
    InitBackground()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type is pygame.KEYDOWN:

                if event.key == pygame.K_f:
                    ChangeFULL()

                if event.key == pygame.K_c:
                    ChangeCONN(False)

                if event.key == pygame.K_q:
                    crashed = True

                if event.key == pygame.K_d:
                    flag_DOOR = ((flag_DOOR % 4) + 1) * -1
                    SetDoor(flag_DOOR)

                if event.key == pygame.K_1:
                    if not flag_RED:
                        flag_RED = True
                        players.append(Player(index, "Red"))
                        index = index + 1

                if event.key == pygame.K_2:
                    if not flag_BLUE:
                        flag_BLUE = True
                        players.append(Player(index, "Blue"))
                        index = index + 1

                if event.key == pygame.K_3:
                    if not flag_GREEN:
                        flag_GREEN = True
                        players.append(Player(index, "Green"))
                        index = index + 1

                if event.key == pygame.K_4:
                    if not flag_PURPLE:
                        flag_PURPLE = True
                        players.append(Player(index, "Purple"))
                        index = index + 1

                if event.key == pygame.K_t:
                    if index != 0:
                        nowTurn = nowTurn + 1
                        nowTurn = nowTurn % (index)

            elif event.type is pygame.KEYUP:
                if event.key == pygame.K_c:
                    ChangeCONN(True)

        Frame(players)
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
