import numpy as np
import math
import config as c
import collections
from collections import deque 

from functions import *



def can_explore(grid, row, col, src): # check if current cell can be explored while routing from the src
    if grid[row][col] == c.T_UNVIS or ((row, col) in c.SOURCE2SINKS[src]):
        return True
    return False

# return  explorable neighbours
# value = -1 found sink 
# value >=1  cost from source to current neighbour

def update_nei(grid, row, col, src): # check neighbors
    (rows, cols) = grid.shape
    neighbors = [] # valid neighbours: sink or empty node

    if row < rows -1  and can_explore(grid, row + 1, col, src): # DOWN
        neighbors.append((row + 1, col))
    if row > 0 and can_explore(grid, row - 1, col, src): # UP
        neighbors.append((row - 1, col))
    if col <  cols - 1 and can_explore(grid, row, col + 1, src): # RIGHT
        neighbors.append((row, col + 1))

    if col > 0 and can_explore(grid, row, col - 1, src): # LEFT
        neighbors.append((row, col - 1))

def backtracing(grid,curr2pre, curr, draw):
    while curr in curr2pre:
        grid[curr[0]][curr[1]] = c.T_PATH
        curr = curr2pre[curr]

def route(grid, src):
    print("routing from source:", src)
    def route_generator():
        
        count = 0
        q = deque(src)
        curr2pre = {}
        # initial cost
        (rows, cols) = grid.shape
        cost = {}
        for i in range(rows):
            for j in range(cols):
                cost[(i, j)] = float("inf")
        cost[src] = 0

        while q:
            curr = q.popleft()
            # find path to a sink
            if curr in c.SOURCE2SINKS[src] and grid[nei[0]][nei[1]] != c.T_SINK_ROUTED: 
                grid[nei[0]][nei[1]] = c.T_SINK_ROUTED
                backtracing(grid, curr2pre, curr)
                 
                print("routed: " + src + " to " + sink)
                
                yield
            # exploaring and update cost
            for nei in update_nei(grid, curr[0], curr[1]):
                tmp_cost = cost[curr] + 1

                if tmp_cost < cost[nei]:
                    curr2pre[nei] = curr
                    cost[nei] = tmp_cost
                    if nei not in q:
                        q.append(nei)

                        yield




        

