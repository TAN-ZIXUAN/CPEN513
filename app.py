import collections

import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path

from queue import PriorityQueue



from block import Block
import config as c


def create_grid(size_x, size_y, num_x):
    grid = []

    for i in range(num_x):
        grid.append([])
        for j in range(num_x):
            block = Block(i, j, size_x, size_y)
            grid[i].append(block)

    return grid





def draw_grid(surface,num_x, size_x, width):

    for i in range(num_x):
        pygame.draw.line(surface, c.BLACK, (0, i * size_x), (width, i * size_x))
        for j in range(num_x):
            pygame.draw.line(surface, c.BLACK, (j * size_x, 0), (j * size_x, width))
        # pygame.display.update()
    
    # pygame.draw.line(surface, c.BLACK, (0, i * size_x), (width, i * size_x))

def draw_blocks(surface, grid):
    for row in grid:
        for block in row:
            block.draw_rect(surface)


class App:
    def __init__(self):
        pygame.init()

        self.num_x = 0
        self.num_y = 0
        self.num_obs = 0 # number of obstacles
        self.size_x = 0
        self.size_y = 0

        self.num_wires = 0
        self.obs = []
        self.wire2source ={}
        self.wire2sink = collections.defaultdict(list)

        # set up window_surfce
        pygame.display.set_caption("Assignment 1 ROUTING")
        self.window_surface = pygame.display.set_mode((c.WIDTH, c.HEIGHT + 100)) 

        self.ui_manager = pygame_gui.UIManager((c.WIDTH, c.HEIGHT + 100), "Assignment1/theme.json")
        self.background = pygame.Surface((c.WIDTH, c.HEIGHT + 100))
        # self.background.fill(c.GREY)

        rect = pygame.Rect(0, 0, c.WIDTH, c.HEIGHT)
        self.subsurface = self.window_surface.subsurface(rect)
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

        # print("color", self.ui_manager.ui_theme.get_colour('dark_bg'))

        # button for loading files
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
        self.wire2colour = {}



    def run(self):

        while self.is_running:
            time_delta = self.clock.tick(60) / 100.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED  and
                    event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.ui_manager,
                                                    window_title='Load File...',
                                                    initial_file_path='Assignment 1/benchmarks/',
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

                    self.size_x = c.WIDTH / self.num_x
                    self.size_y = c.HEIGHT / self.num_y
                    self.num_obs = int(self.loaded_file[1][0])
                    for i in range(self.num_obs):
                        self.obs.append((int(self.loaded_file[2 + i][0]), int(self.loaded_file[2 + i][1])))

                    print("obs", self.obs)
                    self.num_wires = int(self.loaded_file[2 + self.num_obs][0])
                    print("num of wires", self.num_wires)
                    for i in range(self.num_wires):
                        print("wire", i)
                        print(self.loaded_file[2 + self.num_obs + 1 + i])
                        num_pins = int(self.loaded_file[2 + self.num_obs + 1 + i][0])
                        print("num of pins", num_pins)
                        self.wire2source[i] = (int(self.loaded_file[2 + self.num_obs + 1 + i][1]), int(self.loaded_file[2 + self.num_obs + 1 + i][2]))
                        c.PIN2WIRE[self.wire2source[i]] = (0, i)
                        tmp = 0 # for pairing sinks
                        for j in range(num_pins - 1):
                            (coor_x, coor_y )= (int(self.loaded_file[2 + self.num_obs + 1 + i][3 + j + tmp]), int(self.loaded_file[2 + self.num_obs + 1 + i][4 + j + tmp]))
                            self.wire2sink[i].append((coor_x, coor_y))
                            c.PIN2WIRE[(coor_x, coor_y)] = (1, i)
                            tmp += 1

                    
                    c.WIRE2SOURCE = self.wire2source
                    c.WIRE2SINK = self.wire2sink
                    
                    print("-----------------------num_x, num_y --------------------")
                    print(self.num_x, self.num_y)
                    c.NUM_X = self.num_x
                    print("--------------------------------------------------------")

                    print("-----------------------wire 2 source -------------------")
                    print(self.wire2source)
                    print("--------------------------------------------------------")

                    print("-----------------------wire 2 sink ---------------------")
                    print(self.wire2sink)
                    print("--------------------------------------------------------")

                    print("-----------------------PIN2WIRE ---------------------")
                    print(c.PIN2WIRE)
                    print("--------------------------------------------------------")

                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                    event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.file_dialog = None


                self.ui_manager.process_events(event)
            
            c.GRID = create_grid(self.size_x, self.size_y, self.num_x)

            

            for (obs_x, obs_y) in self.obs:
                c.GRID[obs_x][obs_y].is_valid = False
                c.GRID[obs_x][obs_y].mark_obs()

            

            for wire in self.wire2source:
                (source_x, source_y) = self.wire2source[wire]
                # print(x, y)
                # generate colors for each group of pins
                color_tmp = 50+wire*30
                while color_tmp > 255:
                    color_tmp -= 40
                
                self.wire2colour[wire] = (color_tmp, 100, 60)
                c.GRID[source_x][source_y].mark_source(self.wire2colour[wire])
                c.GRID[source_x][source_y].is_valid = False
                

                for (sink_x, sink_y) in self.wire2sink[wire]:
                    c.GRID[sink_x][sink_y].mark_sink(self.wire2colour[wire])

                
                
            
            
            

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            draw_blocks(self.subsurface, c.GRID)
        
            draw_grid(self.subsurface,self.num_x, self.size_x, c.WIDTH)
            # font = pygame.font.SysFont('arial', 50)
            # text = font.render("hello", True, (0, 0, 0)) # display text in a position
            # self.window_surface.blit(text, (9, 9))

            # rect = pygame.Rect(0, 0, c.WIDTH, c.HEIGHT)
            if self.loaded_file:
                src = c.WIRE2SOURCE[0]
                sink = c.WIRE2SINK[0][0]
                c.GRID[src[0]][src[1]].update_neighbours(c.GRID)
                algorithm(lambda: draw_blocks(self.subsurface, c.GRID), c.GRID, src, sink)
                draw_grid(self.subsurface,self.num_x, self.size_x, c.WIDTH)

            pygame.display.update()




    






if __name__ == "__main__":
    app = App()

    app.run()
