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
        self.is_valid = True
        self.neighbours = []
        self.cost = 0
        # self.type = "E"  # E: empty, O: obstacle, W: wire, SRC: Source, SK: Sink, SRC_R: routed source, SK_R: routed_sink


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
        self.colour = c.RED

    def is_obs(self):
        return self.colour == c.BLUE

    # def update_neighbours(self):

    def draw_rec(self, surface): # draw rectangle
        rect = pygame.Rect(self.coor_x, self.coor_y, self.size_x, self.size_y)
        pygame.draw.rec(surface, self.colour, rect)

    def isPin(self):
        return (self.row, self.col) in c.PIN2WIRE


    def isSource(self):
        return self.isPin(self.row, self.col) and c.PIN2WIRE[(self.row, self.col)][0] == 0 # is source

    def isSink(self):
        return self.isPin(self.row, self.col) and c.PIN2WIRE[(self.row, self.col)][0] == 1 # is source

    def get_wire_num(self): # get wire number for a pin
        return c.PIN2WIRE[(self.row, self.col)][1]

    def get_num_pins(self, wire): # get number of pins for a wire
        return len(c.WIRE2SOURCE[wire]) + len(c.WIRE2SINK[wire])

    def get_source(self): # get a
        pass

    #def get_block_type(self):

    def update_neighbours(self, grid):
        self.neighbors = []
        if self.row < c.NUM_X- 1 and grid[self.row + 1][self.col].is_valid: # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and grid[self.row - 1][self.col].is_valid: # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col <  c.NUM_X - 1 and grid[self.row][self.col + 1].is_valid: # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and grid[self.row][self.col - 1].is_valid: # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

