class Site:
    """cell site which cell can be placed on
    sites forms the circuit

    Attributes:
    row: row number of the site
    col: col number of the site
    element: cell in the current site. None if it's empty

    """
    def __init__(self, row=None, col=None):
        self.row = row
        self.col = col

        self.element = None    # cell in the current site. None if it's empty
    
    def is_empty(self):
        return self.element == None

    def __str__(self):
        """string representation of the site"""
        if  self.is_empty():
            return 'empty site ({row},{col})'.format(row=self.row, col=self.col)
        else:
            return 'site ({row},{col}) occupided by cell_{cell_id}'.format(row=self.row, col=self.col, cell_id=self.element.cell_id)

        
    
