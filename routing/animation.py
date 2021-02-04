from __future__ import division
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import matplotlib as mpl 
# mpl.rcParams['animation.ffmpeg_path'] = r"C:\Users\Tan\Downloads\ffmpeg-4.3.2-2021-02-02-full_build\bin"

from layout import Layout
from cell import Cell
from net import Net

import config as c
# from functions import *
from route import *
filename = "stdcell"
default_file = "benchmarks/" + filename + ".infile"

def parse_file(filepath):
    """Parse a netlist and populate the layout.grid.
    
    filepath - the full path of the netlist file to parse"""
    with open(filepath, 'r') as f:
        # first line is grid size
        line = f.readline().strip().split()
        # print(line[0])
        cols = int(line[0])
        rows= int(line[1])
        c.ROWS = rows # col
        c.COLS = cols # row
        # print("parse ROW", c.ROWS)
        
        layout.init_grid(rows, cols)

        # next lines are obstructed cells
        num_obs = int(f.readline().strip())
        for i in range(num_obs):
            line = f.readline().strip().split()
            col = int(line[0])
            row = int(line[1])
            cell = layout.grid[row][col]
            cell.row = row
            cell.col = col
            cell.type = 'obs'

        # next lines are wires to route
        layout.netlist = []
        num_wires = int(f.readline().strip())
        for i in range(num_wires):
            net_num = i + 1 # nets are numbered from 1

            line = list(map(int, f.readline().strip().split()))
            # first item in line is number of pins
            num_pins = line.pop(0)

            # second item is x, y coordinates of source
            col = line.pop(0)
            row = line.pop(0)
            source = layout.grid[row][col]
            source.type = 'src'
            source.connected = True
            source.net_num = net_num

            # next items are x, y coordinates of sinks
            sinks = []
            for _ in range(num_pins-1):
                col = line.pop(0)
                row = line.pop(0)
                sink = layout.grid[row][col]
                sink.type = 'sink'
                sink.net_num = net_num
                sink.est_dist_from_src = sink.estimate_dist(source)
                sinks.append(sink)

            layout.netlist.append(Net(net_num, num_pins, source, sinks))

        c.COLOR_GRID = color_grid(layout.grid)
        # print(c.COLOR_GRID)

def color_grid(grid): # return a grid consit of colors (also call this to update color of each cell)
    (rows, cols) = (len(grid), len(grid[0]))
    # print("layout grid")
    # print(len(layout.grid), len(layout.grid[0]))
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
            cell = layout.grid[i][j]
            if cell.is_obs():
                colorGrid[i][j] = c.COLOR_OBS
            elif cell.is_visited() and (not cell.is_src()) and (not cell.is_sink()): # normal non obstacel visitedcell
                colorGrid[i][j] = c.COLOR_VIS

            if not cell.is_obs() and cell.net_num != 0:
                color = num2color_name[(cell.net_num) % len(num2color_name)] # sink source and path
                colorGrid[i][j] = color # it assign net num to connected path. so here we colored the path
            # if cell.is_connected() and (not cell.is_source()) and (not cell.is_sink()):
            #     colorGrid[i][j] = GREEN

    return colorGrid


if len(sys.argv) < 2: # not parsing file argument. use default file
    print("default file loaded", default_file)
    print("please put file path as argument[1]")
    file_path = default_file
else:
    file_path= sys.argv[1] # file name or path
    print("loaded file", file_path)
if not file_path:
    print("no file selected!") 
    sys.exit()
c.FILEPATH = file_path
parse_file(file_path)

fig = plt.figure()
# fig.set_size_inches(5* 2400.0/float(c.WIDTH),5* 1220.0/float(c.HEIGHT))
gridPlot = plt.imshow(c.COLOR_GRID, interpolation='nearest')
ax = gridPlot._axes
ax.grid(visible=True, ls='solid', color='k', lw=1.5)
# plt.gca().set_aspect("equal") # forced the  grid shape to square
ax.set_xticklabels([])
ax.set_yticklabels([])

def set_axis_properties(rows, cols):
    # print("rows", rows)
    # print("cols", cols)
    '''Set axis/imshow plot properties based on number of rows, cols.'''
    ax.set_xlim((0, cols))
    ax.set_ylim((0, rows))
    ax.set_xticks(np.arange(0, cols+1, 1))
    ax.set_yticks(np.arange(0, rows+1, 1))
    gridPlot.set_extent([0, cols, 0, rows])


set_axis_properties(c.ROWS, c.COLS)
# update_annotations(c.NUM_WIRE, c.NUM_Y, obstProb)


def init_anim():
    '''Plot grid in its initial state by resetting "grid".'''
    layout = Layout()
    layout.init_grid(c.ROWS, c.COLS)
    # layout.print_grid()
    grid = layout.grid
    # print("grid", grid)
    c.GRID = grid
    colorGrid = color_grid(grid)
    gridPlot.set_data(colorGrid)

def update_anim(dummyFrameArgument):
    '''Update plot based on values in "grid" ("grid" is updated
        by the generator--this function simply passes "grid" to
        the color_grid() function to get an image array).
    '''
    layout = Layout()
    layout.init_grid(c.ROWS, c.COLS)
    # layout.print_grid()
    grid = layout.grid
    # print("grid", grid)
    c.GRID = grid
    colorGrid = color_grid(grid)
    gridPlot.set_data(colorGrid)


# route_with_shuffle(10)
# Create animation object. Supply generator function to frames.
ani = animation.FuncAnimation(fig, update_anim,
    init_func=init_anim, frames=route_with_shuffle(100),
    repeat=False, interval=100, save_count=2000)
ani.save('gif/'+filename +".gif", writer='pillow') # comment this if you want the animation programme runs realtime
print("gif generated")

# Turn on interactive plotting and show figure.
plt.ion()
plt.show(block=True)