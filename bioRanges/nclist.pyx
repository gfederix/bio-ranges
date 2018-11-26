# from cpython cimport array
# import array
import numpy as np
cimport cython
from libc.stdlib cimport qsort

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
