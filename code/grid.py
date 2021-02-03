from cell import Cell
class Grid:
    """
    we parse the benchmark file and form a grid of cells(rows * cols). 
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.g = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.net_list = []

    def reset_grid(self):
        """Clear labels of cells in the grid and colourize."""
        for row in self.g:
            for cell in row:
                # cell.connected = False
                cell.clear_label()
    
    def sort_netlist(self):
        """Sorts the net_list based on the number of pins."""
        tmp = sorted(self.net_list, key=lambda net: net.num_pins)
        self.netlist = tmp
    