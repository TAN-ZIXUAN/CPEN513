import collections

import functions as f

'''
a* algorithm on a 2d grid. return True/False
f_n = g_n + h_n
g_n: shortest path from source node to curr_node
h_n: heuristic. estimate dist from curr_node to source node. manhattan dist used here
'''
def a_star(draw, grid, source, sink): 
    count = 0
    #for priorityque, element is removed in a sorted order. here by scores
    open_set = collections.PriorityQueue() # store the nodes we are going to explore
    open_set.put((0, count, source))
    curr2pre = {} # store the predecessor node for backtracing key: curr node, value: pre node

    g_n = {node: float("inf") for row in grid for node in row}
    g_n[source] = 0

    f_n = {node:float("inf") for row in grid for node in row}
    f_n[source] = f.h(source, sink)

    open_hash_set = {source}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_node = open_set.get()[2]
        open_hash_set.remove(curr_node)

        if curr_node == sink:
            f.backtracing(pre, source, draw)
            sink.mark_routed()
            source.mark_routed()
            return True
        
        for nei in curr_node.neighbors:
            tmp_g_n = g_n[curr_node] + 1

            if tmp_g_n < g_score[nei]:
                curr2pre[nei] = curr_node
                g_n[nei] = tmp_g_n
                f_n[nei] = g_n[nei] + h(nei, sink)
                if nei not in open_set_hash:
                    count += 1
                    open_set.put((f_n[nei], count, nei))
                    open_set_hash.add(nei)
                    nei.
        
        


    

