"""
routing algorithms
"""

from queue import PriorityQueue
import random

from grid import Grid
from cell import Cell
from net import Net
from helpers import *
import config as c

print("ROUTING ROWS",c.ROWS)
grid = Grid(c.ROWS, c.COLS)
g = grid.g



def route_from_start(start): 
    """ route a single point with Lee-Moore
    we start exploring from the start cell and stops whenever a possible target

    Arguments: 
        start: the cell as the start point
    Return:
        True: if the cell is routed to a target
        False: cannot reach a target
    """
    print("route from {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))
    counter = 0 # for priorityqueue (priority, counter, object)
    label = 1
    q = PriorityQueue() # stores the cell we want to explore
    q.put((label, counter, start)) #(priority, count, obj) (we have to put counter here to use the PriorityQueue with obj)
    # curr = None
    while not q.empty():
        
        curr = q.get()[2]

        # exit the loop if we reach a target or wire
        if (start.is_src()) and (curr.is_sink()) and (curr.net_num == start.net_num) and (not curr.is_sink_used):
            curr.sink_used = True
            print("src reaches a sink", curr)
            break
        if (curr.is_connected()) and (curr.net_num == start.net_num) and (curr is not start):
            print("sink reaches an existing wire or src")
            break
            
        neighbours = get_neighbours(g, curr, curr.net_num)
        for nei in neighbours:
            nei.visited = True
            c.COLOR_GRID[nei.row][nei.col] = c.COLOR_VIS

            if nei.label == 0:
                nei.cost_from_src = curr.cost_from_src + 1
                label = nei.cost_from_src
                nei.set_label(label)
                # set previous cell of neighbour to current cell
                nei.prev = curr
                # add neighbour to expansion list
                counter += 1
                q.put((nei.label, counter,nei))
        yield # show frames of routing progress

    # could not route the start to a target
    else:  #else only executed when while condition becomes false. it won't be executed if we break out of the loop, or if an exception is raised.
        print("fail to route {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))
        clear_visited(g)
        start.routable = False
        yield False

    # routed successfully 
    # bacltracing:
    # - start at taget, walk back along prev cells
    while True and curr.is_routable():
        # print("tracing back")
        curr.connected = True
        # don't modify content for source and sink
        if not (curr.is_source()) and (not curr.is_sink()):
            curr.net_num = start.net_num
            curr.content = 'net'
        if curr is start:
            break
        curr = curr.prev # backtracing to start

    
    grid.reset_grid()
    clear_visited(g)

    yield True

def route_all():
    """Return the amount of net we routed successfully
    1. route source to any possible sink
    2. route from sink backwards to any possible path
    """
    grid.sort_netlist()
    routed_net_count = 0
    for net in grid.net_list:
        print("-----------------routing net {} -----------------".format(net.net_num))
        net.sort_sinks()

        yield from route_from_start(net.source)

        if(len(net.sinks) > 1):
            print("routing from sinks of net {}".format(net.net_num))
            for sink in net.sinks:
                if sink.is_sink_used():
                    print("{} conneted. skip to next sink".format(sink))
                    continue
                yield from route_from_start(sink)

        if net.is_routed():
            routed_net_count += 1
    
    # return routed_net_count