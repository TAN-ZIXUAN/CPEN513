from cell import Cell
class Layout:
    """Class representing a the grid layout."""

    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.grid = [[]]
        self.netlist = []
        

    def init_grid(self, rows, cols):
        """Initialize the grid to given size by populating with empty Cells."""
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.rows = rows
        self.cols= cols
        # print("layout size")
        # print(self.rows)
        # print(self.cols)

    def print_grid(self):
        """Print the grid in text format."""
        for row in self.grid:
            for cell in row:
                if cell.is_source():
                    print('[{}s]'.format(cell.net_num), end='')
                elif cell.is_sink():
                    print('[{}t]'.format(cell.net_num), end='')
                elif cell.label != 0:
                    print('[{: >2}]'.format(cell.label), end='')
                elif cell.is_obstacle():
                    print('[**]', end='')
                else:
                    print('[  ]', end='')
            print()

    def reset_grid(self):
        """Clear labels of cells in the grid and colourize."""
        for row in self.grid:
            for cell in row:
                cell.clear_label()
                cell.colourize()

    def sort_netlist(self):
        """Sorts the netlist based on the number of pins."""
        tmp = sorted(self.netlist, key=lambda net: net.num_pins)
        self.netlist = tmp