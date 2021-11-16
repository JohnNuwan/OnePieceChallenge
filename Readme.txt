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
	Back-end De la partie Communication pour la partie Tradingview
	avec envoie au client , ce qui nous permet de garder le code robot de notre côté
	
	Dans un Avenir proche je merge le projet Trading_Python dans Jeeves, avec la base de donné 
	Postgre , Le traitement des données et l'envoie de ces même données au Clients
-----------------------
Codeur   : K.Azazel   |
Language : Python3    |
Date     : 16/11/2021 |
________________________________________________________________________________________________
________________________________________________________________________________________________

INSTALATION:
-----------
	* Ouvrire un terminal 
	
	* Faire un Environnement Virtuel :
	-------------------------------
		pip venv env

	* Installation des dependance:
	----------------------------
		pip install requirement.txt


________________________________________________________________________________________________
________________________________________________________________________________________________

DASHBOARD:
----------
	* Dans un premier temps construire les different systeme docker 



un docker pour la party database :
----------------------------------
	* Pour la Database , J'ai pu faire les des Script Back end pour recupéré les diferents Ticker Du marcher
	
	* Nous avont donc plusieur code :
	-------------------------------
		un code en script pure 
		un code en Programmation OOP


un docker pour la parti Flask ( api, site):
-------------------------------------------
	
	Creation dossier app:
	---------------------
		APP:
		----
			Flask Server en Mode Webhook :
			------------------------------
				Reçois les Données de TradingView sous la Form d'un Json:
				---------------------------------------------------------
					Nous pouvons recevoire toute les alerte pour le moment , il faudrait que l'on puisse coupler le AADI et LE ML pour avoir nos bons point d'entrée


		Template:
		---------
			contien les views | page html|
				* base.html:
				------------
					page de Model pour la construction des autre page 				|| FAIT 
					Page index model avec Lorem Ipsum pour un model D'arrivage		|| FAIT 





un docker de communication 

Je Pense Passer Par La Lib Flask WebSocket
________________________________________________________________________________________________
________________________________________________________________________________________________

INFO ROBOT || TV || PYTHON-BOT:
-------------------------------

TV:
---
	pour le moment nous avons un probleme pour recupéré les differente indication des Pine Script
	il nous faut Reussire a combiner nos alerte

PYTHON-BOT:
-----------
	Tous Le code Fonctionne Il est Juste TRes TRes Lent 