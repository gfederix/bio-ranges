#cython: language_level=3
# from cpython cimport array
# import array
import numpy as np
cimport numpy as np
cimport cython
from libc.stdlib cimport qsort
from cython cimport view
from libc.stdlib cimport malloc, free
from libc.stdio cimport printf

cdef int* start_p
cdef int* end_p
ctypedef struct NLshift:
    int shift
    int len

ctypedef struct NLidx:
    int idx
    NLshift* ptr

cdef int compar_by_satart_width(const void* a, const void* b) nogil:
    global start_p, end_p
    ai = (<NLidx*>a).idx
    bi = (<NLidx*>b).idx
    cdef int ret = start_p[ai] - start_p[bi]
    if ret != 0:
        return ret
    return end_p[bi] - end_p[ai]

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void  _order_by_start_width(int[::1] start, int[::1] end, NLidx* idx_p) nogil:
    """
    return order of array first sorted by start then sorted by width
    np.ndarray[np.int_t,ndim=1]
    """
    global start_p, end_p
    cdef size_t size = start.shape[0]
    for i in range(size):
        idx_p[i].idx = i
        idx_p[i].ptr = NULL
    start_p = &start[0]
    end_p = &end[0]
    qsort(idx_p, size, sizeof(NLidx), compar_by_satart_width)

def order_by_start_width(int[::1] start, int[::1] end):
    cdef size_t size = start.shape[0]
    cdef NLidx *idx = <NLidx*> malloc(sizeof(NLidx) * size)
    _order_by_start_width(start, end, idx)
    return np.array([idx[i].idx for i in range(size)], dtype=np.intc)

cpdef void index(int[::1] start, int[::1] end, int[::1] idx) nogil:
    pass

cpdef int find_span(int[::1] index,  int i_start, int i_end,
                    int[::1] start, int[::1] end) nogil:
    cdef int width = 0
    cdef int idx = 0
    for i in range(i_start, i_end):
        idx = index[i]
    return width
