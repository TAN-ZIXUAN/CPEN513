import pygame
import config as c

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coor_x = row * c.SIZE_X
        self.coor_y = col * c.SIZE_Y
        self.colour = c.WHITE


    def get_pos(self):
        return self.row, self.col

    
