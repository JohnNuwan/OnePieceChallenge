
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

os.system('cls')

host = "88.120.219.170"
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



def make_data(name):
	r = requests.get(url+f"/ticker_live/{name}")
	# print(r.status_code)
	data = json.loads(r.text)
	return data	


threadList = ["Thread-1", "Thread-2", "Thread-3"]

r = requests.get(url+f"/all_symbol")
data = json.loads(r.text)
# print(list(pd.DataFrame(data)['Name']))
# sys.exit()
nameList = [list(pd.DataFrame(data)['Name'])]
# print(nameList)

while True:
	try:
		threads = []
		for i in nameList:
			for j in i :

				thread = threading.Thread(target=make_data, args=(j,))
				threads.append(thread)
				thread.start()
		for thread in threads:  # iterates over the threads
			thread.join()       # waits until the thread has finished work
		
	except Exception as e:
		print(e)

	# count+=1
# while count <10:
# 	r = requests.get(url+f"/all_symbol")
# 	data = json.loads(r.text)
# 	# print(type(data))
# 	df = pd.DataFrame(data)
# 	print("-"*60)
# 	print("\nChargement Live Ticker : \n\t")
# 	bar = tqdm(df['Name'],desc='Bar desc', leave=True)



# 	count+=1
# 	# print("\n\n LECTURE STOCKAGE DB RAM TEMPO 5s : \n\t")
# 	# time.sleep(0)
# 	# print(db)

# 	# print(pd.DataFrame(data))