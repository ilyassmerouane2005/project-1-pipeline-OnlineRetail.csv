# Online Retail Data Cleaning Pipeline

A small data engineering project that takes the raw **Online Retail** CSV, detects data quality problems, fixes them, and exports clean datasets as **Parquet** and a **DuckDB** database.

The cleaning is implemented twice, once with **Polars** and once with **DuckDB SQL**, so you can compare both approaches on the same data.

## What it does

1. **Checks data quality** and reports the percentage of issues in each column.
2. **Cleans the data** by fixing the issues found.
3. **Exports** the result to `Parquet` (Polars) and a `DuckDB` table (DuckDB).

## Data quality issues found and how they are fixed

| # | Column | Issue | Fix |
|---|--------|-------|-----|
| 1 | All | Duplicate rows | Remove duplicates |
| 2 | `Description` | ~0.27% missing values | Drop those rows |
| 3 | `CustomerID` | Many missing values | Drop the column and create `IsRegistered` (`yes` / `no`) |
| 4 | `InvoiceNo` | ~1.71% contain letters (e.g. cancellations like `C536379`) | Drop those rows and cast to integer |
| 5 | `StockCode` | Inconsistent case and whitespace | Trim and lowercase |
| 6 | `Description` | Inconsistent case and whitespace | Trim and lowercase |
| 7 | `Quantity` | ~1.96% are `<= 0` | Drop those rows |
| 8 | `UnitPrice` | ~0.46% are `<= 0` | Drop those rows |
| 9 | `Country` | Inconsistent case | Lowercase |
| 10 | `InvoiceDate` | Stored as text | Cast to datetime |

## Project structure

```
.
├── data/
│   ├── raw/                  # OnlineRetail.csv (input)
│   └── processed/            # OnlineRetail.parquet, OnlineRetail.db (output)
├── src/
│   ├── __init__.py
│   ├── cleaning_data.py      # Polars cleaning function
│   ├── duckdb_cleaning.py    # DuckDB SQL cleaning
│   ├── check_data_quality.py # Polars data quality checks
│   └── duckdb_checking.py    # DuckDB data quality checks
├── tests/
│   ├── __init__.py
│   └── test_cleaning_data.py # pytest unit test
├── main.py                   # Runs the full pipeline
├── requirements.txt
└── README.md
```

## Tech stack

- Python 3
- [Polars](https://pola.rs/)
- [DuckDB](https://duckdb.org/)
- pytest

## Getting started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset at data/raw/OnlineRetail.csv
```

## Usage

Run the data quality checks (optional):

```bash
python -m src.check_data_quality
python -m src.duckdb_checking
```

Run the full cleaning pipeline:

```bash
python main.py
```

Outputs:

- `data/processed/OnlineRetail.parquet` (Polars)
- `data/processed/OnlineRetail.db` with the table `CleanRetail` (DuckDB)

Query the result with DuckDB:

```python
import duckdb

con = duckdb.connect("data/processed/OnlineRetail.db")
print(con.sql("SELECT Country, COUNT(*) AS orders FROM CleanRetail GROUP BY Country ORDER BY orders DESC LIMIT 5"))
```

## Tests

```bash
pytest
```

## Dataset

[Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail) from the UCI Machine Learning Repository: transactions of a UK-based online retailer between 2010 and 2011.

## License

This project is licensed under the [MIT License](LICENSE).
