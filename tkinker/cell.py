class Cell:
    """Class representing a cell in the layout.
    
    Data attributes:
        xloc, yloc - coordinates of cell in the grid
        content - 'empty', 'src', 'sink', 'net'
        net_num - net number of net the Cell belongs to
        label - used for Lee-Moore and A* routing
        dist_from_src - used for A* routing
        prev - pointer to predecessor Cell
        rect_id - ID of canvas rectangle object in the gui
        text_id - ID of canvas text object in the gui
        connected - boolean indicating if Cell is connected
                    to a the net source
        
        For sinks only:
            est_dist_from_src - estimate of distance to net
                                source, used to compare sinks
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.content = 'empty'
        self.net_num = 0
        self.label = 0
        self.dist_from_src = 0
        self.prev = None
        self.rect_id = None 
        self.text_id = None
        self.connected = False
        self.est_dist_from_src = 0
        self.visited = False

    def __str__(self):
        """Return a string representation of a Cell."""
        if self.is_connected():
            c = 'x'
        else:
            c = 'o'
        return "Cell({net} {content} {c} ({row}, {col}) l={label}, prev={prev})".format(
                net=self.net_num, row=self.row, col=self.col, content=self.content,
                label=self.label, prev=repr(self.prev), c=c)

    def is_empty(self):
        if self.content == 'empty':
            return True
        else:
            return False

    def is_obstacle(self):
        if self.content == 'obstacle':
            return True
        else:
            return False

    def is_sink(self):
        if self.content == 'sink':
            return True
        else:
            return False

    def is_source(self):
        if self.content == 'src':
            return True
        else:
            return False

    def is_connected(self):
        return self.connected
    
    def is_visited(self):
        return self.visited


    def set_label(self, label):
        self.label = label
        if label == 0:
            self.set_text('')
        else:
            self.set_text(str(label))

    def clear_label(self):
        self.set_label(0)

    def set_text(self, text=''):
        # text for source is +, text for sink is -
        if self.is_source():
            text = '+'
        elif self.is_sink():
            text = '-'

    #     # create canvas text if needed
    #     if self.text_id == None:
    #         x, y = self._get_center()
    #         self.text_id = canvas.create_text(x, y, text=text)
    #     else:
    #         canvas.itemconfigure(self.text_id, text=text)

    # def _get_center(self):
    #     """Returns (x, y) coordinates of center of Cell's canvas rectangle."""
    #     x1, y1, x2, y2 = canvas.coords(self.rect_id) # get rect coords
    #     center_x = (x1 + x2) / 2
    #     center_y = (y1 + y2) / 2
    #     return (center_x, center_y)

    # def colourize(self):
    #     """Colour the cell according to contents."""
    #     net_colours = ['red', 'yellow', 'light grey', 'orange', 'magenta',
    #             'violet', 'green', 'purple']
    #     if self.is_obstacle():
    #         canvas.itemconfigure(self.rect_id, fill='blue')
    #     elif self.net_num != 0:
    #         colour = net_colours[(self.net_num - 1) % len(net_colours)]
    #         canvas.itemconfigure(self.rect_id, fill=colour)

    def estimate_dist(self, target):
        """Return the Manhatten distance between current and target Cells"""
        return abs(self.row - target.row) + abs(self.col - target.col)

