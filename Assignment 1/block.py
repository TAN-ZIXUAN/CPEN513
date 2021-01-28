import numpy as np
import pygame
import config as c


class Block:
    def __init__(self, row, col, size_x, size_y):
        self.row = row
        self.col = col
        self.size_x = size_x
        self.size_y = size_y

        self.coor_x = row * size_x
        self.coor_y = col * size_y



        self.colour = c.GREY


    def get_pos(self):
        return self.row, self.col

    def draw_rect(self, surface): # draw rectangle
        rect = pygame.Rect(self.coor_x, self.coor_y, self.size_x, self.size_y)
        pygame.draw.rect(surface, self.colour, rect)

    
    # TODO how to scale text perfectly to fit into a block?
    def draw_text(self, text):
        text_font = pygame.font.SysFont(None, 12)
        text_image = text_font.render(text, True, c.BLACK. c.WHITE)

    def mark_source(self, colour):
        self.colour = colour
        

    def mark_sink(self, colour):
        self.colour = colour

    def mark_obs(self): # mark obstacle with colour BLUE
        self.colour = c.BLACK

    def mark_path(self):
        self.colour = c.PURPLE

    
    def is_source(self):
        return self.colour == c.ORANGE

    def is_sink(self):
        return self.colour == c.GREEN

    def is_obs(self):
        return self.colour == c.BLUE

    # def update_neighbours(self):