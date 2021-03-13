class Edge:
    """" edge that connects two nodes"""
    def __init__(self, u_node, v_node):
        self.u_node = u_node
        self.v_node = v_node
    
    def iscut(self):
        return self.u_node.block_id != self.v_node.block_id
    
    