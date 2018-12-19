import pytest
import numpy as np
# import pyximport
# pyximport.install()
from bioRanges.nclist import order_by_start_width, index

def test_nclist_sort():
    #                 0  1  2   3  4
    start = np.array([1, 5,  5, 6, 3], dtype="i")
    end   = np.array([2, 7, 10, 9, 5], dtype="i")
    # Raw index
    # I 123456789012345
    # 0 --
    # 1     ---
    # 2     -------
    # 3      ---
    # 4    --
    idx = order_by_start_width(start, end)
    assert all(idx == np.array([0, 4, 2, 1, 3]))
    # Sorted index
    # I 123456789012345
    # 0 --        
    # 4   --      
    # 2     -------
    # 1     ---
    # 3      ---

    index(start, end, idx)
    # NCList index
    #   I 12345678901
    # 0 1     ---    
    # 1 3      ---   
    # 2 0 --         
    # 3 4   --       
    # 4 2     -------
    #
    # N L
    # 0 2 {}
    # 2 3 {2:0, }
    #
    # (2,3, {2: (0,2, {})}
    pass
