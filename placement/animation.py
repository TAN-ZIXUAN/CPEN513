import math
import sys
import logging
from tkinter import filedialog, ttk
from ttkthemes import ThemedStyle
import tkinter as tk

from site import Site
from cell import Cell
from circuit import Circuit
from net import Net

filename = "cm151a.txt"
default_file = "ass2_files/" + filename

def create_hex_color_list(color_file="hex_color.txt"):
    """return hex color list"""
    hex_color = [] # 949 colors 
    with open(color_file, 'r') as f:
        for line in f:
            l = line.strip().split()
            # print(line[-1])
            hex_color.append(l[-1])

def load_file(*args):
    """load benchmark files"""
    file = filedialog.askopenfilename(initialdir="ass2_files/",filetypes=(("Text File", "*.txt"),("All Files","*.*")), title="choose a file")
    if not file:
        return

    logging.info("loading file:{file}".format(file=file))
    circuit.


