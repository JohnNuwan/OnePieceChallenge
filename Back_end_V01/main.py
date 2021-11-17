
"""
Descriton FastAPi
connection DB

Route :
	user
	data

"""

import os
from fastapi import FastAPI
import MetaTrader5 as mt5
import pandas as pd
import uvicorn
import json
port = 8091
host = "0.0.0.0"

os.system("cls")
app = FastAPI()

db = []
live_tick = []
@app.get("/")
async def root():
	""" Route de Test """
	return {"message": "Hello World"}

@app.get("/usr")
async def usr():
	""" Route de Test """
	return {"message": "user"}

# Route Recuperation Info Compte Courant
@app.get("/account_info")
async def account_info():
	""" Route de Recup Info Terminal """
	mt5.initialize()
	account_info=mt5.account_info()
	if account_info!=None:

		account_info_dict = mt5.account_info()._asdict()

 
		# convert the dictionary into DataFrame and print
		df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
		# print("account_info() as dataframe:")
		# print(df.head())
		data = df#.to_json()
		db.append({'account_info':data.values})
		print(db)
	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
	 
	# shut down connection to the MetaTrader 5 terminal
	mt5.shutdown()
	return {'account_info':data.values}

# Route Recuperation Live Tick
@app.get("/ticker_live/{ticker_id}")
async def read_live(ticker_id):
	import numpy as np
	from datetime import datetime
	# establish connection to the MetaTrader 5 terminal
	mt5.initialize()
	 
	# attempt to enable the display of the GBPUSD in MarketWatch
	selected=mt5.symbol_select(ticker_id,True)	# # display the last GBPUSD tick
	# lasttick=mt5.symbol_info_tick(ticker_id)
	symbol_info_tick_dict = mt5.symbol_info_tick(ticker_id)._asdict()
	# shut down connection to the MetaTrader 5 terminal
	mt5.shutdown()
	data = {ticker_id:symbol_info_tick_dict}#pd.DataFrame(symbol_info_tick_dict)
	data2 = pd.DataFrame.from_dict(data)#type(data)#pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)
	data_3 = pd.DataFrame(data2).T
	time_now = datetime.now()
	data_3['med'] = (np.array(data_3['ask'])+np.array(data_3['bid']))/2
	data_3["time"] = time_now
	data_3.drop(columns=['flags','last','time_msc','volume','volume_real'],inplace=True)
	# print("-"*120)
	# print(data_3.T)
	# print("-"*120)
	# sys.exit()
	data = data_3.T
	db.append(data)
	return {"ticker_id": [data]}




# Route Recuperation hist Data
@app.get("/hist_ticker/{ticker}/{timeframe}")
async def read_hist(ticker_id,timeframe ):
	print(ticker_id,timeframe)
	return {"ticker_id": [ticker_id.values,timeframe.values]}

@app.get("/listtick")
async def read_item():
	data = pd.DataFrame(db)
	return data


@app.get("/symbol_info/{item_id}")
async def read_item(item_id ):
	"""  Recuperation Des infos Data  """
	# establish connection to the MetaTrader 5 terminal
	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()
	# display symbol properties
	symbol_info=mt5.symbol_info(item_id)
	if symbol_info!=None:
		symbol_info_dict = mt5.symbol_info(item_id)._asdict()
	# shut down connection to the MetaTrader 5 terminal
	mt5.shutdown()
	data = pd.Series(symbol_info_dict)

	return {"items_id": data}



@app.get("/all_symbol")
async def get_all_symbol():
		
		# establish connection to the MetaTrader 5 terminal
		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()
		 
		# get all symbols
		symbols=mt5.symbols_get()
		# print('Symbols: ', len(symbols))
		# all_symbol = pd.DataFrame()
		name = []
		for s in symbols:
			name.append(s.name)

		data = pd.DataFrame(name,columns=["Name"])
		# data = data.to_json()
		return data


@app.get("/items/{item_id}")
async def read_item(item_id ):
	return {"items_id": item_id}

if __name__ == '__main__':
	uvicorn.run("main:app",port=port, host=host, debug=True)