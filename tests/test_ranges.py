import pytest
from bioRanges import Ranges

def test_creation():
    r = Ranges(start=range(10), width=1)
    r.show()
