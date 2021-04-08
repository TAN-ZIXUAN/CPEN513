import numpy as np
import random
import pytest
from chip import Chip
random.seed(0)
chip = Chip()
chip.parse_chip_file("ass3_files/cm82a.txt")
def random_partition():
    """ set random partition
    randomly assign nodes to block 0 and 1
    """
    for node_id in range(chip.num_nodes):
        node = chip.node_list[node_id]
        node.block_id = node_id % 2# assign them block 0 or 1

def init_gains():
    """calc gain value of each node for the current partition
    gain = # incident edges that cross partition - # incident edges that do not  
    for directed graph, set from and to. 
    node in block 0 (from: block 0, to: block 1)
    node in block 1 (from: block 1, to: block 0)
    so gain = sum(To) - sum(From)
    """
    chip.init_net_partitions()
    for node in chip.graph:
        node.unlock_node()
        node.gain = 0
        from_block = node.block_id
        to_block = (node.block_id + 1) % 2
        for nei in chip.graph[node]:
            if nei.block_id == to_block:
                node.gain += 1
            elif nei.block_id == from_block:
                node.gain -= 1

        chip.blocks[node.block_id].add_node(node)
random_partition()
init_gains()
print(chip.graph_id) # {3: {8, 5}, 5: {9, 10, 3, 7}, 8: {0, 3, 9, 10, 11}, 9: {8, 5}, 10: {8, 5}, 6: {0, 11}, 0: {8, 2, 4, 6}, 11: {8, 1, 4, 6}, 4: {0, 11}, 7: {5}, 2: {0}, 1: {11}})
print(chip)   # block0:[7, 8, 10, 2, 6], block1:[9, 1, 0, 11, 3, 4, 5]
"""
graph:
 {3: {8, 5}, 5: {9, 10, 3, 7}, 8: {0, 3, 9, 10, 11}, 9: {8, 5}, 
 10: {8, 5}, 6: {0, 11}, 0: {8, 2, 4, 6}, 11: {8, 1, 4, 6}, 4: {0, 11}, 7: {5}, 2: {0}, 1: {11}})
partiions:
(node, gain)
block0:[(8, 1), (10, 0), (0, -4), (2, -1), (4, 0), (6, 0)]
block1:[(9, 0), (1, -1), (11, 2), (3, 0), (5, -2), (7, -1)]
"""
expected_result = 0
# all nodes with even id in block0 and all nodes with odd id in block1
for node_id in chip.graph_id:
    for nei_id in chip.graph_id[node_id]:
        if nei_id % 2 != node_id % 2:
            expected_result += 1

print("expected", expected_result)
def test_calc_edge_cutsize():
    assert chip.calc_cutsize() == expected_result
