import operator
import logging

class Net:
    """ part of the netlist

    Attributes:
    cells: contains the cells belongs to the net
    color: net color
    min_row, max_row, min_col, max_col: the four borders of the nets
    """

    def __init__(self):
        self.cells = [] # contains the cells inside this net
        self.color = 'black'

        # for calculating half perimeter
        self.min_row = 0
        self.max_row = 0
        self.min_col = 0
        self.max_col = 0


    # def calc_half_perimeter(self):
    #     """return half perimeter of current net
    #     half_perimeter = (max_row - min_row) + (max_col - min_col)
    #     """
    #     # empty nets
    #     if not self.cells:
    #         return 0

    #     # find four borders
    #     # row
    #     cells_sorted_by_row = sorted(self.cells, key=operator.attrgetter('row'))  
    #     # print("sort by row", cells_sorted_by_row)  # sort cells by row number
    #     min_row = cells_sorted_by_row[0].row
    #     max_row = cells_sorted_by_row[-1].row
    #     self.min_row = min_row
    #     self.max_row = max_row


    #     logging.info("[net.py] sorted cells by row number {}".format(cells_sorted_by_row))
    #     logging.info("[net.py] min_row {}, max_row {}".format(min_row, max_row))
    #     print("min_row {}, max_row {}".format(min_row, max_row))

    #     # col
    #     cells_sorted_by_col = sorted(self.cells, key=operator.attrgetter('col'))    # sort cells by col number
    #     min_col = cells_sorted_by_col[0].col
    #     max_col = cells_sorted_by_col[-1].col
    #     self.min_col = min_col
    #     self.max_col = max_col
    #     # print("sort by col", cells_sorted_by_col)

    #     logging.info("[net.py] sorted cells by col number {}".format(cells_sorted_by_col))
    #     logging.info("[net.py] min_col {}, max_col {}".format(min_col, max_col))
    #     print("min_col {}, max_col {}".format(min_col, max_col))

    #     # calculate half perimeter
    #     half_perimeter = (max_row - min_row) + (max_col - min_col)

    #     return half_perimeter


    def calc_half_perimeter(self):
        """return half perimeter of current net
        half_perimeter = (max_row - min_row) + (max_col - min_col)
        """
        # empty nets
        if not self.cells:
            return 0

        # find four borders
        # row
        x_min = x_max = self.cells[0].col
        y_min = y_max = self.cells[0].row

        # find max and min row and col values of remaining nodes
        for node in self.cells[1:]:
            if node.col < x_min:
                x_min = node.col
            elif node.col > x_max:
                x_max = node.col

            if node.row < y_min:
                y_min = node.row
            elif node.row > y_max:
                y_max = node.row

        # calculate half perimeter bounding box
        # - multiply y coord by 2 to account for empty rows between cells
        hpbb = (x_max - x_min) + 2*(y_max - y_min)
        # print("hpbb", hpbb)
        return hpbb



