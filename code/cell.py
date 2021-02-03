class Cell:
    """
    we parse the benchmark file and form a grid of cells(rows * cols). 

    row, col: the position of the cell in the grid: grid[row][col]
    net_num: indicates which network the cell belongs to
    label: represents the cost used in routing algorithms (Lee-Moore or A*)
    cost_from_source: the cost or actual distance from source to current cell

    type:indicates the type of current cell: empty, src, sink, obs("obstacle")

    prev: used for backtracing when forming a path
    visited: mark the cell as "visited" when we exploring the grid
    
    connected: True if the cell is connected to the source
    sink_used: mark as True if the current cell is sink and is alreadt connected
    routable: mark as False when routing failed
    

    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.net_num = 0
        self.label = 0
        self.cost_from_src = 0
        self.type = "empty"
        self.prev = None

        self.visited = False
        
        self.connected = False
        self.sink_used = False
        self.routable = True

        self.est_dist_from_src = 0

    def is_visited(self):
        return self.visited
    
    def is_obs(self): # if it's a obstacle
        return self.type == "obs"
    
    def is_sink(self):
        return self.type == "sink"
    
    def is_src(self):
        return self.type == "src"
    
    def is_connected(self):
        return self.connected
    
    def is_sink_used(self):
        return self.sink_used

    def is_routable(self):
        return self.routable

    def set_label(self, label):
        self.label = label

    def clear_label(self):
        self.set_label(0)
    
    def estimate_dist(self, target):
        """Return the Manhatten distance between current and target Cells"""
        return abs(self.row - target.row) + abs(self.col - target.col)
    