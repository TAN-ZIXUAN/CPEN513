import operator
import logging

class Net:
    """ part of the netlist

    Attributes:
    nodes: contains the nodes belongs to the net
    color: color of net line (border color of grid)
    net_id: id of net, starting from 0
    partitions: an list that stores the number of nodes in 2 blocks. [# of nodes in block0, # of nodes in block1]
    """

    def __init__(self):
        self.nodes = [] # contains the nodes(node object) inside this net
        self.color = 'black'
        self.partitions = [0,0] # number of nodes in block 0 and 1

    def __str__(self):
        node_id = [node.node_id for node in self.nodes]
        return "node: {}, partitions: {}".format(node_id, self.partitions)

    def init_partitions(self):
        """init list partitions
        iterate node in the net, calculate the number of nodes in each block and update self.partitions
        """
        self.partitions = [0, 0]
        for node in self.nodes:
            self.partitions[node.block_id] += 1
            
    def iscut(self):
        """return True if the net is cut else False
        the net is cut if the net has nodes distributed both in block 0 and 1
        """
        return (self.partitions[0] > 0) and (self.partitions[1] > 0)






