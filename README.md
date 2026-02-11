# csvkit-plus

Power tools for CSV wrangling. Streams large files.

## Install

```bash
git clone https://github.com/openkickstartai/csvkit-plus.git
cd csvkit-plus && pip install -e .
```

## Usage

```bash
# Inspect a CSV
csvkit-plus info data.csv

# Select columns
csvkit-plus select data.csv --columns name,email

# Filter rows
csvkit-plus filter data.csv --where 'age>30'

# Deduplicate
csvkit-plus dedup data.csv --key email

# Join two CSVs
csvkit-plus join a.csv b.csv --on id

# Sample random rows
csvkit-plus sample data.csv --n 100

# Convert
csvkit-plus convert data.csv --to json
```

## Testing

```bash
pytest -v
```
