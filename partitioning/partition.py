from chip import Chip
import random
def random_partition():
    """ set random partition
    randomly assign nodes to block 0 and 1
    """
    # random_nodelist = random.sample(range(chip.num_nodes), chip.num_nodes)
    # for i, node_id in enumerate(random_nodelist):
    for node_id in range(chip.num_nodes):
        node = chip.node_list[node_id]
        node.block_id = random.choice([0, 1])# randomly assign them block 0 or 1
    chip.init_net_partitions()
def init_gains():
    """calc gain value of each node for the current partition
    gain = # incident edges that cross partition - # incident edges that do not  
    for directed graph, set from and to. 
    node in block 0 (from: block 0, to: block 1)
    node in block 1 (from: block 1, to: block 0)
    so gain = sum(To) - sum(From)
    """
    
    for node in chip.node_list:
        node.unlock_node()  # the initial status of node is unlocked
        node.gain = 0
        from_block = node.block_id
        to_block = (node.block_id + 1) % 2
        
        for net in node.nets:
            # gain = sum(subgain)
            # subgain = part1 - part2
            part1 = 0 # incident edges that cross partition 
            part2 = 0 # incident edges that do not
            part1 = net.partitions[to_block]  # equals to number of node in another block
            part2 = net.partitions[from_block] - 1 # edges = equals to number of node in the same block - 1 
            subgain = part1 - part2
            node.gain += subgain
            # if net.partitions[from_block] == 1:
            #     node.gain += 1
            # if net.partitions[to_block] == 0:
            #     node.gain -= 1
        chip.blocks[from_block].add_node(node)

def save_partition():
    block0 = list(chip.blocks[0].save_copy())
    block1 = list(chip.blocks[1].save_copy())
    return [block0, block1]
def select_node():
    """retrurn the selected node
    select the nodes with highest gain whose move would not cause an imbalance
    """
    # block_id = None
    if chip.blocks[0].get_size() == chip.blocks[1].get_size():
        if chip.blocks[0].get_max_gain() > chip.blocks[1].get_max_gain():
            block_id = 0
        elif chip.blocks[0].get_max_gain() < chip.blocks[1].get_max_gain():
            block_id = 1
        else: # randomly select a block
            block_id = random.choice([0, 1])
    
    elif chip.blocks[0].get_size() > chip.blocks[1].get_size():
        block_id = 0
    else:
        block_id = 1
    node = chip.blocks[block_id].pop_max_gain_node()
    return node

def move_node(node):
    from_block = node.block_id
    to_block = (node.block_id + 1) % 2
    node.lock_node()
    node.block_id = to_block
    chip.blocks[node.block_id].add_node(node)
    for net in node.nets:
        net.partitions[from_block] -= 1
        net.partitions[to_block] += 1
        # if net.partitions[node.block_id] == 0:



def partition(num_passes):
    random_partition()
    init_gains()
    chip.cutsize = chip.calc_cutsize()
    chip.best_partition = save_partition()
    chip.min_cutsize = chip.cutsize
    prev_min_cutsize = chip.cutsize
    
    for i in range(num_passes):
        
        chip.unlock_all_nodes()
        print("passes:", i)
        while chip.has_unlocked_nodes:
            # print("passes:", i)
            print(chip)
            # print()
            
            chip.calc_all_gains()
            node = select_node()
            move_node(node)
            # print("move node {} to {}".format(node.node_id, node.block_id))
            chip.calc_cutsize()
            if chip.cutsize < chip.min_cutsize:
                chip.min_cutsize = chip.cutsize
                chip.best_partition = chip.save_partition()
            

        prev_min_cutsize = chip.min_cutsize
        chip.blocks = chip.best_partition
        print("best partition")
        print(chip)
        print("#{i}: cutsize {cutsize}".format(i = i, cutsize = prev_min_cutsize))






if __name__ == "__main__":
    random.seed(0)
    chip = Chip()
    chip.parse_chip_file()
    partition(5)