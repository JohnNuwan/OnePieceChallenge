import os
import sys
import requests 
import time 
from rich import print
import pandas as pd
import json
from tqdm import tqdm
# from tqdm.rich import trange, tqdm_rich
import queue as Queue
import threading
import MetaTrader5 as mt5

from datetime import datetime
from Lib.Trading_Function import *
from Lib.liste_data_trade import Forex
from Class_ticker import * 
os.system('cls')

host = "localhost"
port = "8091"
url = f"http://{host}:{port}/"

lot = 0.01
deviation = 20
comment = "python M15"

r = requests.get(url+f"all_symbol")
print(r.status_code)
print(r)
# print(r.text)

def get_data_trade(name,ut):
	print(f"{name}||{ut}")
	Ticker =  Data_Ticker(name)
	data = Ticker.get_ohlc(name,ut)
	return data

# symbole = "EURUSD"
r = requests.get(url+f"all_symbol")
print(r.status_code)
print(r)
# print(r.text)

data = json.loads(r.text)
df = pd.DataFrame(data)

while True:
	for i in df['Name']:
		for j in Forex:
			if j == i:
				ut = 15
				data = get_data_trade(j,ut)
				print(data)
				time_now = datetime.now()

				if data["Tradable"][-1] == 1:
					print('Buy ')
					# data = get_data_trade(j,1)
					# if data["Tradable"][-1] == 1:
					MESSAGE = f"symbol : {j} ,\n Type : Buy\n time = {time_now}\n Price : {data['close'][-1]} \n UT : {ut} Minute"
					r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}')
					print(r.status_code)
					print(MESSAGE)
					open_trade_buy(action="buy", symbol=j, lot=lot, sl_points="2500", tp_points="90000", deviation=deviation ,comment=comment)
					# count_buy += 1
					print(colored("Buy Detect","green"))
					# else:
					# 	print("Nothing")


				elif data["Tradable"][-1] == -1:
					print('SELL ')
					# data = get_data_trade(j,1)
					# if data["Tradable"][-1] == -1:
					open_trade_sell(action="sell", symbol=j, lot=lot, sl_points="2500", tp_points="90000", deviation=deviation ,comment=comment)
					MESSAGE = f"symbol : {j} ,\n Type : Sell\n time = {time_now}\n Price : {data['close'][-1]}  \n UT : {ut} Minute"
					r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}')
					print(r.status_code)
					print(MESSAGE)
					# count_sell += 1
					print("Sell Detect")

					# else:
					# 	print("Nothing")


				elif data["Tradable"][-1] == 0:
					print(f'Nothing For : {j}')
					print(data.tail(2))

				else:
					print("-")
	

	time.sleep(900)

