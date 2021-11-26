import pandas as pd 
import numpy as np
import os
import time 
from rich import print
from tqdm import tqdm
import ta
from config import *
from datetime import datetime
import requests
from Lib.liste_data_trade import *
import threading
import json

Overbought = 70
OverSold = 30

sr_buy = 0.3
sr_sell = 0.7
fee = 0.0005


TOKEN = "1801058128:AAETqJbJMjVUt6ewpjYL2ZVIU8wzIlrzJL4"
CHAT_ID = "@GOLD_SIGNAL_TESTE"

class Data_Ticker:

	def get_name(self):
		"""
			Return Name Ticker
		"""
		return self.name
	def relative(self,df):
		rel = df.pct_change()
		cumret = (1+ rel).cumprod()-1
		cumret = cumret.fillna(0)
		return cumret

	# SIgnal AADI
	def signal_buy(self ,df):
		if ((df.Moving_Price  < OverSold ) and (df.Moving_Signal < OverSold )) and ((df.Moving_Signal > df.Moving_Price)) :
			return True

		else:
			return False
		
	def signal_sell(self,df):
		if ((df.Moving_Price > Overbought) and (df.Moving_Signal > Overbought )) and ((df.Moving_Signal < df.Moving_Price)) :
			return True

		else:
			return False

	def aadi_pct_change(self,df):
		if (df.signal_buy == True) and (df.Change < float(0.002)):
			return 1

		elif (df.signal_sell == True) and (df.Change < float(-0.004)):
			return -1
		else:
			return 0


	def Tradable(self,df):
		if (df.Signal_SR == -1) and (df.signal_sell == True) and (df.aadi_pct_change == -1) :
			return -1
		elif (df.Signal_SR == 1) and (df.signal_buy == True) and (df.aadi_pct_change == 1) :
			return 1
		else:
			return 0

	def message(self,msg):
		# if a DISCORD URL is set in the config file, we will post to the discord webhook
		if DISCORD_WEBHOOK_URL:
			chat_message = {
				"username": "AADI Alert",
				"avatar_url": "https://i.imgur.com/F1UMx9K.jpeg",
				"content": f"------------------\n{msg}"
			}

			requests.post(DISCORD_WEBHOOK_URL, json=chat_message)


	def plot_show(self,df,ut_time,name):

		symbol = self.name
		# ut_time = self.ut
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
		fig, (ax0, ax1,ax2,ax3,ax4) = plt.subplots(5, 1, sharex=False)
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
		ax2.axhline(y = OverSold, color ="green", linestyle ="--")
		ax2.axhline(y = 50, color ="grey", linestyle ="--")
		ax2.axhline(y = Overbought, color ="red", linestyle ="--")
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
	def get_ohlc(self,name,ut):
		"""
			Return Les Données Ticks en Données OHLC /UT
		"""
		# host = "88.120.219.170"
		# port = "8091"
		# url = f"http://{host}:{port}/"
		# r = requests.get(url+f"read_tick/{self.name}/{ut}")
		# print("-"*30)
		# data = json.loads(r.text)
		# df = pd.DataFrame(data)
		# print("DF sans OHL",df.tail(2))
		df = pd.read_sql(f'Live_Tick_{self.name}', engine).copy()#,index_col=['time']).copy()
		# print(df.tail(2))
		df["time"] = pd.to_datetime(df.time, errors='coerce')
		df = df.set_index(['time'])
		
		df = df.med.resample(f'{ut}T').ohlc()
		df["open"] = pd.to_numeric(df.open, errors='coerce')
		df["high"] = pd.to_numeric(df.high, errors='coerce')
		df["low"] = pd.to_numeric(df.low, errors='coerce')
		df["close"] = pd.to_numeric(df.close, errors='coerce')
		df['time'] = df.index
		# df = df.med.resample(f'{self.ut}T').ohlc()
	
		df.dropna(axis=0,inplace=True)
		df["RSI_13"] = ta.momentum.rsi(close=df["close"], window=13, fillna=False)
		df[f"Moving_Signal"]=df[f'RSI_13'].rolling(window=2).mean()
		df[f"Moving_Price"]=df[f'RSI_13'].rolling(window=7).mean()
		# print(f"Zone Sell :  {df['Zone_Sell'][-1]} || Zone Buy : {df['Zone_Buy'][-1]}")
		# df.ta.indicators()
		df['%_change']=self.relative(df.close)
		df["Relat_close"] = self.relative(df.close)
		df["Relat_high"] = self.relative(df.high)
		df["Relat_low"] = self.relative(df.low)
		df["Relat_open"] = self.relative(df.open)

		df["relat_RSI_13"] = ta.momentum.rsi(close=df["Relat_close"], window=13, fillna=False)
		df["Relat_Moving_Signal"]=df.Relat_close.rolling(window=21).mean()
		df["Relat_Moving_Price"]=df.Relat_close.rolling(window=50).mean()

		df["Change"] = df.close.pct_change()
		df["Scale_price"] = np.array(df.close)/10**np.floor(np.log10(df.close))
		df["S&R"] = df.Scale_price%1
		df["Signal_SR"] = 1*(df["S&R"] <sr_buy) - 1*(df["S&R"] > sr_sell)
		df['signal_buy'] = df.apply(self.signal_buy, axis=1)
		df['signal_sell'] = df.apply(self.signal_sell, axis=1)
		df['aadi_pct_change'] = df.apply(self.aadi_pct_change, axis=1)
		df['Tradable'] = df.apply(self.Tradable,axis=1)
		# print("Apres Analyse",df.tail(10))

		if df['Tradable'][-1] == 1:
			return df.tail(2)
		elif df['Tradable'][-1] == -1:
			return df.tail(2)

		else:
			return df.tail(1)
			# return f'Nothing For {self.name} || TimeFrame : {self.ut}'
		# df.dropna(axis=0,inplace=True)
		# print(df.tail())
		# return df

	def __init__(self,name):
		"""  
			Fonction Activation de la Classe:
			boucle permanante entre les differente ut

		"""
		self.name = name
		# self.ut = 

		# data = self.get_ohlc(self.name,60)
		# print(type(data))

