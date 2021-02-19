import logging
import random
from site import Site
from tkinter import filedialog, ttk
from ttkthemes import ThemedStyle

import tkinter as tk

from cell import Cell
from circuit import Circuit
from net import Net


def initial_temp():
    temperature = 0
    
    return temperature

def random_swap_ceils():
    pass
def calc_cost():
    return 0
def if_meet_exit_criteria():
    return False



def simulated_annealing():
    temperature = initial_temp()
    iterations_num = 10 # num of iterations 
    
    while not if_meet_exit_criteria():
        pass
    else: # meet the exit criteria
        pass



def random_placement():
    num_sites = circuit.num_rows * circuit.num_cols
    random_sites_id_list = random.sample(range(num_sites), circuit.num_cells) # generate random (cell_id, site_id) list of size equals to num_sites
    for cell_id, random_site_id in enumerate(random_sites_id_list):
        site = circuit.get_site_by_id(random_site_id)
        cell = circuit.cell_list[cell_id]
        site.element = cell
        cell.row = site.row
        cell.col = site.col


def tk_gui():
    root = tk.Tk()
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
    open_btn = ttk.Button(btn_frame, text="load file", command=open_benchmark)
    open_btn.grid(column=0, row=0, padx=5, pady=5)
    place_btn = ttk.Button(btn_frame, text="Place", command=place)
    place_btn.grid(column=1, row=0, padx=5, pady=5)
    place_btn.state(['disabled'])
    anneal_btn = ttk.Button(btn_frame, text="Anneal", command=anneal)
    anneal_btn.grid(column=2, row=0, padx=5, pady=5)
    anneal_btn.state(['disabled'])

    # setup stats frame (contains statistics)
    cost_text = StringVar()
    cost_text.set('-')
    ttk.Label(stats_frame, text="cost:").grid(column=1, row=1)
    cost_lbl = ttk.Label(stats_frame, textvariable=cost_text)
    cost_lbl.grid(column=2, row=1)

    # run main event loop for gui
    root.mainloop()


def placed():
    """place the cells"""
    random_placement()
    circuit.cost = circuit.calc_total_cost
    

if __name__ == '__main__':
    logging.basicConfig(filename='placement_info_log.log', filemode='w',level=logging.INFO)
    random.seed(0)

    circuit = Circuit()
    


    




