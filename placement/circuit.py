import logging
from site import Site

from cell import Cell
from net import Net


class Circuit:
    """ circuit consists of cell sites.

    Attributes:
    num_cells: number of cells
    num_connections: number of connections
    num_rows: number of rows in the circuit
    num_cols: number of columns in the circuit

    grid: the 2d grid which reprents the circuit
    netlist: netlist of the circuit
    cell_list: list of cells that should be placed on the circuit



    """

    def __init__(self):
        # number of cells placed the circuit (the number of cells need to be placed on the circuit)
        self.num_cells = 0
        self.num_connections = 0 # number of connections
        self.num_rows = 0   # number of rows in the circuit
        self.num_cols = 0   # number of columns in the circuit

        

        self.grid = []  # the 2d grid that represents cirtcuit
        self.netlist = []
        self.cell_list = []  # list of cells

    def init_grid(self, num_rows, num_cols):
        """init grid which represent the circuit"""
        self.grid = [Site(row, col) for col in range(num_cols)
                     for row in range(num_rows)]
        self.num_rows = num_rows
        self.num_cols = num_cols

    def init_cell_list(self, num_cells):
        """init cell_list"""
        self.cell_list = [Cell(cell_id) for cell_id in range(num_cells)]

    # def get_site_by_id():
    #     pass

    def calc_total_cost(self):
        """return the total cost the current placement"""
        cost = 0
        for net in self.netlist:
            cost += net.calc_half_perimeter()
        return cost

    def get_site_by_id(self, site_id):
        """return the site of given site id"""
        row = site_id // self.num_cols
        col = site_id% self.num_cols

        return self.grid[row][col]


    def parse_circuit_file(self, filepath = "ass2_files/cm151a.txt"):
        """parse the circuit file"""
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f)
                line = f.readline().strip().split()
                if line_num == 0: # first line: num_cells, num_connections, num_rows, num_cols
                    self.num_cells = int(line[0])
                    self.init_cell_list(self.num_cells)
                    self.num_connections = int(line[1])
                    self.num_rows = int(line[2])
                    self.num_cols = int(line[3])
                    self.init_grid(self.num_rows, self.num_cols)

                    logging.info("num_cells: {num_cells}, num_connections: {num_connections}, num_rows: {num_rows}, num_cols: {num_cols}".format(
                        num_cells = self.num_cells,
                        num_connections = self.num_connections,
                        num_rows = self.num_rows,
                        num_cols = self.num_cols
                    ))
                    print("num_cells: {num_cells}, num_connections: {num_connections}, num_rows: {num_rows}, num_cols: {num_cols}".format(
                        num_cells = self.num_cells,
                        num_connections = self.num_connections,
                        num_rows = self.num_rows,
                        num_cols = self.num_cols
                    ))
                else: # the rest of lines (contains netlist)
                    net = Net()
                    # net_num = cnt - 2 # net number starting from 0
                    # net.color = hex_color_list[net_num % len(hex_colors_list)] # TODO: create a color list from hex_color.txt
                    # num_cells_of_net = line[0]  # number of cells in current net

                    # cell_id
                    for item in line[1:]:
                        cell_id = int(item)
                        cell = self.cell_list[cell_id]
                        cell.nets.append(net)
                        net.cells.append(cell)

                    self.netlist.append(net)


                    





