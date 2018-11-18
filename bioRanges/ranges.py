"""
Nested Containment List Realization
From article: 
Nested Containment List (NCList): a new algorithm for accelerating interval
query of genome alignment and interval databases

https://doi.org/10.1093/bioinformatics/btl647

see also Bioconductor IRanges pdf too

Propoused numpy structure for ranged data
>> np.array([(1,2, (3,4)),], dtype=[ ("start", 'u4'), ("length", 'u4'), ("data", [('name', 'f4'), ("score", 'b')] )  ] )

np.array([(1+x,2+x, (3,4)) for x in range(10)], dtype=[ ("start", 'u4'), ("length", 'u4'), ("data", [('name', 'f4'), ("score", 'b')] )  ] )


----------------

lGPL3+ or leter
(c) Fyodor P. Goncharov gfederix@gmail.com
"""
import numpy as np
from itertools import repeat

class Ranges():
    PRI_TYPES = [('start', 'u4'), ('width', 'u4')]
    DATA_TYPES = []

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
        # default data
        if score is not None:
            self.DATA_TYPES += [('score', 'f4')]
        if names is not None:
            self.DATA_TYPES += [('score', 'f4')]

        # Create array
        self.data = np.zeros(len(start), dtype=self.DTYPE)
        self.data['start'] = start
        if width is not None and end is not None:
            raise Exception("End and width cannot be defined bouth in Range class.")
        if width is not None:
            self.data['width'] = width
        elif end is not None:
            self.data['width'] = end - self.data['start'] + 1

            
    def width(self):
        return(len(self.data))

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
            return(self.data[key])
        elif key in self.DATA_TYPES:
            return(self.data['data'][key])
        elif default is not None:
            return(default)
        raise Exception("Wrong index key")

    def __setitem__(self, key, value):
        pass

    # Ranges Representation:
    def show(self, data_delim="|"):
        print("IRange", "with", self.width(), "ranges:")
        # Print Table header:
        for name, type in self.PRI_TYPES:
            print(name, end="\t")
        if len(self.DATA_TYPES):
            print(data_delim, end="\t")
            for name, type in self.DATA_TYPES:
                print(name, end="\t")
            print()

        # Print Tabel body:
        def pri_row_printer(start, width):
            print(start, start + width - 1, sep="\t", end="\t")

        def data_row_printer(data_row):
            print(data_delim, end="\t")
            for cell in data_row:
                print(cell, end="\t")
            print()

        for i, (start, width, data_row) in enumerate(self.data):
            pri_row_printer(start, width)
            data_row_printer(data_row)
            if i > self.MAX_ROW_SHOW // 2 and self.nrow() > self.MAX_ROW_SHOW:
                for start, width, data_row in self.data[- self.MAX_ROW_SHOW // 2:]:
                    pri_row_printer(start, width)
                data_row_printer(data_row)
                break

    # R like table size function:
    def nrows(self):
        return self.data.shape[0]

    def ncols(self):
        return len(self.DATA_TYPES)

    # Ranges class Data model
    def __repr__(self):
        data_cols = 0
        try:
            data_cols = self.data["data"].shape[1]
        except AttributeError:
            pass
        print("<IRange", "width:", self.width(), "with", data_cols,
              "data cols", ">")
        repr(self.data)

    def __str__(self):
        self.show()

    def __len__(self):
        return(self.width())

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
