import polars as pl 
df = pl.read_csv('data/raw/OnlineRetail.csv' , schema_overrides={'InvoiceNo' : pl.Utf8 , 'StockCode' : pl.Utf8} , encoding= 'latin1')

number_of_duplicates = df.is_duplicated().sum()
print(f'number of duplicates rows is: {number_of_duplicates}')

missing_values = df.select((pl.all().null_count() / pl.len() * 100).round(2))
print(f'missing values percentage: {missing_values}')

InvoiceNo_anomalies = df.select((pl.col('InvoiceNo').str.contains(r'[a-zA-Z]').sum() / pl.len() * 100).round(2))
print(f'Rows with characters in InvoiceNo column percentage: {InvoiceNo_anomalies}')

StockCode_anomalies = df.select(((pl.col('StockCode') != pl.col('StockCode').str.strip_chars()).sum() / pl.len() *100).round(2))
print(f'Rows with white spaces in StockCode column percentage: {StockCode_anomalies}')

Description_anomalies = df.select(((pl.col('Description') != pl.col('Description').str.strip_chars()).sum() / pl.len() *100).round(2))
print(f'Rows with white spaces in Description column percentage: {Description_anomalies}') 

Quantity_anomalies = df.select(((pl.col('Quantity') <= 0).sum() / pl.len() * 100).round(2))
print(f'Perecentage of rows with Quantity <= 0 : {Quantity_anomalies}')

UnitPrice_anomalies = df.select(((pl.col('UnitPrice') <= 0).sum() / pl.len() * 100).round(2))
print(f'Perecentage of rows with UnitPrice <= 0 : {UnitPrice_anomalies}')

Country_anomalies = df.select(((pl.col('Country') != pl.col('Country').str.strip_chars()).sum() / pl.len() *100).round(2))
print(f'Rows with white spaces in Country column percentage: {Country_anomalies}') 