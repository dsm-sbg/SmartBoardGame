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
    color = str()
    path = [str(), str()]

    pos = [0, 0]
    action = 1

    direction = "Left"
    index = int()
    turn = False

    def __init__(self, Index, Square, Floor, Color):
        self.index = Index
        self.color = Color
        self.pos[0] = LOCATION[Floor][Square]
        self.pos[1] = Floor * UNIT_FLOOR
        self.path[0] = DEFAULT_PATH + "Stand/" + Color + "/N.png"
        self.path[1] = DEFAULT_PATH + "Run/" + Color + "/N.png"

        print("index: ", self.index)
        print("square_pos: ", self.pos[0])
        print("floor_pos: ", self.pos[1])
        print("character_a", self.path[0])
        print("character_u", self.path[1])

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
