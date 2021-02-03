from queue import PriorityQueue
import random
import logging
from layout import Layout
from cell import Cell
from net import Net
import config as c

logging.basicConfig(filename='router.log', filemode='w', level=logging.INFO)

layout = Layout()


def clear_visited(grid): # call this when ever start a new routing
    (rows, cols) = (len(grid), len(grid[0]))
    for i in range(rows):
        for j in range(cols): 
            cell = grid[i][j]
            cell.visited = False
def get_neighbours(cell, net_num):
    """Return a list of neighbours of a given cell.
    
    Arguments:
    cell - the Cell instance for which to find neighbours
    net_num - the net number of the Net instance we are routing

    Does not include neighbour Cells that contain obstacles or cells that
    belong to other nets."""
    # list to return
    neighbours = []

    # coordinates of possible neighbours
    locs = [{'row' : cell.row,   'col' : cell.col-1}, # north
            {'row' : cell.row+1, 'col' : cell.col},   # east
            {'row' : cell.row,   'col' : cell.col+1}, # south
            {'row' : cell.row-1, 'col' : cell.col}]   # west
    
    # get neighbours in random order
    random.shuffle(locs) 
    for loc in locs:
        # check bounds of possible neighbours
        if (0 <= loc['row'] < layout.rows) and (0 <= loc['col'] < layout.cols):
            cell = layout.grid[loc['row']][loc['col']]
            # don't consider obstacles
            if cell.is_obstacle():
                continue
            # don't consider cells that belong to other nets
            if cell.net_num not in [0, net_num]:
                continue
            neighbours.append(cell)

    return neighbours
def route_segment(start, target = None):
    # print("routing from",start)
    # print("routing to", target)
    counter = 0 # for priorityqueue (priority, counter, object)
    
    if target == None:
        algorithm = 'Lee-Moore'
        logging.info("expanding sink {}".format(start))
        print("expanding sink {}".format(start))
    else:
        algorithm = 'A*'
        logging.info("routing {} to {}".format(start, target))
        print("routing {} to {}".format(start, target))

    expansion_list = PriorityQueue()

    # set start label according to algorithm
    if algorithm == 'A*':
        # A*: start label is estimated distance to target
        label = start.estimate_dist(target)
    else:
        label = 1
    start.set_label(label)
    expansion_list.put((label,counter, start)) #(priority, thing)

    # while expansion list is not empty:
    while not expansion_list.empty():
        # g = grid in expansion list with smallest label
        
        g = expansion_list.get()[2]
        

        logging.debug('expanding on {}'.format(g))

        # for A*: if g is the target, exit the loop
        if algorithm == 'A*':
            if g is target:
                break
        # for Lee-More: if we reach a matching net, exit the loop
        else:
            if (g.is_connected()) and (g.net_num == start.net_num) and (
                    g is not start):
                break
        # for all neighbours of g:
        neighbours = get_neighbours(g, start.net_num)
        for neighbour in neighbours:
            # print(neighbour)
            neighbour.visited = True
            c.COLOR_GRID[neighbour.row][neighbour.col] = c.COLOR_VIS
            # if neighbour is unlabelled:
            if neighbour.label == 0:
                neighbour.dist_from_src = g.dist_from_src + 1
                if algorithm == 'A*':
                    # label neighbour with dist from start + estimate of dist to go
                    label = neighbour.dist_from_src + neighbour.estimate_dist(target)
                else: # Lee-More
                    # label neighbour with distance from start
                    label = neighbour.dist_from_src
                neighbour.set_label(label)
                # set previous cell of neighbour to current cell
                neighbour.prev = g
                # add neighbour to expansion list
                counter += 1
                expansion_list.put((neighbour.label, counter,neighbour))
        yield # show routing progress

    # if loop terminates without hitting target, fail
    else:
        logging.info("couldn't route segment!")
        print("couldn't route segment!")
        # layout.reset_grid()
        clear_visited(layout.grid)
        yield  False

    # traceback():
    # - start at taget, walk back along prev cells
    logging.info("routed segment!")
    while True:
        g.connected = True
        # don't modify content for source and sink
        if not (g.is_source()) and (not g.is_sink()):
            g.net_num = start.net_num
            g.content = 'net'
        if g is start:
            
            break
        g = g.prev

    # clear labels of empty cells, update colours
    # layout.reset_grid()
    clear_visited(layout.grid)
    print("-----------path found ----------------")
    yield True
    



def route():
    layout.sort_netlist() # sort before routing
    nets_routed = 0
    for net in layout.netlist:
        logging.info("routing net {}...".format(net.net_num))

        # sort sinks by estimated distance to source
        net.sort_sinks()

        # route from source to "closest" sink
        yield from route_segment(net.source, net.sinks[0])

        # for multiple sinks: expand around sink looking for connection to net
        if len(net.sinks) > 1:
            logging.info("net {} has multiple sinks".format(net.net_num))
            for sink in net.sinks[1:]:
                route_segment(sink)

        if net.is_routed():
            nets_routed = nets_routed + 1

route()
    