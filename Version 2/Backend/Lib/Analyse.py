# Analyse Live Ticke and Resample in OHLC

import os
import sys
import time
import pandas as pd
import requests 
from rich import print
import json
import numpy as np
import ta
import matplotlib.pyplot as plt
import matplotlib.collections as collections
from config import *
from datetime import datetime
import queue as Queue
import threading
from Lib.liste_data_trade import *
from tqdm import tqdm

import asyncio

Overbought = 70
OverSold = 30

sr_buy = 0.3
sr_sell = 0.7
fee = 0.0005

name = "XAUUSD"
ut_time = ["1","3","5","60","240","1440"]

TOKEN = "1801058128:AAETqJbJMjVUt6ewpjYL2ZVIU8wzIlrzJL4"
CHAT_ID = "@GOLD_SIGNAL_TESTE"


os.system('cls')

host = "88.120.219.170"
port = "8091"
url = f"http://{host}:{port}"


async def plot_show(df,ut_time,name):

	symbol = name
	path = "./images/"
	if not os.path.exists(path):
		os.makedirs(path)
	import matplotlib.pyplot as plt
	import matplotlib.collections as collections

	# df = self.analys_db(self.name)
	plt.style.use('seaborn-dark')#('dark_background')
	loc = "upper left"

	# Reduction DF a 100 data : 
	df = df.tail(50)
	# Creation X subplot a la Figure
	fig, (ax0, ax1,ax2,ax3,ax4) = plt.subplots(5, 1, sharex=True)
	fig.set_size_inches(18.5, 10.5,forward=True)
	fig.suptitle(f'Chart {symbol} {ut_time}M', fontsize=16)
	#Figure 1
	ax0.set_title('Classic Price')
	ax0.plot(df.index, df.close,label="Close")
	ax0.plot(df.index,df.open,label="Open")
	ax0.plot(df.index,df.high,label="High")
	ax0.plot(df.index,df.low,label="Low")
	ax0.fill_between(df.index, df.high, df.low, color='grey', label="Fill Between  | High:Low |")
	ax0.legend(loc=loc)


	# Figure N°2
	ax1.set_title('Relative Price')
	ax1.plot(df.index, df.Relat_close,label="Relative close")
	ax1.plot(df.index,df.Relat_open,label="Relat Open")
	ax1.plot(df.index,df.Relat_high,label="Relat high")
	ax1.plot(df.index,df.Relat_low,label="Relat low")

	ax1.fill_between(df.index, df.Relat_high, df.Relat_low, color='grey',label="Fill Between | High:Low |")
	ax1.legend(loc=loc)
	# Figure N°3
	ax2.set_title('ADAGI Indicateur')
	ax2.plot(df.index, df.RSI_13,label="RSI 13P")
	ax2.plot(df.index, df.Moving_Price, label="Moving_Price")
	ax2.plot(df.index, df.Moving_Signal, label="Moving_Signal")
	ax2.axhline(y = 32, color ="green", linestyle ="--")
	ax2.axhline(y = 50, color ="grey", linestyle ="--")
	ax2.axhline(y = 68, color ="red", linestyle ="--")
	ax2.legend(loc=loc)



	# Figure N°3
	ax3.set_title('Price Signal')
	ax3.plot(df.index, df.Tradable, label="Signal Trade Price")
	ax3.legend(loc=loc)
	# ax3.plot(df['S&R'], marker=11)
	# ax3.plot(df.Signal_SR, color = 'yellow')#,edgecolor = 'red')

	# Figure N°3
	ax4.set_title('ADAGI Signal')
	ax4.plot(df.index, df.aadi_pct_change, label="Signal Trade ADAGI")
	ax4.legend(loc=loc)
	# # Affichage + Legend
	# fig.legend()
	# plt.show()
	plt.savefig(f"{path}Chart_{symbol}_{ut_time}M.png")
	return fig

async def relative(df):
		rel = df.pct_change()
		cumret = (1+ rel).cumprod()-1
		cumret = cumret.fillna(0)
		return cumret


# SIgnal AADI
async def signal_buy(df):
	if ((df.Moving_Price  < OverSold ) and (df.Moving_Signal < OverSold )) and ((df.Moving_Signal > df.Moving_Price)) :
		return True

	else:
		return False
	
async def signal_sell(df):
	if ((df.Moving_Price > Overbought) and (df.Moving_Signal > Overbought )) and ((df.Moving_Signal < df.Moving_Price)) :
		return True

	else:
		return False

async def aadi_pct_change(df):
	if (df.signal_buy == True) and (df.Change < float(0.002)):
		return 1

	elif (df.signal_sell == True) and (df.Change < float(-0.004)):
		return -1
	else:
		return 0


async def Tradable(df):
	if (df.Signal_SR == -1) and (df.signal_sell == True) and (df.aadi_pct_change == -1) :
		return -1
	elif (df.Signal_SR == 1) and (df.signal_buy == True) and (df.aadi_pct_change == 1) :
		return 1
	else:
		return 0

async def message(msg):
	# if a DISCORD URL is set in the config file, we will post to the discord webhook
	if DISCORD_WEBHOOK_URL:
		chat_message = {
			"username": "AADI Alert",
			"avatar_url": "https://i.imgur.com/F1UMx9K.jpeg",
			"content": f"------------------\n{msg}"
		}

		requests.post(DISCORD_WEBHOOK_URL, json=chat_message)


async def resample(name):
	"""  Resample les Donner et Construi les differente Analyse  """
	for i in ut_time:
		print(f"Get Ticker : {name} For TimeFrame : {i}")
		r = requests.get(url+f"/read_tick/{name}/{i}")
		# print(r)
		data = json.loads(r.text)

		# print(name, i)
		# print(type(data))
		df = pd.DataFrame.from_dict(data)
		df['%_change']=relative(df.close)
		df["Relat_close"] = relative(df.close)
		df["Relat_high"] = relative(df.high)
		df["Relat_low"] = relative(df.low)
		df["Relat_open"] = relative(df.open)
		df["RSI_13"] = ta.momentum.rsi(close=df["close"], window=13, fillna=False)
		df["relat_RSI_13"] = ta.momentum.rsi(close=df["Relat_close"], window=13, fillna=False)
		df["Moving_Signal"]=df.RSI_13.rolling(window=2).mean()
		df["Moving_Price"]=df.RSI_13.rolling(window=7).mean()

		df["Relat_Moving_Signal"]=df.Relat_close.rolling(window=10).mean()
		df["Relat_Moving_Price"]=df.Relat_close.rolling(window=100).mean()
		df["Scale_price"] = np.array(df.close)/10**np.floor(np.log10(df.close))
		df["S&R"] = df.Scale_price%1
		df["Signal_SR"] = 1*(df["S&R"] <sr_buy) - 1*(df["S&R"] > sr_sell)
		df['signal_buy'] = df.apply(signal_buy, axis=1)
		df['signal_sell'] = df.apply(signal_sell, axis=1)
		df["Change"] = df.close.pct_change()
		df['aadi_pct_change'] = df.apply(aadi_pct_change, axis=1)
		df['Tradable'] = df.apply(Tradable,axis=1)

		return df