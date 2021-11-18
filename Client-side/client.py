
import os
import requests 
import time 
from rich import print
import pandas as pd
import json

os.system('cls')

host = "88.120.219.170"
port = "8091"
url = f"http://{host}:{port}"

print(url)
ticker = "XAUUSD"
ut_time = "1"

db = []
count = 0  

r = requests.get(url)
print("-"*30)
print(r)


r = requests.get(url+f"/account_info")
data = json.loads(r.text)
print(type(data))
print(pd.DataFrame(data))


r = requests.get(url+f"/ohlc/{ticker}/{ut_time}")
print(r)
data = json.loads(r.text)
# print(type(data))
# print(r.text)
print(pd.DataFrame(data))

# r = requests.get(url+f"/ticker_live/{ticker}")
# data = json.loads(r.text)
# print(type(data))

# r = requests.get(url+f"/symbol_info/{ticker}")
# data = json.loads(r.text)
# print(type(data))

# while count <1000:
# 	r = requests.get(url+f"/all_symbol")
# 	data = json.loads(r.text)
# 	print(type(data))
# 	df = pd.DataFrame(data)
# 	for i in df['Name']:
# 		r = requests.get(url+f"/ticker_live/{i}")
# 		print(r.status_code)
# 		# data = json.loads(r.text)
# 		# print(data)
# 		db.append(data)


# 	count+=1
# 	# print("\n\n LECTURE STOCKAGE DB RAM TEMPO 5s : \n\t")
# 	# time.sleep(0.1)
# 	# print(db)

# 	# print(pd.DataFrame(data))