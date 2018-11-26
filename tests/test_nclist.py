import pytest
import numpy as np
# import pyximport
# pyximport.install()
from bioRanges.nclist import order_by_start_width

def test_nclist_sort():
    #                 0  1   2  3  4
    start = np.array([1, 5,  5, 6, 3], dtype="i")
    end = np.array([2, 3, 10, 8, 4], dtype="i")
    index = np.array(range(5), dtype=np.intc)
    o = order_by_start_width(index, start, end)
    print(o)
    for i in o:
        print(i)
    assert all(o == np.array([0, 4, 2, 1, 3]))

