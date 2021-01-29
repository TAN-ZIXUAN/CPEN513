import config as c
from queue import PriorityQueue
import collections

# create a queue to store sinks by dist ranking

# given a wire number, return a sorted sink2dist dictionary {sink：dist}
def rankSinkByDist(wire): # rank sink routing order by its distance to source. not work well if there is obs block all the possible paths for a sink 
    (src_x, src_y) = c.WIRE2SOURCE[wire] 
    sinks = c.WIRE2SINK[wire] # eg[(6, 5), (6, 8)]
    sink2dist = {} 
    for sink_x, sink_y in sinks:
        dist = abs(src_x - sink_x) + abs(src_y - sink_y)
        sink2dist[(sink_x, sink_y)] = dist

    # rank/sort sink by dist (close to far)
    sorted_sink2dist = dict(sorted(sink2dist.items(), key = lambda item: item[1]))
    return sorted_sink2dist


    
def rankWireByPins():
    pass


# Dijkstra algorithm (not A* bc we don't know which sink we are going to route) # maybe we can route closest node first
def routeSource2Sink(grid,wire): # single source to single sink routing. route the source of the wire to any of its sink
    (src_x, src_y)  = c.WIRE2SOURCE[wire] #(x, y)
    visited = {}

    num_x = len(grid)
    num_y = len(grid[0])

    count = 0
    open_set = PriorityQueue()

    predesessor = {}


def RipOne(grid, wire, sink): # rip all connections of a wire or just one sink?
    pass


def routeAllWires(grid, pins): #route all wire
    pass

def routeOneWire(grid, wire): # route all pins of a wire
    pass


def pathfinding(wire):
    (src_x, src_y) = c.WIRE2SOURCE[wire] 
    sinks = c.WIRE2SINK[wire] # eg[(6, 5), (6, 8)]

    count = 0
    open_set = PriorityQueue( )# contains all the locations we need to search for path (dist, count, index)
    open_set.put((0, count, (src_x, src_y))) #(f_score, count, node)count when we inset the item 
    predesessor = {}
    # g = f + h
    g_score = {}   # initialize to inf
    #initial open set by putting source in it
    
    while open_set:
        curr_block = open_set.get()[2]
