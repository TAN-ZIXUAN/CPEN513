import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import numpy as np
import math
# from simple_term_menu import TerminalMenu  # not support windows
def plot(file_name, num_nodes, netlist, best_assignment, best_cutsize):

    
    fig, ax = plt.subplots()
    ax.set_title('''benchmark file: {}, net cutsize: {}'''.format(filename, best_cutsize))
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
def cal_net_cutsize(assignment):
    """ calculate the net cutsize of current assignment 
    Args: 
        assignment: an array represents the current assignment [[],[]]
    Return: net cutsize
    """
    cutsize = 0
    left = set(assignment[0])
    right = set(assignment[1])
    # fast way to check if a net is cut
    for net in netlist:
        if set(net).intersection(left) and set(net).intersection(right):
            cutsize += 1
    return cutsize
# replot twocm
# best_assignment = [[52, 10, 55, 13, 56, 15, 58, 59, 60, 18, 19, 62, 21, 64, 22, 65, 66, 67, 25, 69, 27, 28, 30, 31, 32, 34, 35, 36, 39, 40, 42, 2, 44, 4, 7], [50, 8, 51, 9, 53, 11, 54, 12, 14, 57, 16, 17, 61, 20, 63, 23, 24, 68, 26, 29, 33, 37, 38, 41, 0, 1, 43, 3, 45, 46, 5, 47, 6, 48, 49]]
# num_nodes = 70
# netlist = [[0, 50], [24, 53, 12, 47, 68, 49, 50, 6, 48], [46, 53, 12, 47, 68, 49, 50, 6, 48], [3, 26, 29, 61, 1], [33, 26, 29, 61, 1], [5, 45], [41, 12], [16, 53], [57, 53], [9, 12], [63, 68], [11, 47], [20, 47], [43, 68], [23, 48], [14, 6], [8, 6], [17, 48], [38, 50], [51, 49], [54, 49], [21, 10], [2, 66, 67, 60, 52, 62, 10, 64, 65], [59, 66, 67, 60, 52, 62, 10, 64, 65], [19, 56, 7, 58, 44], [13, 56, 7, 58, 44], [42, 15], [55, 67], [28, 66], [25, 66], [30, 67], [31, 52], [32, 60], [4, 60], [34, 52], [35, 65], [36, 64], [22, 64], [18, 65], [39, 10], [40, 62], [27, 69], [26, 37], [29, 37], [61, 37], [45, 37], [37, 62], [47, 26], [68, 26], [49, 29], [50, 29], [6, 61], [48, 61], [53, 45], [12, 45], [1, 45], [56, 27], [7, 27], [58, 27], [15, 27], [60, 56], [52, 56], [62, 7], [10, 7], [64, 58], [65, 58], [66, 15], [67, 15], [44, 15]]

# replot cc
best_assignment = [[53, 55, 14, 17, 60, 18, 61, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 32, 35, 36, 38, 39, 40, 41, 42, 3, 45, 47, 7, 49, 9], [52, 10, 11, 54, 12, 13, 56, 57, 15, 58, 16, 59, 21, 27, 31, 33, 34, 37, 0, 1, 43, 2, 44, 4, 46, 5, 6, 48, 8, 50, 51]]
num_nodes = 62
netlist = [[0, 25, 22, 3, 39, 34, 56], [43, 25, 47, 38, 26, 40, 51], [33, 34, 57], [28, 32, 45], [4, 46, 37], [5, 58, 52], [42, 24, 19], [31, 54], [41, 39], [9, 60], [10, 2], [20, 32], [12, 37], [13, 58], [14, 19], [15, 27, 8, 25, 47, 38, 26, 40], [16, 27, 8], [18, 25, 47, 38, 26, 40], [23, 24, 22], [35, 54, 22, 29, 2, 32, 37, 58, 19, 47, 38, 40, 39], [59, 54], [46, 6], [27, 11], [8, 48], [24, 49], [25, 29, 39, 7], [54, 1], [22, 53], [3, 36], [29, 55], [60, 30], [2, 21], [32, 17], [37, 44], [58, 50], [19, 61], [26, 54, 2, 32, 37, 58, 19], [47, 22, 60], [38, 3], [39, 3], [40, 60], [34, 2]]
filename = "cc"
best_cutsize = cal_net_cutsize(best_assignment)

plot(filename, num_nodes, netlist, best_assignment, best_cutsize)  