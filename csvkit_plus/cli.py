"""CLI."""
import click
import csv
import json
import sys
import io
from csvkit_plus.ops import select_columns, filter_rows, dedup_rows, sample_rows, join_csvs

@click.group()
def main(): pass

@main.command()
@click.argument('file')
def info(file):
    """Show CSV info."""
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    click.echo(f"File: {file}")
    click.echo(f"Columns: {', '.join(rows[0].keys()) if rows else 'none'}")
    click.echo(f"Rows: {len(rows)}")

@main.command('select')
@click.argument('file')
@click.option('--columns', '-c', required=True)
def select_cmd(file, columns):
    """Select columns."""
    cols = [c.strip() for c in columns.split(',')]
    for row in select_columns(file, cols):
        click.echo(','.join(str(row.get(c, '')) for c in cols))

@main.command()
@click.argument('file')
@click.option('--key', '-k', required=True)
def dedup(file, key):
    """Remove duplicates by key."""
    rows = dedup_rows(file, key)
    if rows:
        w = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

@main.command()
@click.argument('file')
@click.option('--n', default=10, type=int)
def sample(file, n):
    """Random sample."""
    rows = sample_rows(file, n)
    if rows:
        w = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

@main.command()
@click.argument('file')
@click.option('--to', 'fmt', default='json')
def convert(file, fmt):
    """Convert CSV to other formats."""
    with open(file, newline='') as f:
        rows = list(csv.DictReader(f))
    if fmt == 'json':
        click.echo(json.dumps(rows, indent=2))
