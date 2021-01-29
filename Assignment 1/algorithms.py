import collections
from queue import PriorityQueue

from functions import *

'''
a* algorithm on a 2d grid. return True/False
f_n = g_n + h_n
g_n: shortest path from source node to curr_node
h_n: heuristic. estimate dist from curr_node to source node. manhattan dist used here
'''
def a_star(draw, grid, source, sink): 
    count = 0 # keep track when we insert the node
    #for priorityque, element is removed in a sorted order. here by scores
    open_q = PriorityQueue() # store the nodes we are going to explore
    open_q.put((0, count, source))
    curr2pre = {} # store the predecessor node for backtracing key: curr node, value: pre node

    g_n = {node: float("inf") for row in grid for node in row}
    g_n[source] = 0

    f_n = {node:float("inf") for row in grid for node in row}
    f_n[source] = h(source, sink)

    open_set = {source} # keep track of nodes in the priority queue. 
    closed_set = set() # store visited node

    while not open_q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_node = open_q.get()[2]
        print("curr_node", curr_node)
        open_set.remove(curr_node)
        closed_set.add(curr_node)

        if curr_node == sink:
            print("path mADE")
            backtracing(curr2pre, source, draw)
            sink.mark_routed()
            source.mark_routed()
            return True
        
        for nei in c.GRID[curr_node[0]][curr_node[1]].neighbours:
            print("nei", nei)
            if nei in closed_set:
                continue #slip if we have visited this 
            tmp_g_n = g_n[curr_node] + 1

            if tmp_g_n < g_n[nei]: 
                curr2pre[nei] = curr_node
                g_n[nei] = tmp_g_n
                f_n[nei] = g_n[nei] + h(nei, sink)
                if nei not in open_set: # put the neighbour with better score to the set
                    count += 1
                    open_q.put((f_n[nei], count, nei))
                    open_set.add(nei)
                    nei.mark_path()
        
        draw()

        # if curr_node != source:
        #     closed_set.add(curr_node)
        

    return False



    

