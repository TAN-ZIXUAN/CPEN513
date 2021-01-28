import pygame
import pygame_gui
from pygame_gui.elements import UI_BUTTON
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path

import math
from queue import PriorityQueue


WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Assignment 1")

# define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
