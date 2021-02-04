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

    def reset_grid(self):
        """Clear labels of cells in the grid and colourize."""
        for row in self.grid:
            for cell in row:
                # cell.connected = False
                cell.clear_label()
                # cell.colourize()
    # def clear_path(self):  # thoroughly reset to start a whole new turn of routing (rip up all and clear all status)
    #     """clear all routed path"""
    #     for row in self.grid:
    #         for cell in row:
    #             if (not cell.is_sink()) and (not cell.is_src()) and (cell.net_num != 0):
    #                 cell.net_num = 0
    #                 cell.connected = False
    #             if (cell.is_sink()):
    #                 cell.sink_used = False
    #                 cell.connected = False
    #             # if (not cell.is_src())and (not cell.is_sink()) and (cell.is_connected)
    #             if (cell.is_routable()):
    #                 cell.routable = True
    

    def sort_netlist(self):
        """Sorts the netlist based on the number of pins."""
        tmp = sorted(self.netlist, key=lambda net: net.num_pins)
        self.netlist = tmp