import operator
import logging

class Net:
    """ part of the netlist

    Attributes:
    cells: contains the cells belongs to the net
    color: color o net line (border color of grid)
    net_id: id of net, starting from 0
    min_row, max_row, min_col, max_col: the four borders of the nets
    """

    def __init__(self):
        self.cells = [] # contains the cells(cell object) inside this net
        self.color = 'black'
        self.net_id = None

        # for calculating half perimeter
        # self.min_row = 0
        # self.max_row = 0
        # self.min_col = 0
        # self.max_col = 0


    def calc_half_perimeter(self):
        """return half perimeter of current net
        half_perimeter = (max_row - min_row) + (max_col - min_col)
        """
        # empty nets
        if not self.cells:
            return 0

        # find four borders
        # row
        cells_sorted_by_row = sorted(self.cells, key=operator.attrgetter('corresponding_site.row'))  
        # print("sort by row", cells_sorted_by_row)  # sort cells by row number
        min_row = cells_sorted_by_row[0].corresponding_site.row
        max_row = cells_sorted_by_row[-1].corresponding_site.row
        # self.min_row = min_row
        # self.max_row = max_row



        # print("min_row {}, max_row {}".format(min_row, max_row))

        # col
        cells_sorted_by_col = sorted(self.cells, key=operator.attrgetter('corresponding_site.col'))    # sort cells by col number
        min_col = cells_sorted_by_col[0].corresponding_site.col
        max_col = cells_sorted_by_col[-1].corresponding_site.col
        # self.min_col = min_col
        # self.max_col = max_col
        # print("sort by col", cells_sorted_by_col)

        # print("min_col {}, max_col {}".format(min_col, max_col))

        # calculate half perimeter
        half_perimeter = (max_row - min_row) + 2 * (max_col - min_col)

        return half_perimeter





