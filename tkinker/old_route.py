import random
from layout import Layout
from cell import Cell

layout = Layout()

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
    locs = [{'x' : cell.x,   'y' : cell.y-1}, # north
            {'x' : cell.x+1, 'y' : cell.y},   # east
            {'x' : cell.x,   'y' : cell.y+1}, # south
            {'x' : cell.x-1, 'y' : cell.y}]   # west
    
    # get neighbours in random order
    random.shuffle(locs) 
    for loc in locs:
        # check bounds of possible neighbours
        if (0 <= loc['x'] < layout.xsize) and (0 <= loc['y'] < layout.ysize):
            cell = layout.grid[loc['y']][loc['x']]
            # don't consider obstacles
            if cell.is_obstacle():
                continue
            # don't consider cells that belong to other nets
            if cell.net_num not in [0, net_num]:
                continue
            neighbours.append(cell)

    return neighbours


def route_segment(start, target=None):
    """Route a single segment from start cell to optional target.
    
    If a target is given, uses A* algorithm to find a route between start
    and target. If no target is given, start is assumed to be a net sink
    and Lee-Moore algorithm is run to expand out from the sink looking for
    cells already connected to the net.

    Returns True if net is successfully routed, False otherwise."""
    if target == None:
        algorithm = 'Lee-Moore'
        logging.info("expanding sink {}".format(start))
    else:
        algorithm = 'A*'
        logging.info("routing {} to {}".format(start, target))

    expansion_list = PriorityQueue()

    # set start label according to algorithm
    if algorithm == 'A*':
        # A*: start label is estimated distance to target
        label = start.estimate_dist(target)
    else:
        label = 1
    start.set_label(label)
    expansion_list.add(item=start, priority=start.label)

    # while expansion list is not empty:
    while not expansion_list.is_empty():
        # g = grid in expansion list with smallest label
        g = expansion_list.extract_min()

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
                expansion_list.add(item=neighbour, priority=neighbour.label)

    # if loop terminates without hitting target, fail
    else:
        logging.info("couldn't route segment!")
        layout.reset_grid()
        return False

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
    layout.reset_grid()

    return True


def parse_netlist(filepath):
    """Parse a netlist and populate the layout.grid.
    
    filepath - the full path of the netlist file to parse"""
    with open(filepath, 'r') as f:
        # first line is grid size
        line = f.readline().strip().split()
        xsize = int(line[0])
        ysize = int(line[1])
        layout.init_grid(xsize, ysize)

        # next lines are obstructed cells
        num_obstacles = int(f.readline().strip())
        for i in range(num_obstacles):
            line = f.readline().strip().split()
            xloc = int(line[0])
            yloc = int(line[1])
            cell = layout.grid[yloc][xloc]
            cell.x = xloc
            cell.y = yloc
            cell.content = 'obstacle'

        # next lines are wires to route
        layout.netlist = []
        num_wires = int(f.readline().strip())
        for i in range(num_wires):
            net_num = i + 1 # nets are numbered from 1

            line = list(map(int, f.readline().strip().split()))
            # first item in line is number of pins
            num_pins = line.pop(0)

            # second item is x, y coordinates of source
            xloc = line.pop(0)
            yloc = line.pop(0)
            source = layout.grid[yloc][xloc]
            source.content = 'src'
            source.connected = True
            source.net_num = net_num

            # next items are x, y coordinates of sinks
            sinks = []
            for j in range(num_pins-1):
                xloc = line.pop(0)
                yloc = line.pop(0)
                sink = layout.grid[yloc][xloc]
                sink.content = 'sink'
                sink.net_num = net_num
                sink.est_dist_from_src = sink.estimate_dist(source)
                sinks.append(sink)

            layout.netlist.append(Net(num_pins, source, sinks, net_num))


def open_benchmark(*args):
    """Function called when pressing Open button.
    
    Opens a dialog for user to select a netlist file, parses netlist
    file and sets up initial grid in the GUI."""

    # open a select file dialog for user to choose a benchmark file
    openfilename = filedialog.askopenfilename()
    # return if user cancels out of dialog
    if not openfilename:
        return

    logging.info("opened benchmark:{}".format(openfilename))
    filename.set(os.path.basename(openfilename))
    parse_netlist(openfilename)

    # reset the statsistics label
    stats_text.set("")

    # enable the Route button
    route_btn.state(['!disabled'])

    # initialize canvas with rectangles for layout
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    rw = cw // layout.xsize
    rh = ch // layout.ysize
    xoffset = (cw % rw) / 2
    yoffset = (ch % rh) / 2
    for row in layout.grid:
        for cell in row:
            x1 = cell.x * rw + xoffset
            x2 = x1 + rw + xoffset
            y1 = cell.y * rh + yoffset
            y2 = y1 + rh + yoffset
            cell.rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill='white')

            # colour cell and set text label
            cell.colourize()
            if cell.net_num != 0:
                # label source and sink
                cell.set_text()


def route(*args):
    """Function called when pressing Route button.

    Routes each net in the netlist."""
    # disable the Route button after starting routing
    route_btn.state(['disabled'])

    # route nets in netlist
    layout.sort_netlist() # sort before routing
    nets_routed = 0
    for net in layout.netlist:
        logging.info("routing net {}...".format(net.net_num))

        # sort sinks by estimated distance to source
        net.sort_sinks()

        # route from source to "closest" sink
        route_segment(net.source, net.sinks[0])

        # for multiple sinks: expand around sink looking for connection to net
        if len(net.sinks) > 1:
            logging.info("net {} has multiple sinks".format(net.net_num))
            for sink in net.sinks[1:]:
                route_segment(sink)

        if net.is_routed():
            nets_routed = nets_routed + 1

    # display stats
    stats_msg = "Routed {}/{} nets".format(nets_routed, len(layout.netlist))
    logging.info(stats_msg)
    stats_text.set(stats_msg)