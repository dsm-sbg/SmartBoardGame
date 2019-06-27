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
players = []

os.system("sudo ./AudioRepeat.sh BGM/Egypt_Theme.mp3 &")

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



                if event.key == pygame.K_3:
                    if not flag_GREEN:
                        players.append(player(index, 981, 100, "Green"))
                        index = index + 1
                        flag_GREEN = True

                if event.key == pygame.K_1:
                    if not flag_RED:
                        flag_RED = True
                        index = index + 1
                        players.append(player(index, 981, 100, "Red"))

                if event.key == pygame.K_2:
                    if not flag_BLUE:
                        flag_BLUE = True
                        index = index + 1
                        players.append(player(index, 981, 100, "Blue"))

                if event.key == pygame.K_4:
                    if not flag_PURPLE:
                        flag_PURPLE = True
                        index = index + 1
                        players.append(player(index, 981, 100, "Purple"))



            elif event.type is pygame.KEYUP:
                if event.key == pygame.K_c:
                    ChangeCONN(True)

        if Changed():
            print("Changed")
            DrawBackground()
            DrawDoor()
            pygame.display.update()

except Exception as e:
    print(GetTraceBackStr())

finally:
    os.system("sudo killall AudioRepeat.sh")
    os.system("sudo killall mpg123")
    os.system("sudo killall python3")
    pygame.quit()

