from chip import Chip
import random
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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

def save_partition():
    block0 = list(chip.blocks[0].save_copy())
    block1 = list(chip.blocks[1].save_copy())
    return [block0, block1]
def select_node():
    """retrurn the selected node
    select the nodes with highest gain whose move would not cause an imbalance
    """
    # block_id = None
    if not (chip.blocks[0].has_unlocked_nodes()):
        block_id = 1
    elif not (chip.blocks[1].has_unlocked_nodes()):
        block_id = 0

    elif chip.blocks[0].get_size() == chip.blocks[1].get_size():
        
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
    # update block_id and chip.blocks

    from_block = node.block_id
    to_block = (node.block_id + 1) % 2
    node.lock_node()
    node.block_id = to_block
    chip.blocks[node.block_id].add_node(node)
    for net in node.nets:
        net.partitions[from_block] -= 1
        net.partitions[to_block] += 1

    # update edges'cut value
    for edge in chip.edges:
        if node in edge:
            chip.edges[edge] = not chip.edges[edge] # flip value iscut => !iscut
    # update gains of all connected node
    for nei in chip.graph[node]:
        if nei.block_id == from_block:
            nei.gain += 1
        elif nei.block_id == to_block:
            nei.gain -= 1
            
def rollback_to_saved_partition(partition_copy, edges_copy):
    """
    Arguments: partition_copy = [block0, block1]
        block0 = list(self.blocks[0].save_copy())
        block1 = list(self.blocks[1].save_copy())
    """
    # clear partition 
    chip.blocks[0].clear_block()
    chip.blocks[1].clear_block()
    # blocks
    for block_id, block_nodes in enumerate(partition_copy):
        for node in block_nodes:
            node.block_id = block_id
            # node.gain = node.gain
    # edges
    chip.edges = edges_copy
    init_gains()
    chip.cutsize = chip.min_cutsize
    chip.net_cutsize = chip.calc_net_cutsize()
    # print("110 net", chip.net_cutsize)
    net_cutsize_text.set(chip.net_cutsize)
    

def partition(num_passes = 4):
    print(chip.graph_id)
    # random_partition()
    chip.blocks[0].clear_block()
    chip.blocks[1].clear_block()
    init_gains()
    chip.cutsize = chip.calc_cutsize()
    chip.best_partition_copy = save_partition()
    chip.edges_copy = chip.edges.copy()
    chip.min_cutsize = chip.cutsize
    gui.draw_canvas()
    root.after(100)
    # prev_min_cutsize = chip.cutsize
    
    for i in range(num_passes):
        
        chip.unlock_all_nodes()
        print("passes:", i)
        
        while chip.has_unlocked_nodes():
            print(chip)       
            # chip.calc_all_gains()
            node = select_node()
            move_node(node)
            # print("move node {} to {}".format(node.node_id, node.block_id))
            chip.cutsize = chip.calc_cutsize()
            chip.net_cutsize = chip.calc_net_cutsize()
            # chip.cutsize -= node.gain
            # node.gain = -node.gain
            if chip.cutsize >= 0 and chip.cutsize < chip.min_cutsize:
                    chip.min_cutsize = chip.cutsize
                    chip.best_partition_copy = chip.save_partition()
                    chip.edges_copy = chip.edges.copy()
        rollback_to_saved_partition(chip.best_partition_copy, chip.edges_copy)
    gui.draw_canvas()
    print("best partition")
    load_btn.state(['disabled'])
    partition_btn.state(['disabled'])
    print(chip)

class GUI:
    def init_canvas(self):
        canvas.delete(ALL)
        edge_cutsize_text.set('-')
        net_cutsize_text.set('-')
        self.rdim = 25 # rectangle dimensions
        self.node_pad = 5 # padding between node rectangles
        self.x_pad = 50 # padding in x coordinate between partitions
        self.y_pad = 10 # padding from top and bottom of canvas
        max_cells_per_block = (chip.num_nodes // 2) + 2
        if max_cells_per_block > 25:
            self.num_rows = math.ceil(math.sqrt(max_cells_per_block))
            self.num_cols = math.ceil(max_cells_per_block / self.num_rows)
        else:
            self.num_rows = max_cells_per_block
            self.num_cols = 1
        self.cw = 2 * (2*self.x_pad + self.num_cols*self.rdim + (self.num_cols - 1)*self.node_pad)
        # print("185 cw", cw)
        self.ch = 2*self.y_pad + self.num_rows*self.rdim + (self.num_rows - 1)*self.node_pad
        canvas.config(width=self.cw, height=self.ch)

    def draw_nodes(self):
        """Redraw nodes in each block."""
        rh = rw = self.rdim
        x = [self.x_pad, self.cw//2 + self.x_pad]
        y = [self.y_pad, self.y_pad]
        node_count = [0, 0]
        # Draw rectanges for each node
        for node in chip.node_list:
            # calculate coords of node rectangle
            x1 = x[node.block_id]
            x2 = x1 + rw
            y1 = y[node.block_id]
            y2 = y1 + rh

            # create node rectangle
            if node.is_unlocked():
                fill = 'white'
            else:
                fill = 'red'
            node.rect= canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
            node_count[node.block_id] += 1

            # update x, y value for next rectangle
            # - if on last node in row, move to top of next column
            # print("218 num row", num_rows)
            if (node_count[node.block_id] % self.num_rows) == 0:
                x[node.block_id] = x2 + self.node_pad
                y[node.block_id] = self.y_pad
            else:
                x[node.block_id] = x1
                y[node.block_id] = y2 + self.node_pad

    def draw_nets(self):
        for net in chip.netlist:
            source = net.nodes[0]
            x1, y1 = source.get_rect_center(canvas)
            for sink in net.nodes[1:]:
                x2, y2 = sink.get_rect_center(canvas)
                canvas.create_line(x1, y1, x2, y2, fill=net.color)
    def draw_canvas(self):

        canvas.delete(ALL)

        # init_canvas()
        self.draw_nodes()
        self.draw_nets()
        edge_cutsize_text.set(chip.cutsize)
        net_cutsize_text.set(chip.net_cutsize)


def load_file_button():
    # chip.__init__()
    
    """load benchmark files"""
    # chip = Chip()
    file = filedialog.askopenfilename(initialdir="ass3_files/",filetypes=(("Text File", "*.txt"),("All Files","*.*")), title="choose a file")
    print("load file:", file)
    if not file:
        return

    # logging.info("loading file:{file}".format(file=file))
    chip.parse_chip_file(file)

    partition_btn.state(['!disabled'])
    # load_btn.state(['disabled'])
    gui.init_canvas()




if __name__ == "__main__":
    random.seed(0)
    chip = Chip()
    # chip.parse_chip_file("ass3_files/cm82a.txt")
    # print(chip.graph_id)

    
    root = Tk()
    root.title("Partition")
    
    

    # add frames to gui
    top_frame = ttk.Frame(root, padding="3 3 12 12")
    top_frame.grid(column=0, row=0)
    top_frame.columnconfigure(0, weight=1)
    top_frame.rowconfigure(0, weight=1)
    canvas_frame = ttk.Frame(top_frame)
    canvas_frame.grid(column=0, row=0, sticky=(N,E,S,W))
    stats_frame = ttk.Frame(top_frame)
    stats_frame.grid(column=0, row=1)
    btn_frame = ttk.Frame(top_frame)
    btn_frame.grid(column=0, row=2)

    # setup canvas frame (contains benchmark label and canvas)
    filename = StringVar()
    benchmark_lbl = ttk.Label(canvas_frame, textvariable=filename)
    benchmark_lbl.grid(column=0, row=0)
    canvas = Canvas(canvas_frame, width=320, height=240, bg="dark grey")
    canvas.grid(column=0, row=1, padx=5, pady=5)

    gui = GUI()
    # setup button frame (contains buttons)
    load_btn = ttk.Button(btn_frame, text="load file", command=load_file_button)
    load_btn.grid(column=0, row=0, padx=5, pady=5)
    partition_btn = ttk.Button(btn_frame, text="partition", command=partition)
    partition_btn.grid(column=1, row=0, padx=5, pady=5)
    partition_btn.state(['disabled'])

    edge_cutsize_text = StringVar()
    edge_cutsize_text.set('-')
    ttk.Label(stats_frame, text="edge cutsize:").grid(column=1, row=1, sticky=E)
    cutsize_lbl = ttk.Label(stats_frame, textvariable=edge_cutsize_text)
    cutsize_lbl.grid(column=2, row=1, sticky=W)

    net_cutsize_text = StringVar()
    net_cutsize_text.set('-')
    ttk.Label(stats_frame, text="net cutsize:").grid(column=1, row=2, sticky=E)
    net_cutsize_lbl = ttk.Label(stats_frame, textvariable=net_cutsize_text)
    net_cutsize_lbl.grid(column=2, row=2, sticky=W)
    root.mainloop()
