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
class NotImplemented(Exception):
    pass 

import sys
from itertools import repeat
from collections import namedtuple, defaultdict

import numpy as np
import pandas as pd

from .exeptions import NotImplemented

def log(*args):
    print(*args, file=sys.stderr)
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
                 names=None, data=None, dtype=None):
        self._data = pd.DataFrame(data=data)
        # default data
        if names is not None:
            self._data['name'] = names
            self._update_index_cols()

        # Create array
        self._pos = np.zeros(len(start), dtype=self.PRI_TYPES)
        self._pos['start'] = start
        if width is not None and end is not None:
            raise Exception("End and width cannot be defined bouth in Range class.")
        if width is not None:
            self._pos['width'] = width
        elif end is not None:
            self._pos['width'] = end - self._pos['start'] + 1
    @classmethod
    def from_raw(cls, pos, data_frame):
        self = cls.__new__(cls)
        self._data = data_frame
        self._pos  = pos
        return self
        
    def _update_index_cols(self):
        ix = list(set(self.INDEX_COLS) &
                  (set(self.colnames()) + set(self._data.index.names)))
        self._data = self._data.set_index(ix)

    def width(self):
        return(len(self._pos))

    # Equality Test
    def samerange(self, ran):
        print(self._pos, ran._pos)
        print(self._pos.dtype, ran._pos.dtype)
        return all(self._pos == ran._pos)

    def equals(self, range):
        return all(self._pos == range._pos) and self._data.equals(range._data)

    # TODO1:
    def resize(self, width, fix):
        raise NotImplemented
    def from_arry(array):
        raise NotImplemented
    def sliding_window(self, funct, width, step, pool=None):
        raise NotImplemented
    def overlap(self, x):
        raise NotImplemented

    # TODO2:
    def shift():
        raise NotImplemented

    # TODO3:
    def feflect():
        raise NotImplemented
    def narrow():
        raise NotImplemented
    def promoters():
        raise NotImplemented

    # Emulating container types
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.get_col(key)
        else:
            return Ranges.from_raw(self._pos.__getitem__(key), self._data.__getitem__(key))

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
        raise NotImplemented

    # Ranges Representation:
    def show(self, data_delim=" |"):
        def pr(*args):
            out = ''
            for arg in args:
                if isinstance(arg, np.float):
                    out +="{:>10.4}".format(arg)
                else:
                    out +="{:>10}".format(arg)
            print(out, sep="", end="") 
        print("Range", "with", self.width(), "ranges:")
        # Print Table header:
        pr("start", "width")
        if self.ncols():
            print(data_delim, end="")
            for name in self.colnames():
                pr(name)
        print()
        # Data Type printing:
        pr(
            *map(lambda kw: '<{}>'.format(self._pos[kw].dtype), ['start', 'width']))
        if self.ncols():
            print(data_delim, end="")
            for dtype in self._data.dtypes:
                pr('<{}>'.format(dtype))
        print()
        # Print Tabel body:
        def pri_row_printer(start, width):
            pr(start, width)

        def data_row_printer(data_row):
            # print(data_row, len(data_row))
            if len(data_row):
                print(data_delim, end="")
                for cell in data_row:
                    pr(cell)
        for i, (start, width, *data) in enumerate(self.itertuples(), 1):
            # log(start, "!!", width)
            if i > self.MAX_ROW_SHOW // 2 and self.nrows() > self.MAX_ROW_SHOW:
                print("...")
                # print(self)
                # print(self[- self.MAX_ROW_SHOW // 2:])
                for start, width, *data_row in self[1 - self.MAX_ROW_SHOW // 2:].itertuples():
                    pri_row_printer(start, width)
                    data_row_printer(data_row)
                    print()
                break
            else:
                pri_row_printer(start, width)
                data_row_printer(data)
                print()

    def itertuples(self):
        return IterTuples(self)
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
    def read(cls, path, format="delim"):
        raise NotImplemented

    @classmethod
    def read_delim(cls, path, sep='\t', comment_char="#"):
        with open(path, "r") as fh:
            start_list, end_list = [], []
            data_dict = defaultdict(list)
            comment = ""
            for line in fh:
                if line.startswith(comment_char):
                    comment += line
                    continue
                start, end, *data = line.strip().split(sep)
                if start == 'start' and end == 'end':
                    data_cols = data
                    continue
                start_list += [int(start)]
                end_list += [int(end)]
                if data_cols is None:
                    data_cols = list(range(len(data)))
                for key, val in zip(data_cols, data):
                    data_dict[key] = data_dict[key] + [val]
            print(data_dict)
            for key in data_dict.keys():
                first_val = data_dict[key][0]
                if first_val.startswith("0."):
                    data_dict[key] = np.array(data_dict[key], dtype='f4')
                else:
                    try:
                        int(first_val)
                        data_dict[key] = np.array(data_dict[key], dtype='i4')
                    except ValueError:
                        pass
                    
                
        return(cls(start=start_list, end=end_list, data=data_dict))
    
    @classmethod
    def read_csv(cls, path):
        raise NotImplemented

    def write(self, path, format="delim"):
        raise NotImplemented

    def to_csv(self, path):
        raise NotImplemented

    def to_delim(self, path, sep="\t"):
        with open(path, "w") as fh:
            fh.write(sep.join(['start', 'end'] + self.colnames()) + "\n")
            for start, width, *data in self.itertuples():
                end = start + width - 1
                line = sep.join(map(str, [start, end] + data)) + '\n'
                fh.write(line)


# Range Iterator classes
class IterTuples:
    def __init__(self, ranges):
        self.ranges = ranges
        self.ipos  = iter(ranges._pos)
        if len(ranges._data):
            self.idt   = iter(ranges._data.itertuples(False))
        else:
            self.idt = None
        self.Row = namedtuple("Row", ["start", "width"] + list(ranges._data))
    def __iter__(self):
        return self
    def __next__(self):
        args = [x for x in next(self.ipos)]
        if self.idt is not None:
            dt = list(next(self.idt))
        else:
            dt = tuple()
        args+= dt
        return(self.Row(*args))

