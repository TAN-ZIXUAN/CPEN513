import math
import random
import statistics as stats
from tkinter import *
from tkinter import filedialog, ttk
from collections import deque 

from ttkthemes import ThemedStyle

from circuit import Circuit
import matplotlib.pyplot as plt  

def init_canvas():
    canvas.delete(ALL)

    # size of site
    rdim = 20
    if circuit.num_rows < 10:
        if circuit.num_cols < 10:
            rdim = 50
        elif circuit.num_cols < 30:
            rdim = 30
        else:
            rdim = 15
    elif circuit.num_rows <30:
        if circuit.num_cols < 10:
            rdim = 50
        elif circuit.num_cols < 30:
            rdim = 30
        else:
            rdim = 10
    else:
        rdim = 10
    rh = rw = rdim
    xoffset = rdim // 5
    yoffset = rdim // 5

    # size of canvas
    cw = circuit.num_cols * rw + 2 * xoffset
    ch = (2 * circuit.num_rows - 1) * rh  + 2 * yoffset
    canvas.config(width=cw, height=ch)

    # rectangles
    for row in circuit.grid:
        for site in row:
            x1 = site.col * rw + xoffset
            x2 = x1 + rw
            y1 = site.row * rh * 2 + yoffset
            y2 = y1 + rh
            site.rect = canvas.create_rectangle(x1, y1, x2, y2, fill='white') # white #FFFFFF
                    
def canvas_clear_nets():
    canvas.delete('nets')

def canvas_draw_nets():
    # cnt = 0
    for net in circuit.netlist:
        # print("draw net ",cnt)
        # cnt += 1
        src = net.cells[0]
        x1, y1 = src.corresponding_site.get_rect_center(canvas)
        for sink in net.cells[1:]:
            # print(sink.corresponding_site.get_rect_center(canvas))
            x2, y2 = sink.corresponding_site.get_rect_center(canvas)
            canvas.create_line(x1, y1, x2, y2, fill=net.color, tags='nets')

def update_canvas():
    canvas_clear_nets()
    circuit.update_rects(canvas)
    canvas_draw_nets()
    total_cost_text.set(circuit.total_cost)


def load_file_button():
    xs = []
    ys = []
    """load benchmark files"""
    file = filedialog.askopenfilename(initialdir="ass2_files/",filetypes=(("Text File", "*.txt"),("All Files","*.*")), title="choose a file")
    print("load file:", file)
    if not file:
        return

    # logging.info("loading file:{file}".format(file=file))
    circuit.parse_circuit_file(file)

    place_btn.state(['!disabled'])
    init_canvas()

def random_placement():
    random_sites_id_list = random.sample(range(circuit.num_sites), circuit.num_cells) # generate random (cell_id, site_id) list of size equals to num_sites
    for cell_id, random_site_id in enumerate(random_sites_id_list):
        site = circuit.get_site_by_id(random_site_id)
        cell = circuit.cell_list[cell_id]
        site.element = cell
        cell.corresponding_site = site
        # print(cell.__str__())

def get_init_temp(k=20, num_moves=10):
    costs = [0 for _ in range(num_moves)]
    for i in range(num_moves):
        site1, site2 = select_sites()
        cost_before_swap = 0
        # cost_before_swap = circuit.calc_total_cost()
        if not site1.is_empty():
            cell1 = site1.element
            cost_before_swap += cell1.calc_nets_cost_with_cell()
        if not site2.is_empty():
            cell2 = site2.element
            cost_before_swap += cell2.calc_nets_cost_with_cell()

        swap_sites(site1, site2)

        cost_after_swap = 0
        # cost_after_swap = circuit.calc_total_cost()
        if not site1.is_empty():
            cell1 = site1.element
            cost_after_swap += cell1.calc_nets_cost_with_cell()
            # print("post cost", cost_after_swap)
            
        if not site2.is_empty():
            cell2 = site2.element
            cost_after_swap += cell2.calc_nets_cost_with_cell()

        delta_c = cost_after_swap - cost_before_swap
        circuit.total_cost += delta_c
        costs[i] = circuit.total_cost

    stdev = stats.stdev(costs)
    # print('std_dev of {} random moves is'.format(num_moves), stdev)
    init_temp = k * stdev
    return init_temp



# def initial_temp(k=20, num_moves=50):
#     """Return a good value to use for the initial temperature.

#     Based on standard deviation of a number of random moves."""

#     costs = [0 for _ in range(num_moves)]  # a list of cost of those n random moves
#     for i in range(num_moves):
#         random_placement()
#         costs[i] = circuit.calc_total_cost()
    
#     # print('costs of {} random moves:'.format(num_moves), costs)
#     stdev = stats.stdev(costs)
#     # print('std_dev of {} random moves is'.format(num_moves), stdev)
#     init_temp = k * stdev
#     return init_temp

def select_sites():
    """Return a list of 2 randomly selected sites, only one may be empty."""
    while True:
        (site_id1, site_id2) = random.sample(range(circuit.num_sites), 2)
        site1 = circuit.get_site_by_id(site_id1)
        site2 = circuit.get_site_by_id(site_id2)
    
        # try again if both sites are empty
        if site1.is_empty() and site2.is_empty():
            continue
        else:
            break
        
    return (site1, site2)


def swap_sites(site1, site2):
    """Swap element of two sites."""
    site1.element, site2.element = site2.element, site1.element
    
    if site1.element != None:
        site1.element.corresponding_site = site1
    if site2.element != None:
        site2.element.corresponding_site = site2


def init_place():
    xs = []
    ys = []
    random_placement()
    circuit.total_cost = circuit.calc_total_cost()
    # init_cost_text =  circuit.total_cost
    # print("init cost", circuit.total_cost)
    # print("152", circuit.calc_total_cost())
    update_canvas()
    total_cost = circuit.total_cost
    
    total_cost_text.set(total_cost)
    # init_cost_text.set(total_cost)
    update_canvas()
    # logging.info('initial total cost = {total_cost}'.format(total_cost=total_cost))
    print("initial cost", total_cost)
    # enable the Anneal button
    anneal_btn.state(['!disabled'])

    # disable the Place button
    place_btn.state(['disabled'])


def record_n_recent_costs(n, costs, cost):
    """only keep track of n recent cost and return stdev of the n costs
    n: number of recent costs
    costs_q: deque that stores cost.
    cost: the cost you want to add
    """

    while len(costs) >= n - 1:
            costs.pop(0)
    costs.append(cost)


def placing():
    xs = []
    ys = []
    T0 = get_init_temp()
    num_iterations = circuit.num_cells
    # num_iterations = int(10 * math.sqrt(circuit.num_cells))
    cooling_rate = 0.95
    threshold = 0.01
    stdev_threshold = 0.01
    if T0 <= 100:
        threshold = 0.001
        cooling_rate = 0.95
        stdev_threshold = 0.01
    elif T0 <=500:
        threshold = 0.001
        cooling_rate = 0.95
        stdev_threshold = 0.01
    elif T0 <= 1000:
        threshold = 0.001
        cooling_rate = 0.95
        stdev_threshold = 0.01
    else:
        threshold = 0.001
        cooling_rate = 0.95
        stdev_threshold = 0.01
    print("T0:{}, num_iterations:{}, cooling rate:{}, threshold:{}".format(T0, num_iterations, cooling_rate, threshold))
    costs = []
    
    annealing(T0, cooling_rate, threshold,num_iterations, costs, stdev_threshold)



def annealing(initial_temp, cooling_rate, threshold, num_iterations, costs, stdev_threshold):
    T = initial_temp
    # # costs_q = deque()
    # costs_q = deque([circuit.total_cost])
    
    anneal_loop(T, num_iterations, costs)
    T *= cooling_rate
    update_canvas()
    print("T: {}, cost: {}".format(T, circuit.total_cost))
    ys.append(circuit.total_cost)
    xs.append(T)

    if T <= threshold or stats.stdev(costs) <= stdev_threshold: # exits
        cost = circuit.calc_total_cost()
        total_cost_text.set(cost)
        print("T:", T)
        print('final cost = {}'.format(cost))
        plot_line_chart()
        anneal_btn.state(['disabled'])
    else: # continue annealing
        root.after(10, annealing, T, cooling_rate, threshold, num_iterations, costs, stdev_threshold)


def anneal_loop(T, num_iterations,costs):
    # print("T", T)
    for _ in range(num_iterations): # TODO: cost didn't change after swap site
        site1, site2 = select_sites()
        cost_before_swap = 0
        cost_after_swap = 0
        # cost_before_swap = circuit.calc_total_cost()
        if not site1.is_empty():
            cell1 = site1.element
            cost_before_swap += cell1.calc_nets_cost_with_cell()
        if not site2.is_empty():
            cell2 = site2.element
            cost_before_swap += cell2.calc_nets_cost_with_cell()

        swap_sites(site1, site2)

        cost_after_swap = 0
        # cost_after_swap = circuit.calc_total_cost()
        if not site1.is_empty():
            cell1 = site1.element
            cost_after_swap += cell1.calc_nets_cost_with_cell()
            # print("post cost", cost_after_swap)
            
        if not site2.is_empty():
            cell2 = site2.element
            cost_after_swap += cell2.calc_nets_cost_with_cell()

        delta_c = cost_after_swap - cost_before_swap 

        r = random.random()
        try:
            tmp = math.exp( -delta_c / T)
        except OverflowError:
            # print("overflow err")
            quit_tk()
        if r < tmp:
            circuit.total_cost += delta_c
            record_n_recent_costs(num_iterations*2, costs, circuit.total_cost)
        else:
            # undo moves
            # print("undo")
            swap_sites(site2, site1)

def plot_line_chart():
    print("plotting")
    plt.plot(xs, ys)
    plt.xlim(max(xs), min(xs))
    plt.ylim(min(ys), max(ys))
    plt.xlabel("temperature")
    plt.ylabel("cost")
    # min_idx = ys.index(min(ys))
    # max_idx = ys.index(max(ys))
    plt.annotate("{}".format(ys[0]), (xs[0], ys[0]))
    # plt.annotate("{}".format(min(ys)), (xs[min_idx], ys[min_idx]))
    plt.annotate("{}".format(ys[-1]), (xs[-1], ys[-1]))
    
    plt.show()
    print("plotted")

def quit_tk():
    root.destroy()
    print("quite mainloop")
    plot_line_chart()

if __name__=='__main__':

    random.seed(0)
    circuit = Circuit()

    root = Tk()
    root.title("Placement")
    style = ThemedStyle(root)
    style.set_theme("yaru")

    top_frame = ttk.Frame(root, padding="3 3 12 12")
    top_frame.grid(column=0, row=0)
    top_frame.columnconfigure(0, weight=1)
    top_frame.rowconfigure(0, weight=1)
    canvas_frame = ttk.Frame(top_frame)
    canvas_frame.grid(column=0, row=0, sticky=(N,E,S,W))
    btn_frame = ttk.Frame(top_frame)
    btn_frame.grid(column=0, row=1)
    stats_frame = ttk.Frame(top_frame)
    stats_frame.grid(column=0, row=2)

    # setup canvas frame (contains benchmark label and canvas)
    filename = StringVar()
    benchmark_lbl = ttk.Label(canvas_frame, textvariable=filename)
    benchmark_lbl.grid(column=0, row=0)

    canvas = Canvas(canvas_frame, width=640, height=480, bg="grey")
    canvas.grid(column=0, row=1, padx=5, pady=5)

    # setup button frame (contains buttons)
    open_btn = ttk.Button(btn_frame, text="load file", command=load_file_button)
    open_btn.grid(column=0, row=0, padx=5, pady=5)
    place_btn = ttk.Button(btn_frame, text="init place", command=init_place)
    place_btn.grid(column=1, row=0, padx=5, pady=5)
    place_btn.state(['disabled'])
    anneal_btn = ttk.Button(btn_frame, text="placing", command=placing)
    anneal_btn.grid(column=2, row=0, padx=5, pady=5)
    anneal_btn.state(['disabled'])

    quit_btn = ttk.Button(btn_frame, text="quit & plot", command=quit_tk)
    quit_btn.grid(column=3, row=0, padx=5, pady=5)
    quit_btn.state(['!disabled'])

    total_cost_text = StringVar()
    total_cost_text.set('N/A')
    ttk.Label(stats_frame, text="cost:").grid(column=0, row=1)
    cost_lbl = ttk.Label(stats_frame, textvariable=total_cost_text)
    cost_lbl.grid(column=1, row=1)

    # line chart
    fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    root.mainloop()
    # root.after(0, plot_line_chart)
    
    





