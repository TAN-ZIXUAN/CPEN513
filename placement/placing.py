import logging
import math
import random
import statistics as stats
from tkinter import *
from tkinter import filedialog, ttk

from ttkthemes import ThemedStyle

# from cell import Cell
# # from site import Site
# from net import Net
from circuit import Circuit


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
    cnt = 0
    for net in circuit.netlist:
        print("draw net ",cnt)
        cnt += 1
        src = net.cells[0]
        x1, y1 = src.corresponding_site.get_rect_center(canvas)
        for sink in net.cells[1:]:
            # print(sink.corresponding_site.get_rect_center(canvas))
            x2, y2 = sink.corresponding_site.get_rect_center(canvas)
            canvas.create_line(x1, y1, x2, y2, fill=net.color, tags='nets')


# def update_rects():
#     """Redraw sites in canvas."""
#     # Update rectanges of sites
#     for row in circuit.grid:
#         for site in row:
#             site.update_rect()

def update_canvas():
    canvas_clear_nets()
    circuit.update_rects(canvas)
    canvas_draw_nets()
    total_cost_text.set(circuit.total_cost)


def load_file_button():
    """load benchmark files"""
    file = filedialog.askopenfilename(initialdir="ass2_files/",filetypes=(("Text File", "*.txt"),("All Files","*.*")), title="choose a file")
    if not file:
        return

    logging.info("loading file:{file}".format(file=file))
    circuit.parse_circuit_file(file)

    place_btn.state(['!disabled'])
    init_canvas()

def random_placement():
    random_sites_id_list = random.sample(range(circuit.num_sites), circuit.num_cells) # generate random (cell_id, site_id) list of size equals to num_sites
    for cell_id, random_site_id in enumerate(random_sites_id_list):
        site = circuit.get_site_by_id(random_site_id)
        cell = circuit.cell_list[cell_id]
        site.element = cell
        cell.row = site.row
        cell.col = site.col
        cell.corresponding_site = site
        # print(cell.__str__())
def init_place():
    random_placement()
    circuit.total_cost = circuit.calc_total_cost()
    update_canvas()
    total_cost = circuit.total_cost
    
    total_cost_text.set(total_cost)
    logging.info('initial total cost = {total_cost}'.format(total_cost=total_cost))
    print("initial cost", total_cost)
    # enable the Anneal button
    anneal_btn.state(['!disabled'])

    # disable the Place button
    place_btn.state(['disabled'])

def initial_temp(k=20, num_moves=50):
    """Return a good value to use for the initial temperature.

    Based on standard deviation of a number of random moves."""

    costs = [0 for _ in range(num_moves)]  # a list of cost of those n random moves
    for i in range(num_moves):
        random_placement()
        costs[i] = circuit.calc_total_cost()
    
    # print('costs of {} random moves:'.format(num_moves), costs)
    stdev = stats.stdev(costs)
    # print('std_dev of {} random moves is'.format(num_moves), stdev)
    init_temp = k * stdev
    return init_temp

def get_new_temp(temp, accepted_costs):
    """Return the next annealing temperature.
    
    Based on standard deviation of accepted moves at previous temperature."""

    print('get_new_temp()')
    stdev = stats.stdev(accepted_costs)
    print('std_dev(accepted_costs) =', stdev)
    new_temp = temp * math.exp(-0.7 * temp / stdev)

    # avoid overflow errors due to very low temperatures
    if new_temp < 0.1:
        new_temp = 0.1

    print('new T =', new_temp)
    return new_temp


def exit_condition(temp, accepted_costs):
    """Check annealing exit condition
    
    Based on standard deviation of the costs of accepted moves."""
    
    # print("exit_condition()")
    # stdev = stats.stdev(accepted_costs)
    # print('std_dev(accepted costs) =', stdev)
    # if stdev < 2:
    #     return True
    # else:
    #     return False
    return temp < accepted_costs



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

def anneal():
    # temp = initial_temp()
    temp = initial_temp()
    k = 10 # constant for num iterations at each temp
    niterations = int(k * (circuit.num_cells)**(4/3))

    # print annealing schedule parameters
    print('T0 =', temp)
    print('niterations =', niterations)

    anneal_outer(temp, niterations)

def anneal_inner(temp, niterations, accepted_costs):
    """Inner loop of simulated annealing algorithm."""

    naccepted_moves = 0
    ntotal_moves = 0
    for _ in range(niterations):
        # randomly select two sites
        [site1, site2] = select_sites()

        # calculate cost of move - only need to consider nets that
        # contain the nodes we swapped
        pre_swap_cost = 0
        if not site1.is_empty():
            cell1 = site1.element
            pre_swap_cost += cell1.calc_nets_cost_with_cell()
        if not site2.is_empty():
            cell2 = site2.element
            pre_swap_cost += cell2.calc_nets_cost_with_cell()

        swap_sites(site1, site2)

        post_swap_cost = 0
        if not site1.is_empty():
            cell1 = site1.element
            post_swap_cost += cell1.calc_nets_cost_with_cell()
        if not site2.is_empty():
            cell2 = site2.element
            post_swap_cost += cell2.calc_nets_cost_with_cell()

        delta_c = post_swap_cost - pre_swap_cost 

        # r = random(0, 1)
        r = random.random()

        if r < math.exp(-delta_c / temp):
            # take move (keep swap)
            circuit.total_cost += delta_c
            accepted_costs.append(circuit.total_cost)
            naccepted_moves += 1
        else:
            # don't take move (undo swap)
            swap_sites(site2, site1)
        ntotal_moves += 1

    accept_rate = 100 * naccepted_moves / ntotal_moves
    print("accept_rate =", accept_rate)

def anneal_outer(temp, niterations):
    """Outer loop of annealing function.
    
    Run inner loop, reduce temperature, check exit condition.  """

    print("anneal_outer()")
    accepted_costs = []
    # run anneal inner loop
    anneal_inner(temp, niterations, accepted_costs)

    # reduce temp
    # temp = get_new_temp(temp, accepted_costs)
    temp *= 0.95

    # redraw canvas
    update_canvas()

    print("cost =", circuit.total_cost)

    # check exit condition
    if not exit_condition(temp, accepted_costs):
        # exit condition not met, run outer loop again
        root.after(1000, anneal_outer, temp, niterations)
    else:
        # exit condition met, do final steps
        
        total_cost = circuit.calc_total_cost()
        
        total_cost_text.set(total_cost)
        logging.info('final cost = {}'.format(total_cost))
        print('final cost = {}'.format(total_cost))

def placing():
    init_temp = initial_temp()
    print('T0 =', init_temp)
    num_iterations = 10
    cooling_rate = 0.95
    threshold = 50
    circuit.grid = annealing(init_temp, num_iterations, cooling_rate, threshold)
    update_canvas()
    cost = circuit.calc_total_cost()
    total_cost_text.set(cost)
    # best_cost = min(best_cost, total_cost)
    print('final cost = {}'.format(cost))
    


def annealing(initial_temp, num_iterations, cooling_rate, threshold):
    # temp = initial_temp
    T = initial_temp
    # initial placement
    # random_placement()
    print("cost", circuit.calc_total_cost())
    grid = circuit.grid

    while(T > threshold):
        for _ in range(num_iterations): # TODO: cost didn't change after swap site
            site1, site2 = select_sites()
            pre_swap_cost = 0
            if not site1.is_empty():
                cell1 = site1.element
                pre_swap_cost += cell1.calc_nets_cost_with_cell()
            if not site2.is_empty():
                cell2 = site2.element
                pre_swap_cost += cell2.calc_nets_cost_with_cell()

            swap_sites(site1, site2)

            post_swap_cost = 0
            if not site1.is_empty():
                cell1 = site1.element
                post_swap_cost += cell1.calc_nets_cost_with_cell()
            if not site2.is_empty():
                cell2 = site2.element
                post_swap_cost += cell2.calc_nets_cost_with_cell()

            delta_c = post_swap_cost - pre_swap_cost 

            r = random.random()
            if r < math.exp(-delta_c / T):
                circuit.total_cost += delta_c
                # print("inner cost", circuit.total_cost)
                grid = circuit.grid
            else:
                # undo moves
                print("negative, undo")
                swap_sites(site2, site1)
                grid = circuit.grid
        T *= cooling_rate
        cost = circuit.calc_total_cost()
        total_cost_text.set(cost)
        update_canvas()
        # if delta_c  < 0:
        #     if r < math.exp(-delta_c / T):
        #         # undo moves
        #         print("negative, undo")
        #         swap_sites(site2, site1)
        # else: # take moves
        #     circuit.total_cost += delta_c
        #     print("inner cost", circuit.total_cost)
    return grid


            
            
        
    # T *= cooling_rate
    # print("T", T)
    # if T > threshold:
    #     root.after(1000, annealing, T, num_iterations, cooling_rate, threshold)
    #     update_canvas()
    #     cost = circuit.calc_total_cost()
    #     total_cost_text.set(cost)
        

    
def annealing1():
    # temp = initial_temp
    temp = 200
    # initial placement
    random_placement()
    print("initial cost", circuit.calc_total_cost())

    while (temp > 100):
        for _ in range(20):
            site1, site2 = select_sites()
            pre_swap_cost = 0
            if not site1.is_empty():
                cell1 = site1.element
                pre_swap_cost += cell1.calc_nets_cost_with_cell()
            if not site2.is_empty():
                cell2 = site2.element
                pre_swap_cost += cell2.calc_nets_cost_with_cell()

            swap_sites(site1, site2)

            post_swap_cost = 0
            if not site1.is_empty():
                cell1 = site1.element
                post_swap_cost += cell1.calc_nets_cost_with_cell()
            if not site2.is_empty():
                cell2 = site2.element
                post_swap_cost += cell2.calc_nets_cost_with_cell()

            delta_c = post_swap_cost - pre_swap_cost 

            r = random.random()
            if r < math.exp(-delta_c / temp):
                circuit.total_cost += delta_c
            else:
                # undo swap
                swap_sites(site2, site1)
            
        temp *= 0.6
        update_canvas()
        root.after(1000, annealing)

    cost = circuit.calc_total_cost()
    total_cost_text.set(cost)
    # best_cost = min(best_cost, total_cost)
    print('final cost = {}'.format(cost))





if __name__=='__main__':
    random.seed(0)
    logging.basicConfig(filename='placement_info_log.log', filemode='w',level=logging.INFO)
    # best_cost = float("inf")
    # hex_colors = create_hex_color_list()

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
    stats_frame.grid(column=1, row=0)

    # setup canvas frame (contains benchmark label and canvas)
    filename = StringVar()
    benchmark_lbl = ttk.Label(canvas_frame, textvariable=filename)
    benchmark_lbl.grid(column=0, row=0)

    canvas = Canvas(canvas_frame, width=640, height=480, bg="dark grey")
    canvas.grid(column=0, row=1, padx=5, pady=5)

    # setup button frame (contains buttons)
    open_btn = ttk.Button(btn_frame, text="load file", command=load_file_button)
    open_btn.grid(column=0, row=0, padx=5, pady=5)
    place_btn = ttk.Button(btn_frame, text="init place", command=init_place)
    place_btn.grid(column=1, row=0, padx=5, pady=5)
    place_btn.state(['disabled'])
    anneal_btn = ttk.Button(btn_frame, text="Anneal", command=placing)
    anneal_btn.grid(column=2, row=0, padx=5, pady=5)
    anneal_btn.state(['disabled'])

    # setup stats frame (contains statistics)
    total_cost_text = StringVar()
    total_cost_text.set('-')
    ttk.Label(stats_frame, text="cost:").grid(column=1, row=1)
    cost_lbl = ttk.Label(stats_frame, textvariable=total_cost_text)
    cost_lbl.grid(column=2, row=1)

    # best_cost_text = StringVar()
    # best_cost_text.set('-')
    # ttk.Label(stats_frame, text="best cost:").grid(column=1, row=2)
    # cost_lbl = ttk.Label(stats_frame, textvariable=best_cost_text)
    # cost_lbl.grid(column=2, row=2)

    # run main event loop for gui
    root.mainloop()


