
# """
# Descriton FastAPi
# connection DB

# Route :
# 	user
# 	data

# """


# from fastapi import FastAPI
# import MetaTrader5 as mt5
# import pandas as pd

# app = FastAPI()

# @app.get("/")
# async def root():
# 	""" Route de Test """
# 	return {"message": "Hello World"}

# @app.get("/usr")
# async def usr():
# 	""" Route de Test """
# 	return {"message": "user"}

# @app.get("/account_info")
# async def account_info():
# 	""" Route de Recup Info Terminal """
# 	mt5.initialize()
# 	account_info=mt5.account_info()
# 	if account_info!=None:
# 		# display trading account data 'as is'
# 		print(account_info)
# 		# display trading account data in the form of a dictionary
# 		print("Show account_info()._asdict():")
# 		account_info_dict = mt5.account_info()._asdict()
# 		for prop in account_info_dict:
# 			print("  {}={}".format(prop, account_info_dict[prop]))
# 		print()
 
# 		# convert the dictionary into DataFrame and print
# 		df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
# 		print("account_info() as dataframe:")
# 		print(df)
# 		data = df.to_json()
# 	else:
# 		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
	 
# 	# shut down connection to the MetaTrader 5 terminal
# 	mt5.shutdown()
# 	return {"message": data}


# @app.get("/ticker/{item_id}")
# async def read_item(item_id):
# 	import numpy as np
# 	from datetime import datetime
# 	# establish connection to the MetaTrader 5 terminal
# 	mt5.initialize()
	 
# 	# attempt to enable the display of the GBPUSD in MarketWatch
# 	selected=mt5.symbol_select(item_id,True)
# 	# if not selected:
# 	# 	mt5.shutdown()
# 	# 	quit()
# 	# 	return(f"Failed to select {item_id}")
	 
# 	# # display the last GBPUSD tick
# 	# lasttick=mt5.symbol_info_tick(item_id)
# 	symbol_info_tick_dict = mt5.symbol_info_tick(item_id)._asdict()
# 	# shut down connection to the MetaTrader 5 terminal
# 	mt5.shutdown()
# 	data = {item_id:symbol_info_tick_dict}#pd.DataFrame(symbol_info_tick_dict)
# 	data2 = pd.DataFrame.from_dict(data)#type(data)#pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)
# 	data_3 = pd.DataFrame(data2).T
# 	time_now = datetime.now()
# 	data_3["time"] = time_now
# 	data_3['med'] = (np.array(data_3['ask'])+np.array(data_3['bid']))/2
# 	data_3.drop(columns=['flags','last','time_msc','volume','volume_real'],inplace=True)
# 	print(data_3)
# 	# sys.exit()
# 	data = data_3.to_json()

# 	return {"item_id": data}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
# 	return {"item_id": item_id}
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
