import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path

import config as c
from functions import *
import algorithms as alg

class App:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption("Assignment 1 ROUTING")
        self.window_surface = pygame.display.set_mode((c.WIDTH, c.HEIGHT + 100))
        self.ui_manager = pygame_gui.UIManager((c.WIDTH, c.HEIGHT + 100), "Assignment 1/theme.json")
        self.background = pygame.Surface((c.WIDTH, c.HEIGHT + 100))
        rect = pygame.Rect(0, 0, c.WIDTH, c.HEIGHT)
        self.subsurface = self.window_surface.subsurface(rect) # subsurface for maze
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))



        #load button
        self.load_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                    text='Load File',
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'})


        self.file_dialog = None
        self.loaded_file = []
        self.clock = pygame.time.Clock()
        self.is_running = True


    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                # set filedialog
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED  and
                    event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.ui_manager,
                                                    window_title='Load File...',
                                                    initial_file_path='Assignment 1/benchmarks/',
                                                    allow_existing_files_only=True)
                    self.load_button.disable()

                # loading file
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED):
                    if self.loaded_file is not None:
                        self.loaded_file = []


                    file_path = create_resource_path(event.text)
                    with open(file_path, 'r') as file:
                        for line in file.readlines():
                            self.loaded_file.append((line.strip().split())) # [['40', '20'], ['101'], ['25', '1'], ['26', '1'], ['27', '1']

                    # parse file
                    parse_file(self.loaded_file)
                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                    event.ui_element == self.file_dialog and
                    not self.loaded_file):
                    self.load_button.enable()
                    self.file_dialog = None
                
                if self.loaded_file: self.load_button.disable()

                self.ui_manager.process_events(event)
                # create grid (matrix made by node)
            c.GRID = create_grid(c.NUM_X, c.NUM_Y)
            # update grid colour based on loaed file
            update_grid_colour(c.GRID)
            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            # draw maze
            if self.loaded_file:
                # print("sources", c.SOURCES)
                paint_nodes(self.subsurface, c.GRID)
                draw_grid(self.subsurface, c.NUM_X, c.SIZE_X) # draw nodes first bc node will cover the grid the boarderlines
                source= c.SOURCES[0]
                # draw = lamda: draw(self.subsurface, c.GRID, c.NUM_X, c.SIZE_X)
                alg.a_star(lambda:draw(self.subsurface, c.GRID, c.NUM_X, c.SIZE_X), c.GRID, source, c.SOURCE2SINKS[source][0])

            pygame.display.update()



if __name__ == "__main__":
    app = App()

    app.run()
