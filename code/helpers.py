"""
some helper functions we need
"""
import math
import numpy as np
import config as c
from grid import Grid
from cell import Cell
from net import Net

def clear_visited(g):
    """
    used to clear visted path
    call this whenever starting a new routing.

    Arguments:
    grid: the grid(rows*cols) represents the parsed benchmark file 

    """
    (rows, cols) = (len(g), len(g[0]))
    for i in range(rows):
        for j in range(cols): 
            cell = g[i][j]
            cell.visited = False


def get_neighbours(g, cell, net_num):
    """Return a list of neighbours of a given cell. 
    Do not include neighbour cells that contain obstacles or cells that
    belong to other nets.
    
    Arguments:
    grid: the grid(rows*cols) represents the parsed benchmark file 
    cell - the cell in the grid that we need to find its neighbours
    net_num - the net number of the Net instance we are routing

    """
    neighbours = []
    (rows, cols) = (len(g), len(g[0]))

    # coordinates of possible neighbours
    locs = [{'row' : cell.row,   'col' : cell.col-1}, # north
            {'row' : cell.row+1, 'col' : cell.col},   # east
            {'row' : cell.row,   'col' : cell.col+1}, # south
            {'row' : cell.row-1, 'col' : cell.col}]   # west
    
    # get neighbours in random order
    # random.shuffle(locs) 
    for loc in locs:
        # check bounds of possible neighbours
        if (0 <= loc['row'] < rows) and (0 <= loc['col'] < cols):
            cell = g[loc['row']][loc['col']]
            # don't consider obstacles
            if cell.is_obs():
                continue
            # don't consider cells that belong to other nets
            if cell.net_num not in [0, net_num]:
                continue
            neighbours.append(cell)

    return neighbours

def color_grid(g): # return a grid consit of colors (also call this to update color of each cell)
    (rows, cols) = (len(g), len(g[0]))

    colorGrid = np.full((rows, cols, 3), c.COLOR_UNVIS)
    num2color_name = {0: (255, 0, 0),
             1: (255, 255, 0),
             2:(230, 126, 34), # SILVER
             3:(0,128,128),
             4:(255,0,255), #RED/MARGENTA
             5:(188,143,143),
             6:(125, 206, 160),
             7:(64, 224, 208)
             }
    
    colorGrid = np.full((rows, cols, 3), c.COLOR_UNVIS)

    for i in range(rows):
        for j in range(cols): 
            # print(i, j)
            cell = g[i][j]
            if cell.is_obs():
                # print("color obs")
                colorGrid[i][j] = c.COLOR_OBS
            elif cell.is_visited() and (not cell.is_src()) and (not cell.is_sink()): # normal non obstacel visitedcell
                colorGrid[i][j] = c.COLOR_VIS

            if not cell.is_obs() and cell.net_num != 0:
                # print("sink source path")
                color = num2color_name[(cell.net_num) % len(num2color_name)] # sink source and path
                colorGrid[i][j] = color # it assign net num to connected path. so here we colored the path
            # if cell.is_connected() and (not cell.is_source()) and (not cell.is_sink()):
            #     colorGrid[i][j] = GREEN

    return colorGrid

def parse_netlist(filepath):
    """Parse a netlist and populate the layout.grid.
    
    filepath - the full path of the netlist file to parse"""
    with open(filepath, 'r') as f:
        # first line is grid size
        line = f.readline().strip().split()
        
        cols = int(line[0])
        rows= int(line[1])
        c.ROWS = rows # col
        c.COLS = cols # row
        print("parse ROW", c.ROWS)
        
        grid = Grid(rows, cols)
        g = grid.g

        # next lines are obstructed cells
        num_obs = int(f.readline().strip())
        for i in range(num_obs):
            line = f.readline().strip().split()
            col = int(line[0])
            row = int(line[1])
            cell = g[row][col]
            cell.row = row
            cell.col = col
            cell.type = 'obs'

        # next lines are wires to route
        grid.net_list = []
        num_wires = int(f.readline().strip())
        for i in range(num_wires):
            net_num = i + 1 # nets are numbered from 1

            line = list(map(int, f.readline().strip().split()))
            # first item in line is number of pins
            num_pins = line.pop(0)

            # second item is x, y coordinates of source
            col = line.pop(0)
            row = line.pop(0)
            src = g[row][col]
            src.type = 'src'
            src.connected = True
            src.net_num = net_num

            # next items are x, y coordinates of sinks
            sinks = []
            for _ in range(num_pins-1):
                col = line.pop(0)
                row = line.pop(0)
                sink = g[row][col]
                sink.type = 'sink'
                sink.net_num = net_num
                sink.est_dist_from_src = sink.estimate_dist(src)
                sinks.append(sink)

            grid.net_list.append(Net(net_num, num_pins, src, sinks))
            print("net_list", grid.net_list)

        c.COLOR_GRID = color_grid(g)

