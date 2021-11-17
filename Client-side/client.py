
import os
import requests 
import time 
from rich import print
import pandas as pd
import json

os.system('cls')

host = "192.168.1.192"
port = "8091"
url = f"http://{host}:{port}"

print("url")
ticker = "XAUUSD"

db = []
count = 0  

r = requests.get(url)
print("-"*30)
print(r)

r = requests.get(url+f"/ticker_live/{ticker}")
data = json.loads(r.text)
print(type(data))

r = requests.get(url+f"/symbol_info/{ticker}")
data = json.loads(r.text)
print(type(data))

r = requests.get(url+f"/all_symbol")
data = json.loads(r.text)
print(type(data))
df = pd.DataFrame(data)
for i in df['Name']:
	r = requests.get(url+f"/ticker_live/{i}")
	print(r.status_code)
	data = json.loads(r.text)
	print(data)
	db.append(data)


count+=1
print("\n\n LECTURE STOCKAGE DB RAM TEMPO 5s : \n\t")
time.sleep(5)
print(db)

# print(pd.DataFrame(data))