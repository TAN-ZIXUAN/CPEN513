import pygame
import config as c

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coor_x = row * c.SIZE_X
        self.coor_y = col * c.SIZE_Y
        self.colour = c.WHITE

        self.neighbours = []

        # node type
        # e: empty
        # o: obstacle
        # w: wire
        # src: source
        # sink: sink
        # r: routed sink/source
        self.type = "e"

    def is_pin(self):
        return self.is_source() or self.is_sink()

    def is_source(self):
        return (self.row, self.col) in c.SOURCES
    def is_sink(self):
        return (self.row, self.col) in c.SINKS
    def is_obs(self): # is obstacles
        return (self.row, self.col) in c.OBS
    def can_pass(self, source): # whether we can wire on this node 
        if self.type == "e":
            return True
        elif self.type == "sink": # if it's sink, it has to be the source's sink
            return (self.row, self.col) in c.SOURCE2SINKS[source]
        return False
    
    
    # def is_routed check whether is in the path

    def mark_routed(self):
        self.type = "r"

    def get_neighbours(self): # get valid neighbour for curr_node
        self.neighbours = [] # valid neighbours: sink or empty node

        if self.row < c.NUM_X - 1 and c.GRID[self.row + 1][self.col].can_pass(): # DOWN
            self.neighbours.append(c.GRID[self.row + 1][self.col])
        if self.row > 0 and c.GRID[self.row - 1][self.col].can_pass(): # UP
            self.neighbours.append(gc.GRID[self.row - 1][self.col])
        if self.col <  c.NUM_X - 1 and c.GRID[self.row][self.col + 1].can_pass(): # RIGHT
            self.neighbours.append(c.GRID[self.row][self.col + 1])

        if self.col > 0 and c.GRID[self.row][self.col - 1].can_pass(): # LEFT
            self.neighbours.append(c.GRID[self.row][self.col - 1])





