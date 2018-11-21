import pytest
import numpy as np
from bioRanges import Ranges
@pytest.fixture
def test_out(capsys):
    capture = capsys.readouterr()
    def test(out):
        assert capture == out
    return test

def test_range_creation():
    r = Ranges(start=range(10), width=1)

def test_short_range_show(test_out, capsys):
    Ranges(start=range(3), width=1).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 3 ranges:
     start     width
  <uint32>  <uint32>
         0         1
         1         1
         2         1
''')

def test_short_range_with_data_show(test_out, capsys):
    Ranges(start=range(3), width=1, data = {
        'score' : np.array(range(10, 13), dtype="f4"),
        'fscore' : np.array(range(10, 13), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 3 ranges:
     start     width |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         1 |        10
         1         1 |        11
         2         1 |        12
''')
   
