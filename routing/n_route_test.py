import pytest
import sys
from n_route import route_all
from n_route import route_with_shuffle
from n_route import route_with_permutation
from n_route import route_LeeMoore
from n_route import route_a_star
from n_route import reload_layout

from layout import Layout
from cell import Cell
from net import Net
import config as c


#load file
layout = Layout()
default_file = "benchmarks/example.infile"
if len(sys.argv) < 2: # not parsing file argument. use default file
    print("please put file path as argument[1]")
    print("default file loaded", default_file)
    file_path = default_file
else:
    file_path= sys.argv[1] # file name or path
    print("loaded file", file_path)
if not file_path:
    print("no file selected!") 
    sys.exit()
c.FILEPATH = file_path
reload_layout(file_path)

def test_route_all():
    val = route_all()
    assert val == 2

# def test_route_with_shuffle():
#     return

# def test_route_with_permutation():
#     return

# def test_route_LeeMoore():
#     return

# def test_route_a_star():
#     return
