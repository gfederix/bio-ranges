"""
Nested Containment List Realization
From article: 
Nested Containment List (NCList): a new algorithm for accelerating interval
query of genome alignment and interval databases

https://doi.org/10.1093/bioinformatics/btl647

see also Bioconductor IRanges pdf too

Propoused numpy structure for ranged data without pandas:

>>> np.array([(1,2, (3,4)),], dtype=[ ("start", 'u4'), ("length", 'u4'), ("data", [('name', 'f4'), ("score", 'b')] )  ] )
array([(1, 2, (3., 4))],
      dtype=[('start', '<u4'), ('length', '<u4'), ('data', [('name', '<f4'), ('score', 'i1')])])

>>> np.array([(1+x,2+x, (3,4)) for x in range(10)], dtype=[ ("start", 'u4'), ("length", 'u4'), ("data", [('name', 'f4'), ("score", 'b')] )  ] )
array([( 1,  2, (3., 4)), ( 2,  3, (3., 4)), ( 3,  4, (3., 4)),
       ( 4,  5, (3., 4)), ( 5,  6, (3., 4)), ( 6,  7, (3., 4)),
       ( 7,  8, (3., 4)), ( 8,  9, (3., 4)), ( 9, 10, (3., 4)),
       (10, 11, (3., 4))],
      dtype=[('start', '<u4'), ('length', '<u4'), ('data', [('name', '<f4'), ('score', 'i1')])])

Ranges with pandas:
r._pos == NCList with sequence start and width
r._data == pandas DataFrame

----------------

lGPL3+ or leter
(c) Fyodor P. Goncharov gfederix@gmail.com
"""
import numpy as np
import pandas as pd
from itertools import repeat

class Ranges():
    PRI_TYPES = [('start', 'u4'), ('width', 'u4')]
    DATA_TYPES = []
    INDEX_COLS = ['names']
    @property
    def DTYPE(self):
        # if not len(self.DATA_TYPES):
        #     return(self.PRI_TYPES)
        # else:
        #     return(self.PRI_TYPES + [('data', self.DATA_TYPES)])
        return(self.PRI_TYPES + [('data', self.DATA_TYPES)])
    MAX_ROW_SHOW = 10

    def __init__(self, start, end=None, width=None,
                 names=None, score=None, dtype=None):
        self._data = pd.DataFrame()
        # default data
        if score is not None:
            self._data['score'] = score
        if names is not None:
            self._data['name'] = names
            self._update_index_cols()

        # Create array
        self._pos = np.zeros(len(start), dtype=self.DTYPE)
        self._pos['start'] = start
        if width is not None and end is not None:
            raise Exception("End and width cannot be defined bouth in Range class.")
        if width is not None:
            self._pos['width'] = width
        elif end is not None:
            self._pos['width'] = end - self._pos['start'] + 1

    def _update_index_cols(self):
        ix = list(set(self.INDEX_COLS) &
                  (set(self.colnames()) + set(self._data.index.names)))
        self._data = self._data.set_index(ix)

    def width(self):
        return(len(self._pos))

    # TODO1:
    def resize(self, width, fix):
        pass
    def from_arry(array):
        pass
    def sliding_window(self, funct, width, step, pool=None):
        pass
    def overlap(self, x):
        pass

    # TODO2:
    def shift():
        pass

    # TODO3:
    def feflect():
        pass
    def narrow():
        pass
    def promoters():
        pass

    # Emulating container types
    def __getitem__(self, key):
        if isinstance(key, str):
            self.get_col(key)

    def get_col(self, key, default=None):
        """
        range.get_col(key, default)
        if no key and default not set, function rice exception
        """
        if key in self.PRI_TYPES:
            return(self._pos[key])
        elif key in self.colnames():
            return(self._data[key])
        elif default is not None:
            return(default)
        raise Exception("Wrong index key")

    def __setitem__(self, key, value):
        pass

    # Ranges Representation:
    def show(self, data_delim="|"):
        def pr(*args, **kwargs):
            args = ''.join(map(lambda x: '{:>10}'.format(x), args))
            print(args, sep="", **kwargs) 
        
        print("Range", "with", self.width(), "ranges:")
        # Print Table header:
        pr("start", "width", end="")
        # if self.nrows():
        #     print(data_delim, end="\t")
        #     for name, type in self.DATA_TYPES:
        #         print(name, end="\t")
        print()
        # Data Type printing:
        pr(
            *map(lambda kw: '<{}>'.format(self._pos[kw].dtype), ['start', 'width']))
        # pr('<' + str(self._pos['start'].dtype) + '>',
        #    '<' + str(self._pos['width'].dtype) + '>')

        
        # Print Tabel body:
        def pri_row_printer(start, width):
            pr(start, width, end="")

        def data_row_printer(data_row):
            if len(data_row):
                print(end="\t")
                print(data_delim, end="\t")
                for cell in data_row:
                    pr(cell, end="\t")
            print()

        for i, (start, width, data_row) in enumerate(self._pos):
            pri_row_printer(start, width)
            data_row_printer(data_row)
            if i > self.MAX_ROW_SHOW // 2 and self.nrows() > self.MAX_ROW_SHOW:
                for start, width, data_row in self._pos[- self.MAX_ROW_SHOW // 2:]:
                    pri_row_printer(start, width)
                data_row_printer(data_row)
                break

    # R like data.frame function:
    def nrows(self):
        return self._pos.shape[0]

    def ncols(self):
        return len(self._data.columns)

    def colnames(self):
        return list(self._data)

    # Pandas methods:
    def types(self):
        return self._data.types
                  
    # Ranges class Data model
    def __repr__(self):
        print("<IRange", "width:", self.width(),
              "with", self.ncols(), self.colnames(),
              "data cols", ">")
        repr(self._pos)

    def __str__(self):
        self.show()

    def __len__(self):
        return self.width()

    # Ranges I/O:
    @classmethod
    def from_csv(path):
        pass
    @classmethod
    def from_delim(path):
        pass
    @classmethod
    def read(path, format="delim"):
        pass
        
    def to_csv(path):
        if format not in ('csv', ):
            pass

    def write(path, format="delim"):
        pass

    def to_delim(path):
        pass
