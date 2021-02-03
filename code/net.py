from cell import Cell

class Net:
    """
    class for net
    """
    def __init__(self, net_num, num_pins, src, sinks):
        self.net_num = net_num
        self.num_pins = num_pins
        self.src= src
        self.sinks = sinks
    
    def is_routed(self):  # True if all the sinks are connected
        for sink in self.sinks:
            if not sink.is_connected():
                return False
        return True
        # return all(sink.is_conneted() for sink in self.sinks)

    def sort_sinks(self): # sort sinks based on the mahattan disstance to the source
        tmp = sorted(self.sinks, key=lambda cell: cell.est_dist_from_src)
        self.sinks = tmp
    
