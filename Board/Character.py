#!/usr/bin/python3
import os
import time
import pygame

flag_RED = False
flag_BLUE = False
flag_GREEN = False
flag_PURPLE = False

Block_x  =  ((1032, 898, 764, 630, 494, 360, 226, 99),
            (222, 352, 491, 630, 767, 973),
            (841, 630, 498, 354),
            (495, 700),
            (579))
Block_y  =  (85, 218, 351, 484, 617)

LEFT = 1
RIGHT = 2

DEFAULT_PATH = "/home/pi/SmartBoardGame/Board/Source/Character/"

class Player:
    def __init__(self, Index, Color):
        self.index = Index
        self.color = Color

        self.action = 1
        self.direction = 'Left'
        self.turn = False

        self.now_pos = [Block_x[0][0] + (self.index * 35), Block_y[4]]
        self.dst_pos = self.now_pos
        self.path = [DEFAULT_PATH + "Stand/" + Color + "/N.png",
                     DEFAULT_PATH + "Run/" + Color + "/N.png"]

        print("index: ", self.index)
        print("now_pos: ", self.now_pos)
        print("dst_pos: ", self.dst_pos)
        print("character_a", self.path[0])
        print("character_u", self.path[1])

        def SetNowPos(self, x, y):
            self.now_pos[0] = x
            self.now_pos[1] = y

        def SetDstPos(self, square, floor):
            self.dst_pos[0] = Block_x[floor][suqare] + (self.index * 35)
            self.dst_pos[1] = Block_y[floor]

    def CheckTurn(self, nowTurn):
        if self.index == nowTurn:
            self.turn = True
        else :
            self.turn = False

    def ChangeDirection(self):
        if self.direction == "Left":
            self.direction = "Right"
        else:
            direction = "Left"
