import logging
import random

from node import Node
from net import Net
from block import Block
from collections import defaultdict

def create_hex_color_list(color_file="hex_color.txt"):
    """return hex color list"""
    hex_colors = [] # 949 colors 
    with open(color_file, 'r') as f:
        for line in f:
            l = line.strip().split()
            # print(line[-1])
            hex_colors.append(l[-1])

    return hex_colors

class Chip:
    """ chip consists of node sites.

    Attributes:
    num_nodes: number of nodes
    num_connections: number of connections
    netlist: netlist of the chip
    node_list: list of nodes that should be placed on the chip
    graph: a dict stores the connections between nodes. index: node, value:a list of node that the index node connects to 
    cut_size: cut size
    min_cutsize: stores the min cutsize of the chip
    best_partition: stores the best partition
    blocks: an list that store block0 and block1 objects [block0, block1]
    """

    def __init__(self):
        # number of nodes placed the chip (the number of nodes need to be placed on the chip)
        self.num_nodes = 0
        self.num_connections = 0 # number of connections
        self.netlist = []
        self.node_list = []  # list of nodes
        self.graph = defaultdict(set)
        self.graph_id = defaultdict(set)
        self.edges = {} # key: frozentset(node_1, node_2)  value: true-iscut, fasle - not cut 
        self.cutsize = 0
        self.min_cutsize = None
        self.best_partition_copy = None
        self.blocks = [Block(), Block()]

    def __str__(self):
        s = """{}
        block0:{}
        block1:{}
        """.format(self.cutsize, self.blocks[0], self.blocks[1])
        return s

    def clear_blocks(self):
        self.blocks = [Block(), Block()]
    def init_netlist(self):
        """"init netlist as an empty list"""
        self.netlist = []

    def init_node_list(self, num_nodes):
        """construct node_list as a list contains Node object"""
        self.node_list = [Node(node_id) for node_id in range(num_nodes)]

    def init_net_partitions(self):
        """init every net's partition
        build the net.partitions: [# of node in block 0, # of ndoe in block 1]
        """
        for net in self.netlist:
            net.init_partitions()

    def calc_cutsize(self):
        """"calculate the ut size and return it"""
        cutsize = 0
        for edges in self.edges:
            if self.edges[edges] == True: # is cut
                cutsize += 1
        # for net in self.netlist:
        #     if net.iscut():
        #         cutsize += 1
        # # self.cutsize = cutsize
        return cutsize

    def get_max_net_size(self): # max number of pins on node
        """return the max net size among all nodes"""
        max_net_size = 0
        for node in self.node_list:
            net_size = len(node.nets)
            if net_size > max_net_size:
                max_net_size =net_size

        return max_net_size

    def has_unlocked_nodes(self): 
        """return True if it has unlocked nodes in it else return False"""
        return self.blocks[0].has_unlocked_nodes() or self.blocks[1].has_unlocked_nodes()

    def unlock_all_nodes(self):
        for node in self.node_list:
            node.unlock_node()

    def calc_all_gains(self):
        for node in self.node_list:
            if node.is_unlocked(): # calc gains of unlocked nodes
                node.gain = 0
                from_block = node.block_id
                to_block = (node.block_id + 1) % 2
                for node in self.graph:
                    for nei in self.graph[node]:
                        if nei.block_id == to_block:
                            node.gain += 1
                        if nei.block_id == from_block:
                            node.gain -= 1
                
    
    def save_partition(self):
        """save and return partition result"""
        block0 = list(self.blocks[0].save_copy())
        block1 = list(self.blocks[1].save_copy())
        return [block0, block1]
    
    def buid_graph(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)
    def build_graph_id(self, u_id, v_id):
        self.graph_id[u_id].add(v_id)
        self.graph_id[v_id].add(u_id)
    def buid_edges(self, u_node, v_node):
        dict_key = frozenset((u_node, v_node))
        value = u_node.block_id != v_node.block_id # True: is cut, False: not cut
        self.edges[dict_key] = value

    def parse_chip_file(self, filepath = "ass3_files/cm82a.txt"):
        """parse the chip file"""
        # self.init_grid()
        print("load {}".format(filepath))
        self.init_netlist()
        # self.init_node_list()
        with open(filepath, 'r') as f:
            for line_num, l in enumerate(f):
                line = l.strip().split()
                if not line: # be careful about empty lines
                    break
                # print("{} {}".format(line_num, line))
                if line_num == 0: # first line: num_nodes, num_connections, num_rows, num_cols
                    self.num_nodes = int(line[0])
                    self.init_node_list(self.num_nodes)
                    self.num_connections = int(line[1])
                    # assign block numbers:
                    random_nodelist = random.sample(range(self.num_nodes), self.num_nodes)
                    for i, node_id in enumerate(random_nodelist):
                        node = self.node_list[node_id]
                        node.block_id = random.choice([0, 1])# randomly(also equally) assign them block 0 or 1

                else: # the rest of lines (contains netlist)
                    
                    net = Net()
                    net_num = line_num - 1 # net number starting from 0
                    net.net_id = net_num
                    # print("loading net", net_num)
                    hex_colors = create_hex_color_list()
                    net.color = hex_colors[net_num % len(hex_colors)] # TODO: create a color list from hex_color.txt
                    # num_nodes_of_net = line[0]  # number of nodes in current net
                    
                    # node_id
                    u_node_id = int(line[1])
                    u_node = self.node_list[u_node_id]
                    # u_node.block_id = random.choice([0, 1]) # randomly assign block id to node
                    for item in line[2:]:
                        v_node_id = int(item)
                        v_node = self.node_list[v_node_id]
                        self.buid_graph(u_node, v_node)
                        self.build_graph_id(u_node_id, v_node_id)
                        self.buid_edges(u_node, v_node)
                        
                    for item in line[1:]:
                        node_id = int(item)
                        node = self.node_list[node_id]
                        # print(node.__str__())
                        node.nets.append(net)
                        net.nodes.append(node)

                    self.netlist.append(net)




                    





