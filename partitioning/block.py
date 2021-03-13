import heapq
class Block:
    """
    There exists two blocks for bi-partition
    Attributes:
    nodes: a set that stores the nodes belongs to current block
    unlocked_nodes: a list that stores the unlocked nodes in current block. it is heapified as max heap.

    """
    def __init__(self):
        self.nodes = set() # a set of node representing by id
        self.unlocked_nodes = []
    
    def __str__(self):
        nodes = list(self.nodes)
        # nodes_id = [node.node_id for node in nodes]
        nodes_id = [(node.node_id,node.gain) for node in nodes]
        # unlocked_nodes_id = [(node.node_id, node.gain )for node in self.unlocked_nodes]
        # return "{} unlocked{}".format(nodes_id, unlocked_nodes_id)
        return "{}".format(nodes_id)

    def clear_block(self):
        """"clear all the nodes stores in the block"""
        self.nodes = set()
        self.unlocked_nodes = []

    def get_size(self):
        """return the number of the nodes in the block"""
        return len(self.nodes)

    def add_node(self, node):
        """add a node into the block (add it to self.nodes)
        if the nodes is unlocked. we also push it into the heapq that stores the unlocked nodes
        """
        if node.is_unlocked():
            heapq.heappush(self.unlocked_nodes, node)
        self.nodes.add(node)
        # print("len_nodes", len(self.nodes))
        # print("len_unlocked_nodes", len(self.unlocked_nodes))

    def remove_node(self, node):
        """remove a node from the block"""
        self.nodes.remove(node)
        self.unlocked_nodes.remove(node)
        
    def has_unlocked_nodes(self):
        """return True if it has unlocked nodes in it else return False"""
        return len(self.unlocked_nodes) != 0

    def pop_max_gain_node(self):
        """pop out the node with max gain from unlocked_nodes"""
        max_gain_node = heapq.heappop(self.unlocked_nodes) # index error raised if list is empty
        self.nodes.remove(max_gain_node)
        print("move node({},{})".format(max_gain_node.node_id, max_gain_node.gain))
        return max_gain_node
    
    def get_max_gain(self):
        """return the nodes with max gain
        unlocked_nodes is max heap. we get the max_gain node without removing it
        """
        # print("get max gain",self.unlocked_nodes[0])
        return self.unlocked_nodes[-1]    # error should be raised if list is empty
            
    def has_node(self, node):
        """return True if the block has nodes in it else False"""
        return node.node_id in self.nodes

    def save_copy(self):
        """save a copy of set that stores the nodes in the block"""
        return self.nodes.copy()
        
