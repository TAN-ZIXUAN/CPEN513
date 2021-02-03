from cell import Cell

class Net:
    """Class representing a net."""

    def __init__(self, num_pins, source, sinks, net_num):
        self.num_pins = num_pins
        self.source = source
        self.sinks = sinks
        self.net_num = net_num

    def __str__(self):
        return "Net(pins=%s, src=%s, sinks=%s, net=%s)" % (
                self.num_pins, self.source, self.sinks, self.net_num)

    def is_routed(self):
        """Returns True if all sinks are connected."""
        for sink in self.sinks:
            if not sink.is_connected():
                return False
        return True

    def sort_sinks(self):
        """Sort list of sinks based on estimated segment length.
        
        Use Manhatten distance to the net source as the estimate of
        segment length."""
        tmp = sorted(self.sinks, key=lambda cell: cell.est_dist_from_src)
        self.sinks = tmp