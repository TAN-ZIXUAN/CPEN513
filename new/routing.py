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
    return neighbors

def backtracing(grid,curr2pre, curr, src):
    step = 0
    while curr in curr2pre and curr != src:
        # c.PATH_ARR.append(curr)
        grid[curr[0]][curr[1]] = c.T_PATH
        curr = curr2pre[curr]
        step += 1
    return step

def route(grid, src):
    print("routing from source:", src)
    path_arr = []
    def route_generator(): 
        founded = False
        # count = 0
        q = deque()
        q.append(src)
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
            print("curr", curr)
            # find path to a sink
            
            # exploaring and update cost
            neighbors = update_nei(grid, curr[0], curr[1], src)
            # for nei in neighbors:
            #     grid[nei[0]][nei[1]] = c.T_VISITED

            print(neighbors)
            for nei in neighbors:
                grid[nei[0]][nei[1]] = c.T_VISITED
                
                if nei in c.SOURCE2SINKS[src] and grid[curr[0]][curr[1]] != c.T_SINK_ROUTED: 
                    step = backtracing(grid, curr2pre, curr,src)
                    grid[nei[0]][nei[1]] = c.T_SINK_ROUTED
                    
                    
                    print("routed:")
                    print("src", src)
                    print("sink", curr)
                    print("path", curr2pre)
                    print("step", step)
                    founded = True
                    break

                tmp_cost = cost[curr] + 1

                if tmp_cost < cost[nei]:
                    curr2pre[nei] = curr
                    
                    cost[nei] = tmp_cost
                    if nei not in q and not founded:
                        q.append(nei)
                        # grid[nei[0]][nei[1]] =c.T_PATH

            yield
            if founded: # has to unfolded backtracing to show path in frame
                step = 0
                while curr in curr2pre:
                    grid[curr[0]][curr[1]] = c.T_PATH
                    c.PATH_ARR.append(curr)
                    curr = curr2pre[curr]
                    step += 1
                    # print("path arr", c.PATH_ARR)
                    return
            


                # return
    
    return route_generator

def route_wire(grid, wire):
    def route_wire_generator():
        # print(c.WIRE2SOURCE)
        src = c.WIRE2SOURCE[wire]
        for _ in c.SOURCE2SINKS[src]:
            print("route wire", src)
            founded = False
            # count = 0
            q = deque()
            q.append(src)
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
                print("curr", curr)
                # find path to a sink
                
                # exploaring and update cost
                neighbors = update_nei(grid, curr[0], curr[1], src)
                # for nei in neighbors:
                #     grid[nei[0]][nei[1]] = c.T_VISITED

                print(neighbors)
                for nei in neighbors:
                    grid[nei[0]][nei[1]] = c.T_VISITED
                    
                    if nei in c.SOURCE2SINKS[src] and grid[curr[0]][curr[1]] != c.T_SINK_ROUTED: 
                        step = backtracing(grid, curr2pre, curr,src)
                        grid[nei[0]][nei[1]] = c.T_SINK_ROUTED
                        
                        
                        print("routed:")
                        print("src", src)
                        print("sink", curr)
                        print("path", curr2pre)
                        print("step", step)
                        founded = True
                        break

                    tmp_cost = cost[curr] + 1

                    if tmp_cost < cost[nei]:
                        curr2pre[nei] = curr
                        
                        cost[nei] = tmp_cost
                        if nei not in q:
                            q.append(nei)
                            # grid[nei[0]][nei[1]] =c.T_PATH

                yield
                # if founded: # has to unfolded backtracing to show path in frame
                #     step = 0
                #     while curr in curr2pre:
                #         grid[curr[0]][curr[1]] = c.T_PATH
                #         curr = curr2pre[curr]
                #         step += 1
                #         yield 
        
        if all(grid[sink[0]][sink[1]] == c.T_SINK_ROUTED for sink in c.SOURCE2SINKS[src]):
                print("all sink routed")
                print("path arr", c.PATH_ARR)
                return
        
    return route_wire_generator
# def routeAll(grid):
#     for i in range(c.NUM_WIRE):

def route_sink2path(sink, path):
    pass






        

