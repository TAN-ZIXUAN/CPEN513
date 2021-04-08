class Node:
    """node need to be placed on chips

    Attributes:
    node_id: id of the node. starting from 0
    block_id: the id of the bock that node belongs to. 0 or 1
    gain: gain of the current node. gain = # incident edges that cross partition - # incident edges that do not
    status: 0 unlocked, 1 locked
    nets: list of nets that the node are in
    rect: for python gui
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.block_id = None
        self.gain = 0
        self.status = 0 # 0 unlocked, 1 locked
        self.nets = []
        self.rect = None
        

    def __str__(self):
        return 'node {node_id} (gain={gain}, block id={block})'.format(node_id=self.node_id, gain=self.gain, block = self.block_id)

    def is_unlocked(self):
        return self.status == 0

    def lock_node(self):
        self.status = 1
    
    def unlock_node(self):
        self.status = 0

    def modify_gain(self, delta):
        pass
        
    
    def get_rect_center(self, canvas):
        """Returns (x, y) coordinates of center of Site's canvas rectangle."""
        x1, y1, x2, y2 = canvas.coords(self.rect) # get rect coords
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return (center_x, center_y)
    
    def __lt__(self, other):
        return self.gain > other.gain

        


