import sys
from layout import Layout
from cell import Cell
from net import Net
import config as c
layout = Layout()
def load_file(filepath):
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



#load file
default_file = "benchmarks/example.infile"
if len(sys.argv) < 2: # not parsing file argument. use default file
    print("please put file path as argument[1]")
    print("default file loaded", default_file)
    file_path = default_file
else:
    file_path= sys.argv[1] # file name or path
    print("loaded file", file_path)
if not file_path:
    print("no file selected!") 
    sys.exit()
c.FILEPATH = file_path
# load_file(file_path)


def run(file_path):
    load_file(file_path)
