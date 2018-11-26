import pytest
from pathlib import Path
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
     start       end
  <uint32>  <uint32>
         0         0
         1         1
         2         2
''')

def test_short_range_with_data_show(test_out, capsys):
    Ranges(start=range(3), width=1, data = {
        'score' : np.array(range(10, 13), dtype="f4"),
        'fscore' : np.array(range(10, 13), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 3 ranges:
     start       end |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         0 |      10.0       0.1
         1         1 |      11.0      0.11
         2         2 |      12.0      0.12
''')

def test_long_range_with_data_show(test_out, capsys):
    Ranges(start=range(13), width=1, data = {
        'score': np.array(range(0, 13), dtype="f4"),
        'fscore': np.array(range(0, 13), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 13 ranges:
     start       end |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         0 |       0.0       0.0
         1         1 |       1.0      0.01
         2         2 |       2.0      0.02
         3         3 |       3.0      0.03
         4         4 |       4.0      0.04
...
         9         9 |       9.0      0.09
        10        10 |      10.0       0.1
        11        11 |      11.0      0.11
        12        12 |      12.0      0.12
''')
    Ranges(start=range(10), width=1, data={
        'score': np.array(range(0, 10), dtype="f4"),
        'fscore': np.array(range(0, 10), dtype="f4") /100,
    }).show()
    x = capsys.readouterr().out
    assert x == (
'''Range with 10 ranges:
     start       end |     score    fscore
  <uint32>  <uint32> | <float32> <float32>
         0         0 |       0.0       0.0
         1         1 |       1.0      0.01
         2         2 |       2.0      0.02
         3         3 |       3.0      0.03
         4         4 |       4.0      0.04
         5         5 |       5.0      0.05
         6         6 |       6.0      0.06
         7         7 |       7.0      0.07
         8         8 |       8.0      0.08
         9         9 |       9.0      0.09
''')

def test_delim(tmpdir):
    path = Path(tmpdir, "delim.tab")
    rg1 = Ranges(start=range(13), width=1, data = {
        'score': np.array(range(0, 13), dtype="f4"),
        'fscore': np.array(range(0, 13), dtype="f4") /100,
    })
    rg1.to_delim(path)
    rg2 = Ranges.read_delim(path)
    assert rg1.samerange(rg2)
    assert rg1.equals(rg2)

def test_samerange():
    rg1 = Ranges(start=range(13), width=1, data = {
        'score': np.array(range(0, 13), dtype="f4"),
        'fscore': np.array(range(0, 13), dtype="f4") /100,
    })
    rg2 = Ranges(start=range(13), width=1)
    rg3 = Ranges(start=range(13), width=2)
    assert rg1.samerange(rg2)
    assert not rg2.samerange(rg3)
