import numpy as np
import MetaTrader5 as mt5
from datetime import datetime
import pytz 
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression
import pandas as pd 
from termcolor import colored, cprint

def dl_data(symbole, timeframe, path):
	extend = '.csv'
	# set time zone to UTC
	timezone = pytz.timezone("Etc/UTC")
	# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
	utc_from = datetime(2021, 4, 4, tzinfo=timezone)
	utc_to = datetime.now()
	timeframe_1 = mt5.TIMEFRAME_M1
	rates = mt5.copy_rates_range(symbole, timeframe, utc_from, utc_to )

	rates_frame = pd.DataFrame(rates)
	# convert time in seconds into the 'datetime' format
	rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

	# display data
	cprint("-"*30,"red")
	cprint(f"Display dataframe {symbole} with data : ", 'magenta', 'on_white')
	cprint("-"*30,"red")
	print(rates_frame.tail(1))
	rates_frame.to_csv(path+symbole+extend)



def Direction(df):
	"""
	Rrtourn bool direction du marcher / Up down
	"""
	# Price Up
	if np.array(df.Close) > np.array(df.Open):
		return 1
	# Price Down
	if np.array(df.Close) < np.array(df.Open):
		return -1
	# Neutre
	else:
		return 0

def open_trade_buy(action, symbol, lot, sl_points, tp_points, deviation, comment):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    mt5.initialize()
    symbol_info = get_info(symbol)
    ea_magic_number = 9986989
    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    point = mt5.symbol_info(symbol).point

    buy_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        # "sl": price - sl_points * point,
        # "tp": price + tp_points * point,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(buy_request)
    mt5.shutdown()        
    return result, buy_request 

def open_trade_sell(action, symbol, lot, sl_points, tp_points, deviation,comment):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    mt5.initialize()
    symbol_info = get_info(symbol)
    ea_magic_number = 9986989
    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    point = mt5.symbol_info(symbol).point

    buy_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        # "sl": price + sl_points * point,
        # "tp": price - tp_points * point,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(buy_request)
    mt5.shutdown()        
    return result, buy_request 
def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info

def rsi_signal(df):
	if df.RSI_2 < 32 and df.RSI_7 < 32 :
		return 1
	if df.RSI_2 > 68 and df.RSI_7 > 68 :
		return -1
	else:
		return 0

def cci_signal(df):
	if df.cci_14 < 200 and df.cci_50 < 200 :
		return 1
	if df.cci_14 > -200 and df.cci_50 > -200 :
		return -1
	else:
		return 0


def changeslpl(ticket,pair,pos_type,SL,ea_magic_number):
	request = {
		"action": mt5.TRADE_ACTION_SLTP,
		"symbol": pair,
		"type": pos_type,
		"position": ticket,
		"sl": SL,
		"deviation": 20,
		"magic": ea_magic_number,
		"comment": "python Split",
		"type_time": mt5.ORDER_TIME_GTC,
		"type_filling": mt5.ORDER_FILLING_FOK,
		"ENUM_ORDER_STATE": mt5.ORDER_FILLING_IOC,
	}

	#// perform the check and display the result 'as is'
	result = mt5.order_send(request)

	if result.retcode != mt5.TRADE_RETCODE_DONE:
		print("4. order_send failed, retcode={}".format(result.retcode))

		print(" result",result)

def dif_price(df):
	mt5.initialize()
	if df.type == 0:
		point_dif =  df.price_current - df.price_open 
		point_dif = point_dif * 1000
		print("buy dif",point_dif)
		sl_new = df.price_open+ 0.0003
		print(df.price_open)
		print(sl_new)
		#sys.exit()
		if point_dif >= 2.5:
			try:
				changeslpl(ticket=df.ticket, pair= df.symbol ,pos_type= df.type ,SL = sl_new  ,ea_magic_number=df.magic)
				
			except Exception as e:
				raise e

	if df.type == 1:
		point_dif = df.price_open - df.price_current 
		print("Sell dif",point_dif)
		sl_new = df.price_open - 0.0003
		print(df.price_open)
		print(sl_new)
		if point_dif >= 2.5:
			try:
				changeslpl(ticket=df.ticket, pair= df.symbol ,pos_type= df.type ,SL = sl_new  ,ea_magic_number=df.magic)
				
			except Exception as e:
				raise e

def close_trade(action, buy_request, result, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
    symbol = buy_request['symbol']
    if action == 0:
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(df.symbol).ask
    elif action == 1 :
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(df.symbol).bid
    position_id=result.order
    lot = buy_request['volume']

    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": df.symbol,
        "volume": df.volume,
        "type": trade_type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "Split Python Script",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a close request
    result=mt5.order_send(close_request)

def changeslpl(ticket,pair,pos_type,SL,ea_magic_number):
	request = {
		"action": mt5.TRADE_ACTION_SLTP,
		"symbol": pair,
		"type": pos_type,
		"position": ticket,
		"sl": SL,
		"deviation": 20,
		"magic": ea_magic_number,
		"comment": "python script open",
		"type_time": mt5.ORDER_TIME_GTC,
		"type_filling": mt5.ORDER_FILLING_FOK,
		"ENUM_ORDER_STATE": mt5.ORDER_FILLING_IOC,
	}

	#// perform the check and display the result 'as is'
	result = mt5.order_send(request)

	if result.retcode != mt5.TRADE_RETCODE_DONE:
		print("4. order_send failed, retcode={}".format(result.retcode))

		print(" result",result)

def dif_price(df):
	mt5.initialize()
	if df.type == 0:
		point_dif =  df.price_current - df.price_open 
		point_dif = point_dif * 1000
		print("buy dif",point_dif)
		sl_new = df.price_open+ 0.00015
		print(df.price_open)
		print(sl_new)
		#sys.exit()
		if point_dif >= 1:
			try:
				changeslpl(ticket=df.ticket, pair= df.symbol ,pos_type= df.type ,SL = sl_new  ,ea_magic_number=df.magic)
				
			except Exception as e:
				raise e

	if df.type == 1:
		point_dif = df.price_open - df.price_current 
		print("Sell dif",point_dif)
		sl_new = df.price_open - 0.00015
		print(df.price_open)
		print(sl_new)
		if point_dif >= 1:
			try:
				changeslpl(ticket=df.ticket, pair= df.symbol ,pos_type= df.type ,SL = sl_new  ,ea_magic_number=df.magic)
				
			except Exception as e:
				raise e

def close_trade(action, buy_request, result, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
    symbol = buy_request['symbol']
    if action == 0:
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(df.symbol).ask
    elif action == 1 :
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(df.symbol).bid
    position_id=result.order
    lot = buy_request['volume']

    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": df.symbol,
        "volume": df.volume/2,
        "type": trade_type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "Split Python Script",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a close request
    result=mt5.order_send(close_request)

def pythag(pt1, pt2):
    a_sq = (pt2[0] - pt1[0]) ** 2
    b_sq = (pt2[1] - pt1[1]) ** 2
    return sqrt(a_sq + b_sq)

def regression_ceof(pts):
    X = np.array([pt[0] for pt in pts]).reshape(-1, 1)
    y = np.array([pt[1] for pt in pts])
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0], model.intercept_

def local_min_max(pts):
    local_min = []
    local_max = []
    prev_pts = [(0, pts[0]), (1, pts[1])]
    for i in range(1, len(pts) - 1):
        append_to = ''
        if pts[i-1] > pts[i] < pts[i+1]:
            append_to = 'min'
        elif pts[i-1] < pts[i] > pts[i+1]:
            append_to = 'max'
        if append_to:
            if local_min or local_max:
                prev_distance = pythag(prev_pts[0], prev_pts[1]) * 0.5
                curr_distance = pythag(prev_pts[1], (i, pts[i]))
                if curr_distance >= prev_distance:
                    prev_pts[0] = prev_pts[1]
                    prev_pts[1] = (i, pts[i])
                    if append_to == 'min':
                        local_min.append((i, pts[i]))
                    else:
                        local_max.append((i, pts[i]))
            else:
                prev_pts[0] = prev_pts[1]
                prev_pts[1] = (i, pts[i])
                if append_to == 'min':
                    local_min.append((i, pts[i]))
                else:
                    local_max.append((i, pts[i]))
    return local_min, local_max
