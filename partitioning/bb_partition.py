import random
netlist = []
num_nets = 0
num_nodes = 0

def parse_file(filepath = "ass3_files/cm82a.txt"):
    global netlist, num_node, num_nets
    # init netlist
    netlist = []
    with open(filepath, 'r') as f:
        for line_num, l in enumerate(f):
            line = l.strip().split()
            if not line: # be careful about empty lines
                break
            # print("{} {}".format(line_num, line))
            if line_num == 0: # first line: num_nodes, num_connections, num_rows, num_cols
                num_nodes = int(line[0])
                num_nets = int(line[1])
            
            else: # the rest of lines (contains netlist)
                

                net_num = line_num - 1 # net number starting from 0
                net_id = net_num
                    
                for item in line[1:]:
                    node_id = int(item)
                    node = self.node_list[node_id]
                    # print(node.__str__())
                    node.nets.append(net)
                    net.nodes.append(node)

                self.netlist.append(net)

