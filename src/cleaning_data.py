import polars as pl 
df = pl.read_csv('data/raw/OnlineRetail.csv' , schema_overrides={'InvoiceNo' : pl.Utf8 , 'StockCode' : pl.Utf8} , encoding= 'latin1')

def data_cleaning (data : pl.DataFrame) -> pl.DataFrame:
    data_clean = (
        data
        .drop_nulls(subset=['Description'])
        .filter(
            ~ pl.col('InvoiceNo').str.contains(r'[a-zA-Z]') ,
            pl.col('Quantity') > 0 ,
            pl.col('UnitPrice') > 0
        )
        .with_columns([
            pl.when(pl.col('CustomerID').is_null())
            .then(pl.lit('no')) 
            .otherwise(pl.lit('yes'))
            .alias('IsRegistered') ,
            pl.col('InvoiceNo').cast(pl.Int64) ,
            pl.col('StockCode').str.strip_chars().str.to_lowercase() ,
            pl.col('Description').str.strip_chars().str.to_lowercase() ,
            pl.col('Country').str.to_lowercase() ,
            pl.col("InvoiceDate").str.strptime(pl.Datetime, format="%m/%d/%Y %H:%M", strict=False)
        ])
        .drop('CustomerID')
        .unique()
    )
    return data_clean
print(data_cleaning(df))