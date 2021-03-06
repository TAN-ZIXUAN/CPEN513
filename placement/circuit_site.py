class Site:
    """cell site which cell can be placed on
    sites forms the circuit

    Attributes:
    row: row number of the site
    col: col number of the site
    element: cell in the current site. None if it's empty
    text: text is the number of cell which occupies the site
    rect: canvas rectangle unit

    """
    def __init__(self, row=None, col=None):
        self.row = row
        self.col = col
        self.element = None    # cell in the current site. None if it's empty
        self.rect = None
    
    def is_empty(self):
        return self.element == None

    def __str__(self):
        """string representation of the site"""
        if  self.is_empty():
            return 'empty site ({row},{col})'.format(row=self.row, col=self.col)
        else:
            return 'site ({row},{col}) occupided by cell_{cell_id}'.format(row=self.row, col=self.col, cell_id=self.element.cell_id)

    def update_rect(self, canvas):
        """Colour the rectangle according to content, set text to Node ID."""
        if self.is_empty():
            canvas.itemconfigure(self.rect, fill='white')
        else:
            canvas.itemconfigure(self.rect, fill='blue')

    

    def get_rect_center(self, canvas):
        """Returns (x, y) coordinates of center of Site's canvas rectangle."""
        x1, y1, x2, y2 = canvas.coords(self.rect) # get rect coords
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return (center_x, center_y)


        
    
