class Cell:
    """cell need to be placed on circuits

    Attributes:
    cell_id: id of the cell. starting from 0
    corresponding_site: the site which cell is placed on
    row: row number of the cell
    col: col number of the cell
    nets: list of nets that the cell are in

    """
    def __init__(self, cell_id):
        self.cell_id = cell_id
        self.corresponding_site = None
        # self.row = None
        # self.col = None
        self.nets = []
        

    def __str__(self):
        return 'cell {cell_id} ({row}, {col})'.format(cell_id=self.cell_id, row=self.corresponding_site.row, col=self.corresponding_site.col)

    def calc_nets_cost_with_cell(self):
        """ return the cost of nets after including the current cell
        (sum of cost of all nets that includes the cell)
        
        """
        nets_cost = 0
        for net in self.nets:
            nets_cost += net.calc_half_perimeter()
        
        return nets_cost

    def calc_incremental_net_cost(self, net):
        """ return cost of the net
        update the cost of the net afer including the cell incrementally
        (compare the row and col of cell with the net's bounadary)
        """

        min_row = min(net.min_row, self.corresponding_site.row)
        max_row = max(net.max_row, self.corresponding_site.row)
        min_col = min(net.min_col, self.corresponding_site.col)
        max_col = max(net.max_col, self.corresponding_site.col)

        half_perimeter = (max_row - min_row) + (max_col - min_col)

        return half_perimeter

        


