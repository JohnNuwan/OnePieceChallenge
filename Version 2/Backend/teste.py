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

from Lib.liste_data_trade import Forex

os.system('cls')

host = "localhost"
port = "8091"
url = f"http://{host}:{port}/"


# r = requests.get(url)
# print("-"*30)
# print(r)

# r = requests.get(url+"account_info")
# print(r.status_code)
# print(r)
# # print(r.text)

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
				print('-'*30)
				print(f"{j}||{i}")
				# r = requests.get(url+f"symbol_info/{j}")
				# data = json.loads(r.text)
				# print(pd.DataFrame(data))
				r = requests.get(url+f"ticker_live/{j}")
				# thread = threading.Thread(target=r, args=(j,i))
				print(r.status_code)
				data = json.loads(r.text)
				print(pd.DataFrame(data))
				print()
	# time.sleep(0.5)
# print(type(data))


