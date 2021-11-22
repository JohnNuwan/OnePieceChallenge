
import pandas as pd 
from config import *

name = "XAUUSD"
timeframe = ["1","3","5","60","240","1440"]

for i in timeframe:
	try:
		data = pd.read_sql(f'OHLC_AADI_{name}_{i}_Min',engine)#, if_exists='append', index=False)
		print(f"Donner pour ut : {i}\n {data.tail(2)}")
		
	except Exception as e:
		# raise e
		pass
