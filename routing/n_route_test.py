import pytest
import sys
# from n_route import route_all
from n_route import route_with_shuffle
from n_route import route_with_permutation
from n_route import route_LeeMoore
from n_route import route_a_star

from layout import Layout
from cell import Cell
from net import Net
import config as c

layout = Layout()

def load_file(file_path):
    loaded_file = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            loaded_file.append((line.strip().split()))

    
    # convert string to integer
    file = loaded_file
    # print(file)
    for i in range(len(file)):
        for j in range(len(file[i])):
            file[i][j] = int(file[i][j])

    # print("loaded_file", file)
    cols, rows = file[0][0], file[0][1]
    layout.init_grid(rows, cols)
    num_obs= file[1][0]

    for i in range(num_obs):
        col = file[2 + i][0]
        row =  file[2 + i][1]
        cell = layout.grid[row][col]
        cell.row = row
        cell.col = col
        cell.type = 'obs'

    layout.netlist = []
    num_wires = file[2 + num_obs][0]

    for i in range(num_wires):
        net_num = i + 1 # nets are numbered from 1

        num_pins = file[2 + num_obs + 1 + i][0]
        col = file[2 + num_obs + 1 + i][1]
        row = file[2 + num_obs + 1 + i][2]
        source = layout.grid[row][col]
        source.type = 'src'
        source.connected = True
        source.net_num = net_num

        # next items are x, y coordinates of sinks
        sinks = []
        tmp = 0
        for j in range(num_pins-1):
            col = file[2 + num_obs + 1 + i][3 + j + tmp]
            row = file[2 + num_obs+ 1 + i][4 + j + tmp]
            sink = layout.grid[row][col]
            sink.type = 'sink'
            sink.net_num = net_num
            sink.est_dist_from_src = sink.estimate_dist(source)
            sinks.append(sink)
            tmp += 1

        layout.netlist.append(Net(net_num, num_pins, source, sinks))




file_name = ["example.infile", "impossible.infile", "impossible2.infile", "kuma.infile", "misty.infile", "oswald.infile", "rusty.infile", "stanley.infile", "stdcell.infile", "sydney.infile"]
expected = [3, 3, 3, 6, 5, 1, 4, 5, 18 ,3]

def route_all_at_file(file_path):
    load_file(file_path)
    return route_all()
test = []
for i in range(len(file_name)):
    test.append(("benchmarks/" + file_name[i], expected[i]))
print(test)


# @pytest.mark.parametrize("test_input, expected", test)
# def test_route_all(test_input, expected):
#   assert route_all_at_file(test_input) == expected
def route_all():
    """Return the amount of net we routed successfully
    1. route source to any possible sink
    2. route from sink backwards to any possible path
    """
    layout.sort_netlist()
    routed_net_count = 0
    routed_segment = 0
    for net in layout.netlist:
        # print("-----------------routing net {} -----------------".format(net.net_num))
        net.sort_sinks()
        if route_LeeMoore(net.src): routed_segment += 1
        if(len(net.sinks) > 1):
            # print("routing from sinks of net {}".format(net.net_num))
            for sink in net.sinks:
                if sink.is_sink_used():
                    # print("{} conneted. skip to next sink".format(sink))
                    continue
                if route_LeeMoore(sink): routed_segment += 1

        if net.is_routed():
            routed_net_count += 1
    # print("routed: {}/{}".format(routed_net_count, len(layout.netlist)))
    return routed_segment

load_file("benchmarks/" + "example.infile")
print(route_all())
