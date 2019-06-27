#!/usr/bin/python3

import os
import time
import pygame

flag_RED = False
flag_BLUE = False
flag_GREEN = False
flag_PURPLE = False

DEFAULT_FLOOR = 690
DEFAULT_SQUARE = 140

UNIT_FLOOR = 150
UNIT_SQUARE = 100

DEFAULT_PATH = "/home/pi/SmartBoardGame/Board/Source/Character/"

class player:
    character_a = pygame.image.load("Default.png")
    character_u = pygame.image.load("Default.png")

    square_pos = int()
    floor_pos = int()
    index = int()
    turn = False

    def __init__(self, index, square, floor, Color):
        self.index = index
        self.square_pos = square
        self.floor_pos = floor
        self.character_a = pygame.image.load(DEFAULT_PATH + "Character_{0}_A.png".format(Color))
        self.character_u = pygame.image.load(DEFAULT_PATH + "Character_{0}_U.png".format(Color))

        print("index: ", self.index)
        print("square_pos: ", self.square_pos)
        print("floor_pos: ", self.floor_pos)
        print("character_a", self.character_a)
        print("character_u", self.character_u)

    def CheckTurn(nowTurn):
        if this.index == nowTurn:
            turn = 1
        else :
            turn = 0
