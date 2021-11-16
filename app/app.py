#! usr/bin/env/python3
#-*-Coding:UTF-8-*-
# Author : K.Azazel
#------------------------------------

# import Lib
import os
from flask import Flask, request, render_template, jsonify
import  json, requests
from art import *

import MetaTrader5 as mt5

import pandas as pd

from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

from Lib.Trading_Function import *
from config import *
# Affichage console
codeur = "K.Azazel"
console = Console(width=20)



def message(msg):
	# if a DISCORD URL is set in the config file, we will post to the discord webhook
	if DISCORD_WEBHOOK_URL:
		chat_message = {
			"username": "AADI Alert",
			"avatar_url": "https://i.imgur.com/F1UMx9K.jpeg",
			"content": f"------------------\n{msg}"
		}

		requests.post(DISCORD_WEBHOOK_URL, json=chat_message)

app = Flask(__name__)

host= "0.0.0.0"
port = "80"
debug= True
Art=text2art("Jeeves",chr_ignore=True)

os.system('cls')

def banner(Art):
	""" Simple Decoration d'en-tête """

	print(Text("_"*60, justify="left" ,style="color(9) blink"))
	print(Text(Art, justify="left" ,style="color(2) blink " ))
	print(f"Author : {codeur}")
	print(Text("_"*60, justify="left" ,style="color(9) blink"))
	# # input_lot = input("Entrée Un volume de Lot CFDs: ")
	# Lot = "0.02"#input_lot

	return ""

@app.route('/')
def index():
	""" Route Page Index """
	# port_ext = os.system(f"ngrok.exe http {port}")

	return render_template('index.html')

@app.route('/register')
def register():
	""" Route Page resiter """
	# port_ext = os.system(f"ngrok.exe http {port}")

	return render_template('register.html')

@app.route('/login')
def login():
	""" Route Page Login """
	# port_ext = os.system(f"ngrok.exe http {port}")

	return render_template('login.html')

@app.route('/price')
def price():
	""" Route Page Dashboard """
	return render_template('price.html')

@app.route('/dashbord')
def dashbord():
	""" Route Page Dashboard """
	return render_template('dashboard.html')

@app.route('/webhook',  methods=['POST'])
def webhook():
	""" Route Pour la Comunication TradingView Discord """
	lot = None
	deviation = 20
	comment = None
	webhook_message = json.loads(request.data)
	print(webhook_message)

	df = pd.DataFrame(webhook_message)
	ticker = df.ticker[0]
	Action = df['strategy'].iloc[0]
	
	if ticker == "GOLD" or ticker == "XAUUSD":
		symbol = "XAUUSD"
		lot = 0.16
		comment = "Python AADI M15"
		print(ticker , symbol)		

	if ticker == "US30":
		symbol = "US30.cash"
		lot = 0.16
		comment = "CFD_Intra"

		print(ticker , symbol)
	if ticker == "DE40":
		symbol = "GER30.cash"
		comment = "CFD_Intra"
		lot = 0.16
		print(ticker , symbol)
	else:
		symbol = ticker
		lot = 0.08
		comment = "Python AADI M1"

		print(ticker , symbol)
	print("-"*30)
	print(symbol)
	print(Action)
	print("-"*30)
	# MESSAGE = f"symbol : {symbol},\n{webhook_message} "
	# r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}')
	# print(r.status_code)
	# print(MESSAGE)
	if Action == 'buy':
		print("Buy")
		message(f"BUY , {symbol}")
		# open_trade_buy(action="buy", symbol=symbol, lot=lot, sl_points="2500", tp_points="90000", deviation=deviation ,comment=comment)

	elif Action == 'SELL':
		print("SELL")
		message(f"SELL , {symbol}")
		# open_trade_sell(action="sell", symbol=symbol, lot=lot, sl_points="2500", tp_points="90000", deviation=deviation ,comment=comment)

	else:
		print("Nothing ")

	return webhook_message



if __name__ == '__main__':
	banner(Art)
	print(Text("_"*60, justify="left" ,style="color(156) blink"))
	print("Address Local :\t",Text(f"{host}:{port}/webhook", justify="left" ,style="color(45) " ))
	print(Text("_"*60, justify="left" ,style="color(156) blink"))
	
	app.run(host=host,port=port,debug=debug)