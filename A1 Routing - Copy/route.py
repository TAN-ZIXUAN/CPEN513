from queue import PriorityQueue
import random
import logging
from layout import Layout
from cell import Cell
from net import Net
import config as c
from itertools import permutations 
# from animation import update_annotations
# from animation import filename

layout = Layout()
middle_frames = True # true: contain frames showing routing process


def reload_layout(filepath):
    """Parse a netlist and populate the layout.grid.

    filepath - the full path of the netlist file to parse"""
    with open(filepath, 'r') as f:
        # first line is grid size
        line = f.readline().strip().split()
        
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

        # c.COLOR_GRID = color_grid(layout.grid)





def clear_visited(grid): # call this when ever start a new routing
    (rows, cols) = (len(grid), len(grid[0]))
    for i in range(rows):
        for j in range(cols): 
            cell = grid[i][j]
            cell.visited = False

    
def get_neighbours(cell, net_num):
    """Return a list of neighbours of a given cell. 
    Do not include neighbour cells that contain obstacles or cells that
    belong to other nets.
    
    Arguments:
    grid: the grid(rows*cols) represents the parsed benchmark file 
    cell - the cell in the grid that we need to find its neighbours
    net_num - the net number of the Net instance we are routing

    """
    neighbours = []
    (rows, cols) = (layout.rows, layout.cols)

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
            cell = layout.grid[loc['row']][loc['col']]
            # don't consider obstacles
            if cell.is_obs():
                continue
            # don't consider cells that belong to other nets
            if cell.net_num not in [0, net_num]:
                continue
            neighbours.append(cell)

    return neighbours

def route_LeeMoore(start):
    """ route a single point with Lee-Moore
    we start exploring from the start cell and stops whenever a possible target

    Arguments: 
        start: the cell as the start point
    Return:
        True: if the cell is routed to a target
        False: cannot reach a target
    """
    print("Lee Moore: route from {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))

    counter = 0 # for priorityqueue (priority, counter, object)
    label = 1
    q = PriorityQueue() # stores the cell we want to explore
    q.put((label, counter, start)) #(priority, count, obj) (we have to put counter here to use the PriorityQueue with obj)
    curr = None
    while not q.empty():
        
        curr = q.get()[2]

        # exit the loop if we reach a target or wire
        if (start.is_src()) and (curr.is_sink()) and (curr.net_num == start.net_num) and (not curr.sink_used):
            curr.sink_used = True
            # print("src reaches a sink", curr)
            break
        if (curr.is_connected()) and (curr.net_num == start.net_num) and (curr is not start):
            # print("sink reaches an existing wire or src")
            break
            
        neighbours = get_neighbours(curr, start.net_num)
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
        if middle_frames:
            yield # show frames of routing progress

    # could not route the start to a target
    else:  #else only executed when while condition becomes false. it won't be executed if we break out of the loop, or if an exception is raised.
        # print("fail to route {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))
        clear_visited(layout.grid)
        curr.routable = False
        layout.reset_grid()
        yield False

    # routed successfully 
    # bacltracing:
    # - start at taget, walk back along prev cells
    while True and curr.is_routable():
        # print("tracing back")
        curr.connected = True
        # don't modify content for source and sink
        if not (curr.is_src()) and (not curr.is_sink()):
            curr.net_num = start.net_num
            curr.content = 'net'
        if curr is start:
            break
        curr = curr.prev # backtracing to start

    
    layout.reset_grid()
    clear_visited(layout.grid)

    yield True
    



def route_a_star(start, target):
    print("A*: route from {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))
    q = PriorityQueue()
    counter = 0
    label = 0 + start.estimate_dist(target)
    q = PriorityQueue() # stores the cell we want to explore
    q.put((label, counter, start)) #(priority, count, obj) (we have to put counter here to use the PriorityQueue with obj)
    curr = None
    while not q.empty():
        
        curr = q.get()[2]

        # exit the loop if we reach a target or wire
        if curr is target:
            break
            
        neighbours = get_neighbours(curr, start.net_num)
        for nei in neighbours:
            nei.visited = True
            c.COLOR_GRID[nei.row][nei.col] = c.COLOR_VIS

            if nei.label == 0:
                nei.cost_from_src = curr.cost_from_src + 1
                label = nei.cost_from_src + nei.estimate_dist(target)
                nei.set_label(label)
                # set previous cell of neighbour to current cell
                nei.prev = curr
                # add neighbour to expansion list
                counter += 1
                q.put((nei.label, counter,nei))
        # yield # show frames of routing progress
        if middle_frames:
            yield # show frames of routing progress

    # could not route the start to a target
    else:  #else only executed when while condition becomes false. it won't be executed if we break out of the loop, or if an exception is raised.
        # print("fail to route {type} ({x} {y})".format(type = start.type, x = start.row, y = start.col))
        clear_visited(layout.grid)
        curr.routable = False
        layout.reset_grid()
        yield False

    # routed successfully 
    # bacltracing:
    # - start at taget, walk back along prev cells
    while True and curr.is_routable():
        # print("tracing back")
        curr.connected = True
        # don't modify content for source and sink
        if not (curr.is_src()) and (not curr.is_sink()):
            curr.net_num = start.net_num
            curr.content = 'net'
        if curr is start:
            break
        curr = curr.prev # backtracing to start

    
    layout.reset_grid()
    clear_visited(layout.grid)

    yield True

def route_with_shuffle(trial_time):
    max_routed_net_count = 0
    routed_net_count = 0
    i = 0
    # final_routing = None # store the routing result when max_routed_net_count
    while i < trial_time and routed_net_count < len(layout.netlist):
        routed_net_count = 0
        random.shuffle(layout.netlist)
        print("================================route trial time #{} ================================".format(i))
        for net in layout.netlist:
            # print("-----------------routing net {} -----------------".format(net.net_num))
            random.shuffle(net.sinks)

            if len(net.sinks) <=1:
                yield from route_a_star(net.src, net.sinks[0]) # a*
            else: # lee-moore
                yield from route_LeeMoore(net.src)
                
                for sink in net.sinks:
                    if sink.is_sink_used():
                        # print("{} conneted. skip to next sink".format(sink))
                        continue
                    yield from route_LeeMoore(sink)

            if net.is_routed():
                routed_net_count += 1
            max_routed_net_count = max(max_routed_net_count, routed_net_count)
        print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))
        layout.reset_grid()
        reload_layout(c.FILEPATH) # ugly way to reload the whole layout but works
        i += 1
    print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))



def route_all():
    """Return the amount of net we routed successfully
    1. route source to any possible sink
    2. route from sink backwards to any possible path
    """
    layout.sort_netlist()
    routed_net_count = 0
    for net in layout.netlist:
        print("-----------------routing net {} -----------------".format(net.net_num))
        net.sort_sinks()

        if len(net.sinks) <=1:
            yield from route_a_star(net.src, net.sinks[0]) # a*
        else: # lee-moore
            yield from route_LeeMoore(net.src)
            
            for sink in net.sinks:
                if sink.is_sink_used():
                    # print("{} conneted. skip to next sink".format(sink))
                    continue
                yield from route_LeeMoore(sink)

        if net.is_routed():
            routed_net_count += 1
    # update_annotations(filename, routed_net_count)
    print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))
    return routed_net_count

# use permutation instead
def route_with_permutation(timeout = float("inf")): # if parsing timeout, force it exit if routing too many time. 
    max_routed_net_count = 0
    perm_netlist = permutations(layout.netlist)
    # final_routing = None # store the routing result when max_routed_net_count
    i = 0
    for net_list_p in list(perm_netlist):
        routed_net_count = 0
        print("================================route trial time #{} ================================".format(i))
        for net in net_list_p:
            if len(net.sinks) <=1:
                yield from route_a_star(net.src, net.sinks[0]) # a*
            else: # lee-moore
                yield from route_LeeMoore(net.src)
                
                for sink in net.sinks:
                    if sink.is_sink_used():
                        # print("{} conneted. skip to next sink".format(sink))
                        continue
                    yield from route_LeeMoore(sink)

            if net.is_routed():
                routed_net_count += 1
            max_routed_net_count = max(max_routed_net_count, routed_net_count)
            if routed_net_count == len(layout.netlist): 
                print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))
                return
        layout.reset_grid()
        reload_layout(c.FILEPATH) 
        i += 1
        if i >= timeout: break
        
        print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))
    # layout.reset_grid()
    # reload_layout(c.FILEPATH) # ugly way to reload the whole layout but works
    
    
    print("routed: {}/{}".format(max_routed_net_count, len(layout.netlist)))
    