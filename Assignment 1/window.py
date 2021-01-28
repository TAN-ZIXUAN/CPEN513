import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path

import config as c
import Block

WIDTH = 1000
HEIGHT = 500

#colors
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

class Window:
    def __init__(self, row, col):
        pygame.init()

        self.row = row
        self.col = col
        self.colour = WHITE
        # self.x = row * width
        # self.y = col * width
        # self.colour = WHITE
        # self.width = width
        # self.height = height
        # self.total_rows = total_rows
        self.neighbours = []
        # self.sources = []
        # self.sinks = []
        self.num_x = 0
        self.num_y = 0
        self.num_obs = 0 # number of obstacles
        self.obs = []
        self.num_wires = 0
        self.wire2source ={}
        self.wire2sink = {}

        self.size_x = 0
        self.size_y = 0

        self.x = 0
        self.y = 0



        pygame.display.set_caption("Assignment 1 ROUTING")
        self.window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), "theme.json")
        self.background = pygame.Surface((WIDTH, WIDTH))
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

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

    def get_pos(self):
        return self.row, self.col

    def make_grid(self, num_x, num_y, size_x, size_y):
        grid = []
        for i in range(num_x):
            grid.append([])
            for j in range(num_y):
                




    def make_source(self):
        self.colour = ORANGE
    
    def make_sink(self):
        self.colour = GREEN

    def make_obstacle(self):
        self.colour = BLUE
    def make_path(self):
        self.colour = PURPLE
    def draw_rec(self, surface): # draw rectangle
        rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        pygame.draw.rec(surface, self.colour, rect)

    # def update_neighbours(self, grid):
    #     self.neighbours = []





    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED  and
                    event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.ui_manager,
                                                    window_title='Load File...',
                                                    initial_file_path='benchmarks/',
                                                    allow_existing_files_only=True)
                    self.load_button.disable()

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED):
                    if self.loaded_file is not None:
                        self.loaded_file = []

                    file_path = create_resource_path(event.text)
                    with open(file_path, 'r') as file:
                        for line in file.readlines():
                            self.loaded_file.append((line.strip().split())) # [['40', '20'], ['101'], ['25', '1'], ['26', '1'], ['27', '1']
                    print("-----------------------file loaded ---------------------")
                    print(self.loaded_file)
                    print("--------------------------------------------------------")
                    # TODO add label to display selected file name in window

                    self.num_x, self.num_y = int(self.loaded_file[0][0]), int(self.loaded_file[0][1])
                    self.num_obs = int(self.loaded_file[1][0])
                    for i in range(self.num_obs):
                        self.obs.append((int(self.loaded_file[2 + i][0]), int(self.loaded_file[2 + i][1])))

                    self.num_wires = int(self.loaded_file[2 + self.num_obs][0])
                    print("num of wires", self.num_wires)
                    for i in range(self.num_wires):
                        print("wire", i)
                        print(self.loaded_file[2 + self.num_obs + 1 + i])
                        num_pins = int(self.loaded_file[2 + self.num_obs + 1 + i][0])
                        print("num of pins", num_pins)
                        self.wire2source[i] = (int(self.loaded_file[2 + self.num_obs + 1 + i][1]), int(self.loaded_file[2 + self.num_obs + 1 + i][2]))

                        for j in range(num_pins - 1):
                            self.wire2sink[i] = (int(self.loaded_file[2 + self.num_obs + 1 + i][3 + j]), int(self.loaded_file[2 + self.num_obs + 1 + i][4 + j]))


                    print("-----------------------num_x, num_y --------------------")
                    print(self.num_x, self.num_y)
                    print("--------------------------------------------------------")

                    print("-----------------------wire 2 source -------------------")
                    print(self.wire2source)
                    print("--------------------------------------------------------")

                    print("-----------------------wire 2 sink ---------------------")
                    print(self.wire2sink)
                    print("--------------------------------------------------------")

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                    event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.file_dialog = None


                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            # font = pygame.font.SysFont('arial', 50)
            # text = font.render("hello", True, (0, 0, 0)) # display text in a position
            # self.window_surface.blit(text, (9, 9))

            pygame.display.update()

        self.size_x = WIDTH / self.num_x
        self.size_y = HEIGHT / self.num_y
        self.x = self.row * self.size_x
        self.y = self.col * self.size_y


if __name__ == "__main__":
    app = Window(10, 10)

    app.run()
