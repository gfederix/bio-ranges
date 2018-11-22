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
         0         1 |      10.0       0.1
         1         1 |      11.0      0.11
         2         1 |      12.0      0.12
''')

def test_long_range_with_data_show(test_out, capsys):
    Ranges(start=range(13), width=1, data = {
        'score' : np.array(range(0, 13), dtype="f4"),
        'fscore' : np.array(range(0, 13), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 13 ranges:
     start     width |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         1 |       0.0       0.0
         1         1 |       1.0      0.01
         2         1 |       2.0      0.02
         3         1 |       3.0      0.03
         4         1 |       4.0      0.04
...
         9         1 |       9.0      0.09
        10         1 |      10.0       0.1
        11         1 |      11.0      0.11
        12         1 |      12.0      0.12
''')
    Ranges(start=range(10), width=1, data = {
        'score' : np.array(range(0, 10), dtype="f4"),
        'fscore' : np.array(range(0, 10), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 10 ranges:
     start     width |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         1 |       0.0       0.0
         1         1 |       1.0      0.01
         2         1 |       2.0      0.02
         3         1 |       3.0      0.03
         4         1 |       4.0      0.04
         5         1 |       5.0      0.05
         6         1 |       6.0      0.06
         7         1 |       7.0      0.07
         8         1 |       8.0      0.08
         9         1 |       9.0      0.09
''')

