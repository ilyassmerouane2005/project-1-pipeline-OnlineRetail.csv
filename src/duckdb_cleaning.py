import duckdb 
import polars as pl
import pytest
path = 'data/raw/OnlineRetail.csv'
cleaning_query = f"""
with raw_data as (
    select * from read_csv('{path}' , encoding = 'latin1' , header = True , all_varchar = True)
)
select distinct 
    try_cast(InvoiceNo as int) as InvoiceNo ,
    lower(trim(StockCode)) as StockCode ,
    lower(trim(Description)) as Description ,
    try_cast(Quantity as int) as Quantity ,
    try_strptime(InvoiceDate , '%m/%d/%Y %H:%M') as InvoiceDate ,
    try_cast(UnitPrice as float) as UnitPrice ,
    lower(trim(Country)) as Country ,
    case when CustomerID is null then 'No' 
         else 'yes'
    end as IsRegistered
from raw_data 
where (InvoiceNo !~ '[a-zA-Z]') and (Description is not null) and (try_cast(Quantity as int) > 0) and (try_cast(UnitPrice as float) > 0) 
"""
cleaning_results = duckdb.query(cleaning_query)
print(cleaning_results)