def parse_netlist(filepath):
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
        num_obstacles = int(f.readline().strip())
        for i in range(num_obstacles):
            line = f.readline().strip().split()
            col = int(line[0])
            row = int(line[1])
            cell = layout.grid[row][col]
            cell.row = row
            cell.col = col
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
            col = line.pop(0)
            row = line.pop(0)
            source = layout.grid[row][col]
            source.content = 'src'
            source.connected = True
            source.net_num = net_num

            # next items are x, y coordinates of sinks
            sinks = []
            for _ in range(num_pins-1):
                col = line.pop(0)
                row = line.pop(0)
                sink = layout.grid[row][col]
                sink.content = 'sink'
                sink.net_num = net_num
                sink.est_dist_from_src = sink.estimate_dist(source)
                sinks.append(sink)

            layout.netlist.append(Net(num_pins, source, sinks, net_num))

        c.COLOR_GRID = color_grid(layout)
        print(c.COLOR_GRID)

