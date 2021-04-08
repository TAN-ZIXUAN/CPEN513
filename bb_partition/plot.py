import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import numpy as np
import math
# from simple_term_menu import TerminalMenu  # not support windows
def plot(file_name, num_nodes, netlist, best_assignment, best_cutsize):

    
    fig, ax = plt.subplots()
    ax.set_title("{} cutsize:{}".format(filename, best_cutsize))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    # rect = patches.Rectangle((0, 0), 300, 300, linewidth = 2, edgecolor = 'black', fill = "blue")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # ax.spines['left'].set_position('center')
    ax.set_aspect('equal')
    ax.autoscale_view()



    left = best_assignment[0]
    right = best_assignment[1]
    max_nodes_per_side = num_nodes // 2 + 2
    num_rows = max_nodes_per_side if max_nodes_per_side <= 16 else math.ceil(math.sqrt(max_nodes_per_side))
    num_cols = 1 if max_nodes_per_side <= 16 else math.ceil(max_nodes_per_side / num_rows) + 1
    m = [[np.nan] * (2 * num_cols + 1) for _ in range(num_rows)]

    node_coord = [None]*num_nodes
    for idx, node in enumerate(left):
        i = idx // num_cols
        j = idx % num_cols
        m[i][j] = node
        node_coord[node] = [i,j]
        ax.text(j, i, str(m[i][j]), va='center', ha='center')
    for idx, node in enumerate(right):
        i = idx // num_cols
        j = idx % num_cols + num_cols + 1
        m[i][j] = node
        node_coord[node] = [i,j]
        ax.text(j, i, str(m[i][j]), va='center', ha='center')
    ax.matshow(m)

    for net in netlist:
        src = net[0]
        sinks = net[1:]
        for sink in sinks:
            x = [node_coord[src][0], node_coord[sink][0]]
            y = [node_coord[src][1], node_coord[sink][1]]
            ax.plot(y, x)
    plt.show()
    fig.savefig("figs/" + filename)

best_assignment = [[0, 1, 2, 3, 6, 7, 8, 14, 16, 19, 21, 22, 23, 24, 25, 27, 32, 34, 36], [4, 5, 9, 10, 11, 12, 13, 15, 17, 18, 20, 26, 28, 29, 30, 31, 33, 35]]
num_nodes = 37
netlist = [[0, 27], [1, 8], [11, 28, 13], [35, 28, 13, 31, 20], [4, 17, 28, 13], [33, 31, 20], [16, 22], [7, 14], [10, 26, 13], [9, 17, 30, 29], [2, 36, 34, 3], [23, 21, 34], [24, 34], [12, 17, 30, 29], [36, 32], [21, 19], [6, 25], [17, 5], [18, 15], [8, 36], [30, 36, 21, 6], [13, 36, 34, 3], [22, 21], [3, 21], [14, 6], [34, 6], [26, 18], [27, 18], [28, 8, 22, 14, 26, 27, 30], [29, 8, 22, 14, 26, 27], [20, 8, 22, 14, 27], [31, 26, 30]]
filename = "con1"
best_cutsize = 4
plot(filename, num_nodes, netlist, best_assignment, best_cutsize)  