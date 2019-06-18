import os
import time
import pygame
import signal

pid = os.fork()

if (pid == 0):
    os.system("sudo ./AudioRepeat.sh Egypt_Theme.mp3")

else:
    bgSize = (1280, 720)

    flag_FULL = 0; pre_flag_FULL = 0
    flag_CONN = 0; pre_flag_FULL = 0
    flag_TURN = 1; pre_flag_FULL = 1

    pygame.init()

    gameDisplay = pygame.display.set_mode(bgSize, pygame.DOUBLEBUF)
    pygame.display.set_caption('SMART BOARD GAME')

    crashed = False

    door_path = "./Source/Door_Open/"

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

    def Gate():
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(587,90))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(503,223))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(708,223))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(362,356))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(849,356))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(230,489))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(981,489))
            gameDisplay.blit(pygame.image.load(door_path + "Door_Open1.png"),(107,622))

            if not flag_CONN:
                gameDisplay.blit(pygame.image.load("./Connect Failed.png"), (30, 5))

            if(Changed()):
                pygame.display.update()


    def Draw_image():
        gameDisplay.blit(pygame.image.load("./BG.png"),(0,0))

    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type is pygame.KEYDOWN and event.key == pygame.K_f:
                if flag_FULL == 1:
                    gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    flag_FULL = 0
                else:
                    gameDisplay = pygame.display.set_mode(bgSize, pygame.DOUBLEBUF)
                    flag_FULL = 1

            if event.type is pygame.KEYDOWN and event.key == pygame.K_c:
                flag_CONN = 0
            elif event.type is pygame.KEYUP and event.key == pygame.K_c:
                flag_CONN = 1

            if event.type is pygame.KEYDOWN and event.key == pygame.K_q:
                os.system("sudo killall AudioRepeat.sh")
                os.system("sudo killall mpg123")
                os.system("sudo killall python3")

            print(event)

        Draw_image()
        Gate()
        pygame.display.update()

    pygame.quit()
