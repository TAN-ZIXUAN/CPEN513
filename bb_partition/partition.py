import random
import math
import os
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import numpy as np
from collections import defaultdict
# from simple_term_menu import TerminalMenu  # not support windows

"""
this is the branch and bound parition with "worst" intial best assignment(cutsize = len(netlist) + 1)
"""

def plot(filename, best_cutsize, best_assignment):
    """plot best assignment using matplot
    """
    fig, ax = plt.subplots()
    ax.set_title('''benchmark file: {}, net cutsize: {}'''.format(filename[:-4], best_cutsize))
    # hide ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
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
        ax.text(j, i, str(m[i][j]), va='center', ha='center', fontsize="large")
    for idx, node in enumerate(right):
        i = idx // num_cols
        j = idx % num_cols + num_cols + 1
        m[i][j] = node
        node_coord[node] = [i,j]
        ax.text(j, i, str(m[i][j]), va='center', ha='center', fontsize = "large")
    ax.matshow(m)

    for net in netlist:
        src = net[0]
        sinks = net[1:]
        for sink in sinks:
            x = [node_coord[src][0], node_coord[sink][0]]
            y = [node_coord[src][1], node_coord[sink][1]]
            ax.plot(y, x)
    plt.show()

    # save figure
    fig.savefig("figs/" + filename[:-4])



def parse_file(filepath):
    global netlist, num_nodes, num_nets
    # init netlist
    netlist = []
    with open(filepath, 'r') as f:
        for line_num, l in enumerate(f):
            line = l.strip().split()
            if not line: # be careful about empty lines
                break
            # print("{} {}".format(line_num, line))
            if line_num == 0: # first line: num_nodes, num_connections, num_rows, num_cols
                num_nodes = int(line[0])
                num_nets = int(line[1])
            
            else: # the rest of lines (contains netlist)
                nodes = []  # id of nodes in current net   
                for item in line[1:]:
                    node_id = int(item)
                    nodes.append(node_id)

                netlist.append(nodes)
    print(filepath)
    print("netlist",netlist)
    print("num_nodes", num_nodes)

# def is_net_cut(net, assignment):
#     """if the current net is cut
#     Args: 
#         net: an array with nodes in current net [node1, node2, node3]
#         assignment: current assignment
#     Return:
#         True if the net is cut (nodes appears in both left and right assignment)
#         False: net is not cut (all nodes are in a single side of the assignment)
#     """
#     left_cnt = 0
#     right_cnt = 0
#     left_assignment = assignment[0]
#     right_assignment = assignment[1]
#     if all(node in left_assignment for node in net) or all(node in right_assignment for node in net):
#         return False
#     else:
#         return True
#     # for node in net:
#     #     if left_cnt >= 1 and right_cnt >= 1: # stop checking the rest of nodes if the net is already cut
#     #         return True
#     #     # check left
#     #     if node in left_assignment:
#     #         left_cnt += 1
#     #     elif node in right_assignment:
#     #         right_cnt += 1
#     # return (left_cnt and right_cnt)

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

def check_partition(assignment, partition):
    """check if if we can place node in current side of partition. 
    we compare if the current assignment is balanced or not to determine if we can place the node in this side of partition 
    Args:
        assignment： assignment array [[],[]]
        partition: 0 -> check left partition. 1 - > check right partition
    Return:
        True: we can place node in this partition
        False: we cannot place node in this partition
    """
    avg = 0
    if num_nodes % 2 == 0:
        avg = num_nodes // 2
    else:
        avg = num_nodes // 2 + 1
    
    return len(assignment[partition]) < avg

def select_next_node(curr_node):
    """ select next node to assign
    Args:
        curr_node: id of curr_node
    Return: id of next node or None
    """
    if curr_node + 1 < num_nodes:
        return curr_node + 1
    elif curr_node + 1 == num_nodes:
        return None


def recursive_bb_partition(curr_assignment, node_to_assign, min_cutsize): 
    """Branch and Bound partition (recursivw)
    Args:
        curr_assignment: assignment array eg. [[node1, node2,..],[node3, node4,...]]
        node_to_assignment: a number represent the node to assign
        min_cutsize: minimum cutsize so far
    """
    global best_assignment, best_cutsize
    
    if node_to_assign == None:
        curr_cutsize = cal_net_cutsize(curr_assignment)
        if curr_cutsize < best_cutsize:
            best_cutsize = curr_cutsize
            best_assignment = curr_assignment
        print("best assignment: {}, current min_cutsize: {}".format(best_assignment, min_cutsize))

    else:
        tmp_cutsize = cal_net_cutsize(curr_assignment)
        if tmp_cutsize < min_cutsize:
            next_node = select_next_node(node_to_assign)
            # check left branch
            if check_partition(curr_assignment, 0):
                next_node = select_next_node(node_to_assign)
                tmp_assignment = [curr_assignment[0] + [node_to_assign], curr_assignment[1]] 
                # tmp_assignment[0].append(node_to_assign) 
                if (cal_net_cutsize(tmp_assignment) < best_cutsize):
                    recursive_bb_partition(tmp_assignment, next_node, best_cutsize)

            # check right branch
            if check_partition(curr_assignment, 1):
                next_node = select_next_node(node_to_assign)
                tmp_assignment = [curr_assignment[0], curr_assignment[1] + [node_to_assign]] 
                # tmp_assignment[1].append(node_to_assign)
                if (cal_net_cutsize(tmp_assignment) < best_cutsize):
                    recursive_bb_partition(tmp_assignment, next_node, best_cutsize)



def list_files(directory="ass3_files/"):
    file_list =  [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return file_list
def consol_menu(select_list):
    # menu = SelectionMenu(list_files(), "Select a benchmark file")
    return SelectionMenu.get_selection(select_list, title="Select a benchmark file")


if __name__ == "__main__":
    # some global variables storing info from benchmark files
    netlist = []
    num_nets = 0
    num_nodes = 0
    
    # for terminal menu
    directory = "ass3_files/"
    file_list = list_files(directory)
    filename = file_list[consol_menu(file_list)]
    filepath = directory + filename
    
    parse_file(filepath)

    # for storing best assignment
    best_assignment = []
    # initial assignment, node to assign and cutsize
    assignment = [[], []]  # todo using dictionary to save time
    # assignment = defaultdict(int)
    # best_assignment = assignment
    node_to_assign = 0
    best_cutsize = num_nets + 1 # initial min_cutsize

    recursive_bb_partition(assignment, node_to_assign, best_cutsize)

    print('''
    FINAL best assignment: {}
    best_cutsize: {}
    '''.format(best_assignment, best_cutsize))
    # print("netlist", netlist)
    plot(filename, best_cutsize, best_assignment)
    



    






