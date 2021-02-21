import logging


from cell import Cell
from net import Net
from circuit_site import Site


def create_hex_color_list(color_file="hex_color.txt"):
    """return hex color list"""
    hex_colors = [] # 949 colors 
    with open(color_file, 'r') as f:
        for line in f:
            l = line.strip().split()
            # print(line[-1])
            hex_colors.append(l[-1])

    return hex_colors

class Circuit:
    """ circuit consists of cell sites.

    Attributes:
    num_cells: number of cells
    num_connections: number of connections
    num_rows: number of rows in the circuit
    num_cols: number of columns in the circuit
    num_sites: number of sites on the circuit

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
        self.num_sites = 0
        

        self.grid = []  # the 2d grid that represents cirtcuit
        self.netlist = []
        self.cell_list = []  # list of cells
        self.total_cost = 0

    def init_grid(self, num_rows, num_cols):
        """init grid which represent the circuit"""
        self.grid = [[Site(row, col) for col in range(num_cols)] for row in range(num_rows)]
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_sites = num_rows * num_cols

    def init_net_list(self):
        self.netlist = []

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
        # self.total_cost = cost
        return cost

    def get_site_by_id(self, site_id):
        """return the site of given site id"""
        row = site_id // self.num_cols
        col = site_id % self.num_cols

        return self.grid[row][col]

    def update_rects(self, canvas):
        """update all rectangles"""
        for row in self.grid:
            for site in row:
                site.update_rect(canvas)

    def parse_circuit_file(self, filepath = "ass2_files/cm151a.txt"):
        """parse the circuit file"""
        with open(filepath, 'r') as f:
            for line_num, l in enumerate(f):
                line = l.strip().split()
                if not line: # be careful about empty lines
                    break
                # print("{} {}".format(line_num, line))
                if line_num == 0: # first line: num_cells, num_connections, num_rows, num_cols
                    self.num_cells = int(line[0])
                    self.init_cell_list(self.num_cells)
                    self.num_connections = int(line[1])
                    self.num_rows = int(line[2])
                    self.num_cols = int(line[3])
                    self.init_grid(self.num_rows, self.num_cols)
                    self.num_sites = self.num_rows * self.num_cols

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
                    net_num = line_num - 1 # net number starting from 0
                    # print("loading net", net_num)
                    hex_colors = create_hex_color_list()
                    net.color = hex_colors[net_num % len(hex_colors)] # TODO: create a color list from hex_color.txt
                    # num_cells_of_net = line[0]  # number of cells in current net

                    # cell_id
                    for item in line[1:]:
                        cell_id = int(item)
                        cell = self.cell_list[cell_id]
                        # print(cell.__str__())
                        cell.nets.append(net)
                        net.cells.append(cell)

                    self.netlist.append(net)


                    





