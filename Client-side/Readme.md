		       _ ______ ________      ________  _____ 
		      | |  ____|  ____\ \    / /  ____|/ ____|
		      | | |__  | |__   \ \  / /| |__  | (___  
		  _   | |  __| |  __|   \ \/ / |  __|  \___ \ 
		 | |__| | |____| |____   \  /  | |____ ____) |
		  \____/|______|______|   \/   |______|_____/ 
		                                              
________________________________________________________________________________________________
________________________________________________________________________________________________

Description : 
-------------

Connection A Fast Api pour Traitement des Donner


Codeur   : K.Azazel   |

Language : Python3    |

Date     : 16/11/2021 |
________________________________________________________________________________________________
________________________________________________________________________________________________

## Fichier client:

Simple fichier de teste pour voir et testé les connection au Fastapi
petit stockage memoire interne 

prochain essai est de coupler les le module pydantic pour interagire avec les database 

#### le code sera de forme 
	
	from typing import Optional

	from fastapi import FastAPI
	from pydantic import BaseModel


	class Item(BaseModel):
	    name: str
	    description: Optional[str] = None
	    price: float
	    tax: Optional[float] = None


	app = FastAPI()


	@app.post("/items/")
	async def create_item(item: Item):
	    return item


# Save Data
Dans un premier Temps Recuperation des Ticks et Stockage dans la Base de Donner

# Resample Data

resample data en OHLC et Par TimeFrame 
Nous traiton les donné sur Fastapi et on upload direct dans la DB
le Fichier utiliser pour le moment est:

	Teste_connect.py


# Analyse Data
resample data en OHLC et Par TimeFrame 
Nous traiton les donné dans le Script et on upload direct dans la DB
le Fichier utiliser pour le moment est:

	Teste_Resample_Data.py

# Save Data & Signal

