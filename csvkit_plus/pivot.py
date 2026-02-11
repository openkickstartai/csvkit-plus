"""Pivot table operation."""
import csv
from collections import defaultdict
from typing import List, Dict

def pivot(file: str, rows: str, cols: str, values: str, agg: str = 'sum') -> str:
    with open(file, newline='') as f:
        data = list(csv.DictReader(f))
    if not data: return ''
    # Collect unique column values
    col_vals = sorted(set(r.get(cols, '') for r in data))
    # Aggregate
    table = defaultdict(lambda: defaultdict(list))
    for r in data:
        rk = r.get(rows, '')
        ck = r.get(cols, '')
        try: table[rk][ck].append(float(r.get(values, 0)))
        except ValueError: pass
    # Format output
    lines = [','.join([rows] + col_vals)]
    for rk in sorted(table.keys()):
        vals = []
        for ck in col_vals:
            cell = table[rk][ck]
            if agg == 'sum': vals.append(str(sum(cell)) if cell else '0')
            elif agg == 'avg': vals.append(str(round(sum(cell)/len(cell), 2)) if cell else '0')
            elif agg == 'count': vals.append(str(len(cell)))
            elif agg == 'min': vals.append(str(min(cell)) if cell else '0')
            elif agg == 'max': vals.append(str(max(cell)) if cell else '0')
            else: vals.append(str(sum(cell)) if cell else '0')
        lines.append(','.join([rk] + vals))
    return '\n'.join(lines)
