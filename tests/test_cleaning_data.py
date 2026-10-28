import polars as pl 
import pytest
from src.cleaning_data import data_cleaning
def test_clean_data():
    mockdata = pl.DataFrame({
        "InvoiceNo": ["536365", "C536379", "536366" , "536365"] ,
        "StockCode": ["85123a ", "71053", " 84406b" , "85123a "] ,
        "Description": ["DoUbtfull   ", None ,"white hanging heart" , "DoUbtfull   "],
        "Quantity": [6, -1, 10 , 6] ,
        "InvoiceDate": ["12/1/2010 8:26", "12/1/2010 8:34", "12/1/2010 8:34" , "12/1/2010 8:26"] ,
        "UnitPrice": [2.55, 0.00, 4.39 , 2.55] , 
        "CustomerID": [17850.0, 17850.0, None , 17850.0] ,
        "Country": ["united kingdom", "united kingdom", "france" , "united kingdom"] ,
    })
    result = data_cleaning(mockdata)
    assert result.height == 2
    row_registered = result.filter(pl.col('InvoiceNo') == 536365)
    assert row_registered['Description'][0] == 'doubtfull'
    assert row_registered['IsRegistered'][0] == 'yes'
    guest_row = result.filter(pl.col('InvoiceNo') == 536366)
    assert guest_row['IsRegistered'][0] == 'no'