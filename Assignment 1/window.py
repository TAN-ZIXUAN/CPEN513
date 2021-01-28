import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path

WIDTH = 800
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
    def __init__(self, row, col, width, total_rows):
        pygame.init()
        
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []

        

        pygame.display.set_caption("Assignment 1")
        self.window_surface = pygame.display.set_mode((WIDTH, WIDTH))
        self.ui_manager = pygame_gui.UIManager((WIDTH, WIDTH), "theme.json")
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

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        

    

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
                            self.loaded_file.append(line.strip())
                    print("-----------------------file loaded ---------------------")
                    print(self.loaded_file)
                    print("--------------------------------------------------------")
                    # TODO add label display selected file name in window


                if (event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_WINDOW_CLOSE and
                    event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.file_dialog = None


                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()



if __name__ == "__main__":
    app = Window()
    app.run()
