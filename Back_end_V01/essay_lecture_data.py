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
from telegram.ext import Updater, CommandHandler

os.system('cls')

item_id = "XAUUSD"
path_csv_ticker = "./Datas/Ticker/"
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
		ut_time = self.ut
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
		global path_csv_ticker

		
		# df = pd.read_csv(f'{path_csv_ticker}Live_Tick_{self.name}.csv')#,index_col="time",parse_dates=True).copy()
		df = pd.read_sql(f'Live_Tick_{self.name}', engine).copy()
		df["time"] = pd.to_datetime(df.time, errors='coerce')
		df["ask"] = pd.to_numeric(df.ask, errors='coerce')
		df["bid"] = pd.to_numeric(df.bid, errors='coerce')
		df["med"] = pd.to_numeric(df.med, errors='coerce')
		df = df.set_index(['time'])
		# print(df.tail(2))
		# df.drop(columns=["Unnamed: 0"], inplace =True,axis=1)
		df = df.med.resample(f'{ut}T').ohlc()
		# Calculate Returns and append to the df DataFrame
		# df.ta.log_return(cumulative=True, append=True)
		# df.ta.percent_return(cumulative=True, append=True)
		Zone = {"Buy"}
		List_windows = [14]
		# for i in List_windows:
		# 	df[f'RSI_{i}'] = ta.momentum.rsi(close= df.close, window=i, fillna=False)
		# 	# rsi = df[f'RSI_{i}'] 
		# 	df[f"Moving_Signal"]=df[f'RSI_{i}'].rolling(window=2).mean()
		# 	df[f"Moving_Price"]=df[f'RSI_{i}'].rolling(window=7).mean()

		# 	# df['Zone_Sell'] = (df[f"Moving_Signal"] < df[f"Moving_Price"]) > 80
			
		# 	# df['Zone_Buy'] = (df[f"Moving_Signal"] > df[f"Moving_Price"]) < 20
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
		df["Scale_price"] = np.array(df.close)/10**np.floor(np.log10(df.close))
		df["S&R"] = df.Scale_price%1
		df["Signal_SR"] = 1*(df["S&R"] <sr_buy) - 1*(df["S&R"] > sr_sell)
		df['signal_buy'] = df.apply(self.signal_buy, axis=1)
		df['signal_sell'] = df.apply(self.signal_sell, axis=1)

		df["relat_RSI_13"] = ta.momentum.rsi(close=df["Relat_close"], window=13, fillna=False)
		df["Relat_Moving_Signal"]=df.Relat_close.rolling(window=10).mean()
		df["Relat_Moving_Price"]=df.Relat_close.rolling(window=100).mean()

		df["Change"] = df.close.pct_change()
		df['aadi_pct_change'] = df.apply(self.aadi_pct_change, axis=1)
		df['Tradable'] = df.apply(self.Tradable,axis=1)
		df.dropna(inplace=True)
		# print(df["Tradable"][-1])

		time_now = datetime.now()

		if df['Tradable'][-1] == 1:
			print("-"*30,f"\nBUY ZONE For Ut {ut} M")
			MESSAGE = f"symbol : {self.name} ,\n Type : Zone Buy\n time = {time_now}\n Price : {df.close[-1]}\n\t FOR TimeFrame : {ut} Min"
			r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}')
			print(r.status_code)
			self.plot_show(df,ut,self.name)

		elif df['Tradable'][-1] == -1:
			print("-"*30,f"\nSELL ZONE For Ut {self.ut} M")
			print("-"*30,f"\nBUY ZONE For Ut {self.ut} M")
			MESSAGE = f"symbol : {self.name} ,\n Type : Zone Sell\n time = {time_now}\n Price : {df.close[-1]}\n\t FOR TimeFrame : {self.ut} Min"
			r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}')
			print(r.status_code)
			self.plot_show(df,self.ut,self.name)
		else:
			pass
			# pass
			# print("-"*30,f"\nNeutre For Ut {ut} M")
		# print(df.columns)
		return df

	def __init__(self,name,ut):
		"""  
			Fonction Activation de la Classe:
			boucle permanante entre les differente ut

		"""
		self.name = name
		self.ut = ut
		# print("-"*120,f"\nTicker : {self.name}")
		Count = 0
		# while Count < 10:
		# print(f"{self.name} : {i} M")
		# data = self.get_ohlc(self.name,self.ut)
		thread = threading.Thread(target=self.get_ohlc, args=(self.name,self.ut))
		thread.start()
			# thread.join()
		# print()
		# print(data.tail(1))
		# time.sleep(int(ut)*60)
		Count +=1




count = 0
while True:
	os.system('cls')
	print("|"*10,f"Boucle N°:{count}", "|"*10)
	Tickers = tqdm(ALL,desc="Traitement Donné")
	ut_list = [1,3,5,15,30,60]
	ut_time = tqdm(ut_list,desc="TimeFrame")
	for j in Tickers:
		try:
			for i in ut_time:
				try:
					ut_time.set_postfix({'UT': i})
					Tickers.set_postfix({'Ticker': j})
					# data = Data_Ticker(j,i)
					thread = threading.Thread(target=Data_Ticker, args=(j,i))
					thread.start()
					
				except Exception as e:
					print("Error")
					pass
			
		except Exception as e:
			pass

		# print(data)
	count +=1
	time.sleep(1)

# help(data)
# print(help(ta.ALL_PATTERNS))
# f = inspect.abstract
