"""
create animation using FuncAnimation from matplot
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

from helpers import *
import config as c
from routing import *

default_file = "kuma.infile"
if len(sys.argv) < 2: # not parsing file argument. use default file
    print("default file loaded", "kuma.infile")
    print("please put file path as argument[1]")
    file_path = default_file
else:
    file_path= sys.argv[1] # file name or path
    print("loaded file", file_path)
if not file_path:
    print("no file selected!") 
    sys.exit()

parse_netlist(file_path)

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
    g = Grid(c.ROWS, c.COLS).g
    # c.GRID = g
    colorGrid = color_grid(g)
    gridPlot.set_data(colorGrid)

def update_anim(dummyFrameArgument):
    '''Update plot based on values in "grid" ("grid" is updated
        by the generator--this function simply passes "grid" to
        the color_grid() function to get an image array).
    '''
    print("update frame")
    g = Grid(c.ROWS, c.COLS).g
    # c.GRID = g
    colorGrid = color_grid(g)
    gridPlot.set_data(colorGrid)



# Create animation object. Supply generator function to frames.
ani = animation.FuncAnimation(fig, update_anim,
    init_func=init_anim, frames=route_all(),
    repeat=False, interval=100)

# Turn on interactive plotting and show figure.
plt.ion()
plt.show(block=True)