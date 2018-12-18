#cython: language_level=3
# from cpython cimport array
# import array
import numpy as np
cimport numpy as np
cimport cython
from libc.stdlib cimport qsort
from cython cimport view

cdef int* start_p
cdef int* end_p
cdef int compar_by_satart_width(const void* a, const void* b) nogil:
    global start_p, end_p
    ai = (<int*>a)[0]
    bi = (<int*>b)[0]
    cdef int ret = start_p[ai] - start_p[bi]
    if ret !=0:
        return ret
    return end_p[bi] - end_p[ai]

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int[::1] order_by_start_width(int[::1] index, int[::1] start, int[::1] end) nogil:
    """
    return order of array first sorted by start then sorted by width
    np.ndarray[np.int_t,ndim=1]
    """
    global start_p, end_p
    cdef size_t size = start.shape[0]
    cdef int* index_p = &index[0]
    for i in range(size):
        index_p[i] = i
    start_p = &start[0]
    end_p = &end[0]
    qsort(index_p, size, sizeof(int), compar_by_satart_width)
    return index

cpdef int find_span(int[::1] index,  int i_start, int i_end,
                    int[::1] start, int[::1] end) nogil:
    cdef int width = 0
    cdef int idx = 0
    for i in range(i_start, i_end):
        idx = index[i]
    return width
