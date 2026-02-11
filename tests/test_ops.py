"""Tests."""
import os, csv, tempfile
from csvkit_plus.ops import select_columns, filter_rows, dedup_rows, sample_rows, join_csvs, _eval_condition

def _mk_csv(rows, headers):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)
    f.flush()
    return f.name

def test_select():
    f = _mk_csv([{'name':'Alice','age':'30','city':'NYC'}], ['name','age','city'])
    rows = list(select_columns(f, ['name','age']))
    assert rows[0] == {'name':'Alice','age':'30'}
    os.unlink(f)

def test_dedup():
    f = _mk_csv([{'id':'1','v':'a'},{'id':'1','v':'b'},{'id':'2','v':'c'}], ['id','v'])
    rows = dedup_rows(f, 'id')
    assert len(rows) == 2
    os.unlink(f)

def test_sample():
    f = _mk_csv([{'id':str(i)} for i in range(100)], ['id'])
    rows = sample_rows(f, 5)
    assert len(rows) == 5
    os.unlink(f)

def test_join():
    a = _mk_csv([{'id':'1','name':'Alice'},{'id':'2','name':'Bob'}], ['id','name'])
    b = _mk_csv([{'id':'1','score':'95'},{'id':'3','score':'80'}], ['id','score'])
    rows = join_csvs(a, b, 'id')
    assert len(rows) == 1
    assert rows[0]['name'] == 'Alice'
    assert rows[0]['score'] == '95'
    os.unlink(a); os.unlink(b)

def test_eval_condition():
    row = {'age': '30', 'name': 'Alice'}
    assert _eval_condition(row, 'age>25')
    assert not _eval_condition(row, 'age>35')
    assert _eval_condition(row, 'name=Alice')
