import pandas as pd 

import os 

item_id = "XAUUSD"
path_csv_ticker = "./Datas/Ticker/"
df = pd.read_csv(f'{path_csv_ticker}Live_Tick_{item_id}.csv',index_col="time",parse_dates=True).copy()
df.dropna(inplace=True)
print(df)