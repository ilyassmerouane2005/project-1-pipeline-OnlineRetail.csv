import polars as pl
from src.cleaning_data import data_cleaning
from src.duckdb_cleaning import cleaning_data_duckdb
def main():
    print('Reading raw data')
    df_raw = pl.read_csv('data/raw/OnlineRetail.csv' , schema_overrides={'InvoiceNo' : pl.Utf8 , 'StockCode' : pl.Utf8} , encoding= 'latin1')
    print(f"Loaded {df_raw.height} raw rows.")
    df_clean = data_cleaning(df_raw)
    df_clean.write_parquet('data/processed/OnlineRetail.parquet')
    print(f"Success: {df_clean.height:,} cleaned rows saved to data/processed/OnlineRetail.parquet")
    cleaning_data_duckdb()
if __name__ == "__main__" :
    main()