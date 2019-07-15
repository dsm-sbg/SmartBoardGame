#!/usr/bin/python3
import os
import time
import pygame

flag_RED = False
flag_BLUE = False
flag_GREEN = False
flag_PURPLE = False

LOCATION = ((600, 500, 400, 300, 200, 100),
            (100, 200, 300, 400, 500),
            (400, 300, 200, 100),
            (100, 200, 300),
            (200, 100))

DEFAULT_FLOOR = 690
DEFAULT_SQUARE = 140

UNIT_FLOOR = 150
UNIT_SQUARE = 100

LEFT = 1
RIGHT = 2

DEFAULT_PATH = "/home/pi/SmartBoardGame/Board/Source/Character/"

class Player:
    def __init__(self, Index, Square, Floor, Color):
        self.index = Index
        self.color = Color

        self.action = 1
        self.direction = 'Left'
        self.turn = False

        self.pos = [LOCATION[Floor][Square], (Floor + 1) * UNIT_FLOOR]
        self.path = [DEFAULT_PATH + "Stand/" + Color + "/N.png",
                     DEFAULT_PATH + "Run/" + Color + "/N.png"]

##          print("index: ", self.index)
##          print("square_pos: ", self.pos[0])
##          print("floor_pos: ", self.pos[1])
##          print("character_a", self.path[0])
##          print("character_u", self.path[1])

    def SetPos(self, Pos):
        self.pos[0] = LOCATION[Pos[1]][Pos[0]]
        self.pos[1] = Pos[1] * UNIT_FLOOR

    def CheckTurn(self, nowTurn):
        if self.index == nowTurn:
            self.turn = True
        else :
            self.turn = False

    def CheckDirection(self, nowFloor):
        if (nowFloor / 2) == 0:
            direction = "Left"
        else :
            direction = "Right"
