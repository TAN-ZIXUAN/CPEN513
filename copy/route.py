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
            # cell.connected = False
            cell.visited = False
# def clear_path(grid, start, g):
#     while True:
#         g.connected = False
#         # don't modify content for source and sink
#         if not (g.is_source()) and (not g.is_sink()):
#             print("clear grid", g)

#             g.net_num = 0
#             g.content = 'empty'
#         if g is start:
#             break
#         g = g.prev
#     g.prev = None
            
    
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
    # random.shuffle(locs) 
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
def route_segment(start):
    counter = 0 # for priorityqueue (priority, counter, object)

    print("expanding from {}".format(start))

    expansion_list = PriorityQueue()
    label = 1
    start.set_label(label)
    expansion_list.put((label,counter, start)) #(priority, thing)

    while not expansion_list.empty():
        
        g = expansion_list.get()[2]


        # exit the loop if we reach a target or wire
        if (start.is_source()) and (g.is_sink()) and (g.net_num == start.net_num):
            g.sink_used = True
            print("src reaches a sink", g)
            break
        if (g.is_connected()) and (g.net_num == start.net_num) and (
                g is not start):
            print("sink reaches an existing wire or src")
            break
        neighbours = get_neighbours(g, start.net_num)
        for neighbour in neighbours:
            
            neighbour.visited = True
            c.COLOR_GRID[neighbour.row][neighbour.col] = c.COLOR_VIS

            if neighbour.label == 0:
                neighbour.dist_from_src = g.dist_from_src + 1
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
        layout.reset_grid()
        print("-------------------couldn't route segment!-----------------")
        print("clear grid")
        clear_visited(layout.grid)
        # clear_path(layout.grid, start, g)
        g.routable = False

        yield False

    # traceback():
    # - start at taget, walk back along prev cells
    logging.info("routed segment!")
    while True and g.is_routable():
        print("tracing back")
        g.connected = True
        # don't modify content for source and sink
        if not (g.is_source()) and (not g.is_sink()):
            g.net_num = start.net_num
            g.content = 'net'
        if g is start:
            break
        g = g.prev

    # clear labels of empty cells, update colours
    layout.reset_grid()
    clear_visited(layout.grid)
    # clear_path(layout.grid)
    # print("-----------path found ----------------")
    yield True
    



def route():
    layout.sort_netlist() # sort before routing
    nets_routed = 0
    for net in layout.netlist:
        logging.info("routing net {}...".format(net.net_num))

        # sort sinks by estimated distance to source
        # net.sort_sinks()

        # route from source to "closest" sink
        yield from route_segment(net.source)

        # for multiple sinks: expand around sink looking for connection to net
        if len(net.sinks) > 1:
            logging.info("net {} has multiple sinks".format(net.net_num))
            print("net {} has multiple sinks".format(net.net_num))
            for sink in net.sinks:
                if sink.is_sink_used():
                    print("conneted skip to next sink", sink)
                    continue
                yield from route_segment(sink)

        if net.is_routed():
            nets_routed = nets_routed + 1

route()
    