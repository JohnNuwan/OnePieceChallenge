
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

os.system("cls")
app = FastAPI()

@app.get("/")
async def root():
	""" Route de Test """
	return {"message": "Hello World"}

@app.get("/usr")
async def usr():
	""" Route de Test """
	return {"message": "user"}

@app.get("/account_info")
async def account_info():
	""" Route de Recup Info Terminal """
	mt5.initialize()
	account_info=mt5.account_info()
	if account_info!=None:
		# display trading account data 'as is'
		print(account_info)
		# display trading account data in the form of a dictionary
		print("Show account_info()._asdict():")
		account_info_dict = mt5.account_info()._asdict()
		for prop in account_info_dict:
			print("  {}={}".format(prop, account_info_dict[prop]))
		print()
 
		# convert the dictionary into DataFrame and print
		df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
		print("account_info() as dataframe:")
		print(df.head())
		data = df#.to_json()
	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
	 
	# shut down connection to the MetaTrader 5 terminal
	mt5.shutdown()
	return {'message':data.values}


@app.get("/ticker/{ticker_id}")
async def read_item(ticker_id):
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
	print("-"*120)
	print(data_3)
	print("-"*120)
	# sys.exit()
	data = data_3#.to_json()
	return {"ticker_id": data}

@app.get("/items/{item_id }")
async def read_item(item_id ):
	return {"ticker_id": ticker_id}

if __name__ == '__main__':
	uvicorn.run("main:app")