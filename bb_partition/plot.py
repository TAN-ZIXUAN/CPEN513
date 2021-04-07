import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import numpy as np
import math
# from simple_term_menu import TerminalMenu  # not support windows


best_assignment = [[0, 1, 2, 4, 6, 11], [3, 5, 7, 8, 9, 10]]
num_nodes = 12
netlist = [[3, 5, 8], [9, 5, 8], [10, 5, 8], [6, 0, 11], [4, 0, 11], [5, 7], [0, 2], [11, 1], [8, 0, 11]]     
fig, ax = plt.subplots()
# ax.set_title("{} cutsize:{}".format(filename, best_cutsize))
ax.set_xticks([])
ax.set_yticks([])
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
for node in left:
    i = node % num_rows
    j = node % num_cols
    m[i][j] = node
    node_coord[node] = [i,j]
    ax.text(j, i, str(m[i][j]), va='center', ha='center')
for node in right:
    i = node % num_rows
    j = node % num_cols + num_cols + 1
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