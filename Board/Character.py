#!/usr/bin/python3
import os
import time
import pygame

flag_RED = False
flag_BLUE = False
flag_GREEN = False
flag_PURPLE = False

LOCATION = [[600, 500, 400, 300, 200, 100]
            [100, 200, 300, 400, 500]
            [400, 300, 200, 100]
            [100, 200, 300]
            [200, 100]]

DEFAULT_FLOOR = 690
DEFAULT_SQUARE = 140

UNIT_FLOOR = 150
UNIT_SQUARE = 100

LEFT = 1
RIGHT = 2

DEFAULT_PATH = "/home/pi/SmartBoardGame/Board/Source/Character/"

class Player:
    path = [str(), str()]

    pos = [0, 0]

    direction = LEFT
    index = int()
    turn = False

    def __init__(self, index, square, floor, Color):
        self.index = index
        self.pos[0] = LOCATION[floor][square]
        self.pos[1] = floor * UNIT_FLOOR
        self.path[0] = DEFAULT_PATH + "Default_N.png"
        self.path[1] = DEFAULT_PATH + "Default_N.png"

        print("index: ", self.index)
        print("square_pos: ", self.pos[0])
        print("floor_pos: ", self.pos[1])
        print("character_a", self.path[0])
        print("character_u", self.path[1])

    def SetPos(self, pos):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]

    def CheckTurn(self, nowTurn):
        if self.index == nowTurn:
            self.turn = True
        else :
            self.turn = False

    def CheckDirection(self, nowFloor):
        if (nowFloor / 2) == 0:
            direction = LEFT
        else :
            direction = RIGHT
