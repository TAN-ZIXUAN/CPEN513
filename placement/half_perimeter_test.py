
import numpy as np
import pytest

"""
test for the function calculate half perimeter
half_perimeter = (max_row - min_row) + (max_col - min_col)

run the test: `python -m pytest half_perimeter_test`
"""
list0 = [(1,2), (0,0)] # half_p = (1-0) + (2-0) = 3
list1 = [(1,2), (2,3), (4,5), (6,7), (8,9), (10, 11)] # half_p = (10-1) + (11-2) = 18
list2 = [] # Empty list # return 0



def calc_half_perimeter(list):
    if not list:
        return 0
    
    list_sort_by_row = sorted(list, key = lambda x:x[0])
    min_row = list_sort_by_row[0][0]
    max_row = list_sort_by_row[-1][0]

    list_sort_by_col = sorted(list, key = lambda x:x[1])
    min_col = list_sort_by_col[0][1]
    max_col = list_sort_by_col[-1][1]

    half_perimeter = (max_row - min_row) + (max_col - min_col)

    return half_perimeter

tests = [(list0, 3), (list1, 18), (list2, 0)]


@pytest.mark.parametrize("test_input, expected", tests)
def test_route_with_shuffle(test_input, expected):
  assert calc_half_perimeter(test_input) == expected