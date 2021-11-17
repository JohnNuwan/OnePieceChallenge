
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

count = 0  
while count < 10:
	r = requests.get(url)
	print("-"*30)
	print(r)
	r = requests.get(url+"/usr")
	print("-"*30)
	print(r.text)
	print()
	r = requests.get(url+f"/ticker_live/{ticker}")
	data = json.loads(r.text)
	print("Data Mode Json :")
	print(data)
	print("-"*30)
	print("Data Mode DataFrame : ")
	df = pd.DataFrame(data)
	print(pd.Series(df.T['time']).iloc[0])
	print(df)
	print()
	count+=1
	time.sleep(0.5)