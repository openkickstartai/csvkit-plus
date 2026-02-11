"""Tests."""
import os, csv, tempfile
from csvkit_plus.pivot import pivot

def _mk(rows, headers):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader(); w.writerows(rows)
    f.flush(); return f.name

def test_pivot_sum():
    f = _mk([{'region':'US','q':'Q1','rev':'100'},{'region':'US','q':'Q2','rev':'200'},
             {'region':'EU','q':'Q1','rev':'150'}], ['region','q','rev'])
    result = pivot(f, 'region', 'q', 'rev', 'sum')
    assert 'US' in result
    assert 'EU' in result
    lines = result.strip().split('\n')
    assert len(lines) == 3  # header + 2 regions
    os.unlink(f)

def test_pivot_count():
    f = _mk([{'a':'x','b':'1','c':'10'},{'a':'x','b':'1','c':'20'},{'a':'y','b':'2','c':'30'}], ['a','b','c'])
    result = pivot(f, 'a', 'b', 'c', 'count')
    assert '2' in result  # x,1 appears twice
    os.unlink(f)
