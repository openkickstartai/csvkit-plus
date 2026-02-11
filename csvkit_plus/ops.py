"""Core operations."""
import csv
import random
from typing import List, Dict

def select_columns(file: str, columns: List[str]):
    with open(file, newline='') as f:
        for row in csv.DictReader(f):
            yield {k: row.get(k, '') for k in columns}

def filter_rows(file: str, condition: str) -> List[Dict]:
    # Simple key>value or key=value filtering
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if _eval_condition(row, condition):
                rows.append(row)
    return rows

def _eval_condition(row, cond):
    for op in ['>=', '<=', '!=', '>', '<', '=']:
        if op in cond:
            key, val = cond.split(op, 1)
            key, val = key.strip(), val.strip()
            cell = row.get(key, '')
            try:
                cell_n, val_n = float(cell), float(val)
                if op == '>': return cell_n > val_n
                if op == '<': return cell_n < val_n
                if op == '>=': return cell_n >= val_n
                if op == '<=': return cell_n <= val_n
                if op == '!=': return cell_n != val_n
                return cell_n == val_n
            except ValueError:
                if op == '=': return cell == val
                if op == '!=': return cell != val
    return True

def dedup_rows(file: str, key: str) -> List[Dict]:
    seen = set()
    result = []
    with open(file, newline='') as f:
        for row in csv.DictReader(f):
            k = row.get(key, '')
            if k not in seen:
                seen.add(k)
                result.append(row)
    return result

def sample_rows(file: str, n: int) -> List[Dict]:
    with open(file, newline='') as f:
        rows = list(csv.DictReader(f))
    return random.sample(rows, min(n, len(rows)))

def join_csvs(file_a: str, file_b: str, on: str) -> List[Dict]:
    with open(file_a, newline='') as f:
        a_rows = {row[on]: row for row in csv.DictReader(f)}
    result = []
    with open(file_b, newline='') as f:
        for row in csv.DictReader(f):
            key = row.get(on, '')
            if key in a_rows:
                merged = {**a_rows[key], **row}
                result.append(merged)
    return result
