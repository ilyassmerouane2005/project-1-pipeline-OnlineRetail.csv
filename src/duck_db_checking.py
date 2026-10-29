import duckdb
import polars as pl

path = "data/raw/OnlineRetail.csv"

detecting_query = f"""
with raw_data as (
    select * 
    from read_csv ('{path}' , encoding = 'latin1' , header = True , all_varchar = True)
)
select
    (select count(*) from raw_data) - (select count(*) from (select distinct * from raw_data)) as nbr_of_duplicates ,
    round(count(*) filter (where InvoiceNo is null) * 100.0 / count(*) , 2) as per_of_nulls_InvoiceNo ,
    round(count(*) filter (where StockCode is null) * 100.0 / count(*) , 2) as per_of_nulls_StockCode , 
    round(count(*) filter (where Description is null) * 100.0 / count(*) , 2) as per_of_nulls_Description ,
    round(count(*) filter (where Quantity is null) * 100.0 / count(*) , 2) as per_of_nulls_Quantity ,
    round(count(*) filter (where InvoiceDate is null) * 100.0 / count(*) , 2) as per_of_nulls_InvoiceDate ,
    round(count(*) filter (where UnitPrice is null) * 100.0 / count(*) , 2) as per_of_nulls_UnitPrice ,
    round(count(*) filter (where CustomerID is null) * 100.0 / count(*) , 2) as per_of_nulls_CustomerID ,
    round(count(*) filter (where Country is null) * 100.0 / count(*) , 2) as per_of_nulls_Country ,
    round(count(*) filter (where InvoiceNo ~ '[a-zA-Z]') * 100.0 / count(*) , 2) as per_of_str_InvoicNo ,
    round(count(*) filter (where StockCode != trim(StockCode)) * 100.0 / count(*) , 2) as per_white_spaces_StackCode ,
    round(count(*) filter (where Description != trim(Description)) * 100.0 / count(*) , 2) as per_white_spaces_Description ,
    round(count(*) filter (where try_cast(Quantity as int) <= 0) * 100.0 / count(*) , 2) as per_Quantity_less_then_0 ,
    round(count(*) filter (where try_cast(UnitPrice as float) <= 0) * 100.0 / count(*) , 2) as per_UnitPrice_less_then_0 ,  
    round(count(*) filter (where Country != trim(Country)) * 100.0 / count(*) , 2) as per_white_spaces_Country 
from raw_data
"""
pl.Config.set_tbl_rows(-1)
results = duckdb.query(detecting_query).pl()
print(results.transpose(include_header=True, header_name="metric", column_names=["value"]))