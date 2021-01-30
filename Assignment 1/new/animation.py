from __future__ import division
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

import config as c
from functions import *
from routing import *

default_file = "rusty.infile"
if len(sys.argv) < 2: # not parsing file argument. use default file
    print("default file loaded", "kuma.infile")
    print("please put file path as first argument")
    file_path = default_file
else:
    file_path= sys.argv[1] # file name or path
    print("loaded file", file_path)
if not file_path:
    print("no file selected!") 
    sys.exit()

parse_file(file_path)

colorGrid = c.COLOR_GRID

# Initialize figure, imshow object, and axis.
fig = plt.figure()
# fig.set_size_inches(5* 2400.0/float(c.WIDTH),5* 1220.0/float(c.HEIGHT))
gridPlot = plt.imshow(colorGrid, interpolation='nearest')
ax = gridPlot._axes
ax.grid(visible=True, ls='solid', color='k', lw=1.5)
# plt.gca().set_aspect("equal") # forced the  grid shape to square
ax.set_xticklabels([])
ax.set_yticklabels([])

colText = ax.annotate('', (0.15, 0.04), xycoords='figure fraction')
rowText = ax.annotate('', (0.15, 0.07), xycoords='figure fraction')

def set_axis_properties(rows, cols):
    '''Set axis/imshow plot properties based on number of rows, cols.'''
    ax.set_xlim((0, cols))
    ax.set_ylim((rows, 0))
    ax.set_xticks(np.arange(0, cols+1, 1))
    ax.set_yticks(np.arange(0, rows+1, 1))
    gridPlot.set_extent([0, cols, 0, rows])

def update_annotations(rows, cols, obstProb):
    '''Update annotations with obstacle probability, rows, cols.'''
    # obstText.set_text('Obstacle density: {:.0f}%'.format(obstProb * 100))
    colText.set_text('Rows: {:d}'.format(rows))
    rowText.set_text('Columns: {:d}'.format(cols))


set_axis_properties(c.NUM_X, c.NUM_Y)
# update_annotations(c.NUM_WIRE, c.NUM_Y, obstProb)


def init_anim():
    '''Plot grid in its initial state by resetting "grid".'''
    grid = generate_grid(c.NUM_X, c.NUM_Y)
    colorGrid = color_grid(grid)
    gridPlot.set_data(colorGrid)

def update_anim(dummyFrameArgument):
    '''Update plot based on values in "grid" ("grid" is updated
        by the generator--this function simply passes "grid" to
        the color_grid() function to get an image array).
    '''
    colorGrid = color_grid(c.GRID)
    gridPlot.set_data(colorGrid)

src = c.WIRE2SOURCE[0]

# Create animation object. Supply generator function to frames.
ani = animation.FuncAnimation(fig, update_anim,
    init_func=init_anim, frames=route(c.GRID, src),
    repeat=False, interval=200)

# Turn on interactive plotting and show figure.
plt.ion()
plt.show(block=True)